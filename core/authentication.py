"""
Authentication Module for Zero Trust IoT Framework.
Features:
- Device credential verification with HMAC-SHA256
- Nonce generation and verification for dynamic CHALLENGE responses
- Authentication failure tracking and security event logging
- Zero Trust principle: Authentication is necessary but not sufficient for trust.
"""
import hmac
import hashlib
import secrets
import time
import logging
from typing import Dict, Tuple, Optional
from database.db_manager import DatabaseManager

logger = logging.getLogger("AuthModule")

class AuthenticationManager:
    def __init__(self, db: DatabaseManager):
        self.db = db
        # Track recent failures in-memory for instant fast response
        self.recent_failed_attempts: Dict[str, int] = {}
        # Active challenges: nonce -> (device_id, expires_at)
        self.active_challenges: Dict[str, Tuple[str, float]] = {}

    def register_device(self, device_id: str, device_type: str, role: str, secret_key: str, sensitivity: str = "LOW"):
        """Registers a new device with hashed secret."""
        secret_hash = hashlib.sha256(secret_key.encode()).hexdigest()
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT OR REPLACE INTO devices (
                device_id, device_type, role, secret_hash, auth_status, current_trust,
                current_confidence, risk_level, access_policy, sensitivity
            ) VALUES (?, ?, ?, ?, 'UNAUTHENTICATED', 90.0, 0.85, 'LOW', 'ALLOW', ?);
            """, (device_id, device_type, role, secret_hash, sensitivity))
            conn.commit()
        logger.info(f"Device {device_id} registered successfully.")

    def authenticate_device(self, device_id: str, secret_key: str) -> Tuple[bool, str]:
        """
        Verifies device credentials.
        Returns: (success: bool, message: str)
        """
        device = self.db.get_device(device_id)
        if not device:
            self.db.log_auth_event(device_id, "FAILED", "Device not registered")
            return False, "Device not registered in registry"

        expected_hash = device["secret_hash"]
        provided_hash = hashlib.sha256(secret_key.encode()).hexdigest()

        if hmac.compare_digest(expected_hash, provided_hash):
            self.db.update_device_auth_status(device_id, "AUTHENTICATED")
            self.db.log_auth_event(device_id, "SUCCESS")
            # Clear failed count
            self.recent_failed_attempts[device_id] = 0
            logger.info(f"Device {device_id} authenticated successfully.")
            return True, "Authentication successful"
        else:
            self.recent_failed_attempts[device_id] = self.recent_failed_attempts.get(device_id, 0) + 1
            self.db.update_device_auth_status(device_id, "AUTH_FAILED")
            self.db.log_auth_event(device_id, "FAILED", f"Invalid secret key (attempt {self.recent_failed_attempts[device_id]})")
            
            # If repeated auth failures, log high-severity security event
            if self.recent_failed_attempts[device_id] >= 3:
                self.db.log_security_event({
                    "device_id": device_id,
                    "event_type": "REPEATED_AUTH_FAILURES",
                    "severity": "HIGH",
                    "description": f"Detected {self.recent_failed_attempts[device_id]} consecutive credential authentication failures.",
                    "trust_before": device.get("current_trust", 90.0),
                    "trust_after": max(10.0, device.get("current_trust", 90.0) - 25.0),
                    "policy_decision": "DENY",
                    "reason": "Brute-force credential stuffing / authentication failure threshold exceeded"
                })
            logger.warning(f"Device {device_id} authentication failed.")
            return False, "Invalid credentials"

    def issue_challenge(self, device_id: str, ttl_seconds: float = 30.0) -> str:
        """
        Generates a fresh cryptographic nonce for CHALLENGE access control policy.
        """
        nonce = secrets.token_hex(16)
        expires_at = time.time() + ttl_seconds
        self.active_challenges[nonce] = (device_id, expires_at)
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO challenge_records (device_id, nonce, status)
            VALUES (?, ?, 'PENDING');
            """, (device_id, nonce))
            conn.commit()
            
        logger.info(f"Issued challenge nonce for {device_id}: {nonce[:8]}...")
        return nonce

    def verify_challenge_response(self, device_id: str, nonce: str, response_token: str, secret_key: str) -> bool:
        """
        Validates HMAC(secret_key, nonce) == response_token.
        """
        if nonce not in self.active_challenges:
            return False

        saved_device_id, expires_at = self.active_challenges[nonce]
        if saved_device_id != device_id or time.time() > expires_at:
            # Expired or device mismatch
            self.active_challenges.pop(nonce, None)
            return False

        # Calculate expected HMAC response
        expected_token = hmac.new(secret_key.encode(), nonce.encode(), hashlib.sha256).hexdigest()
        is_valid = hmac.compare_digest(expected_token, response_token)

        if is_valid:
            self.active_challenges.pop(nonce, None)
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                UPDATE challenge_records 
                SET status = 'VERIFIED', verified_at = CURRENT_TIMESTAMP
                WHERE nonce = ? AND device_id = ?;
                """, (nonce, device_id))
                conn.commit()
            logger.info(f"Device {device_id} successfully verified challenge nonce {nonce[:8]}...")
            return True
        else:
            logger.warning(f"Device {device_id} failed challenge response verification.")
            return False

    def get_failure_count(self, device_id: str) -> int:
        return self.recent_failed_attempts.get(device_id, 0)

