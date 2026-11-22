"""
Device Behaviour Monitoring Module with ML-Assisted Anomaly Detection.
Tracks sliding window behaviour metrics for each IoT device:
- Publishing rate (Hz) and rate anomaly
- Unauthorized topic access attempts
- Authentication failures
- Payload size deviation
- Reconnections and connection stability
- Replay detection (nonces and sequence numbers)
- Uses Scikit-learn models to dynamically score behavioral anomalies.
"""
import time
import math
import numpy as np
import logging
from collections import deque, defaultdict
from typing import Dict, List, Any, Optional
from database.db_manager import DatabaseManager
from config import DEFAULT_DEVICES

logger = logging.getLogger("BehaviorMonitor")

class DeviceBehaviorProfile:
    def __init__(self, device_id: str, baseline_rate: float = 1.0, baseline_payload: float = 64.0):
        self.device_id = device_id
        self.baseline_rate = baseline_rate
        self.baseline_payload = baseline_payload
        
        # Sliding window buffer: stores (timestamp, payload_size, topic, seq_num, nonce)
        self.message_window: deque = deque(maxlen=200)
        self.unauth_attempts = 0
        self.auth_failures = 0
        self.reconnections = 0
        self.replay_attempts = 0
        
        # Nonce and sequence cache for replay detection
        self.seen_nonces = set()
        self.last_seq_num = -1

class BehaviorMonitor:
    def __init__(self, db: DatabaseManager):
        self.db = db
        self.profiles: Dict[str, DeviceBehaviorProfile] = {}
        
        # Initialize profiles from default configs
        for d in DEFAULT_DEVICES:
            self.profiles[d["device_id"]] = DeviceBehaviorProfile(
                d["device_id"],
                baseline_rate=d.get("typical_rate_hz", 1.0),
                baseline_payload=d.get("typical_payload_bytes", 64.0)
            )

    def record_message(self, device_id: str, topic: str, payload_size: int, seq_num: int = 0, nonce: str = "") -> bool:
        """
        Records an incoming MQTT message from an IoT device.
        Checks for replay attacks (duplicate nonce or non-increasing sequence number).
        Returns: is_replay (bool)
        """
        if device_id not in self.profiles:
            self.profiles[device_id] = DeviceBehaviorProfile(device_id)

        prof = self.profiles[device_id]
        now = time.time()
        is_replay = False

        # Sequence & Nonce Replay Check
        if nonce and nonce in prof.seen_nonces:
            is_replay = True
            prof.replay_attempts += 1
            logger.warning(f"[REPLAY ATTACK] Duplicate nonce detected from {device_id}: {nonce[:8]}")
        elif seq_num > 0 and seq_num <= prof.last_seq_num:
            is_replay = True
            prof.replay_attempts += 1
            logger.warning(f"[REPLAY ATTACK] Stale sequence number from {device_id}: seq {seq_num} <= last {prof.last_seq_num}")
        else:
            if nonce:
                prof.seen_nonces.add(nonce)
                # Cap seen nonces memory
                if len(prof.seen_nonces) > 500:
                    prof.seen_nonces.pop()
            if seq_num > 0:
                prof.last_seq_num = seq_num

        prof.message_window.append((now, payload_size, topic, seq_num, nonce))
        return is_replay

    def record_unauthorized_attempt(self, device_id: str, topic: str):
        if device_id not in self.profiles:
            self.profiles[device_id] = DeviceBehaviorProfile(device_id)
        self.profiles[device_id].unauth_attempts += 1
        logger.warning(f"[SECURITY ALERT] Device {device_id} attempted unauthorized access to {topic}")

    def record_auth_failure(self, device_id: str):
        if device_id not in self.profiles:
            self.profiles[device_id] = DeviceBehaviorProfile(device_id)
        self.profiles[device_id].auth_failures += 1

    def record_reconnection(self, device_id: str):
        if device_id not in self.profiles:
            self.profiles[device_id] = DeviceBehaviorProfile(device_id)
        self.profiles[device_id].reconnections += 1

    def compute_behavior_features(self, device_id: str, window_sec: float = 10.0) -> Dict[str, Any]:
        """
        Calculates normalized behavioral anomaly features over the given time window.
        Returns a dictionary of normalized values [0.0 - 1.0].
        """
        if device_id not in self.profiles:
            self.profiles[device_id] = DeviceBehaviorProfile(device_id)

        prof = self.profiles[device_id]
        now = time.time()
        cutoff = now - window_sec

        # Filter messages in window
        recent_msgs = [m for m in prof.message_window if m[0] >= cutoff]
        msg_count = len(recent_msgs)
        current_rate_hz = round(msg_count / window_sec, 2)

        # 1. Rate Anomaly Score [0, 1]
        # Compare current rate to baseline rate
        baseline = prof.baseline_rate
        if current_rate_hz <= baseline * 1.5:
            rate_anomaly = 0.0
        else:
            # Normalized surge: rate exceeds 5x baseline -> anomaly score approaches 1.0
            excess = (current_rate_hz - baseline) / max(1.0, baseline * 4.0)
            rate_anomaly = min(1.0, max(0.0, excess))

        # 2. Payload Anomaly Score [0, 1]
        if recent_msgs:
            payload_sizes = [m[1] for m in recent_msgs]
            payload_mean = float(np.mean(payload_sizes))
            payload_std = float(np.std(payload_sizes))
            # Deviation from expected baseline
            ratio = abs(payload_mean - prof.baseline_payload) / max(32.0, prof.baseline_payload)
            payload_anomaly = min(1.0, max(0.0, ratio / 3.0))
        else:
            payload_mean = prof.baseline_payload
            payload_std = 0.0
            payload_anomaly = 0.0

        # 3. Unauthorized Topic Access Score [0, 1]
        # Even 1 attempt is an anomaly, >= 3 attempts saturates to 1.0
        unauth_anomaly = min(1.0, prof.unauth_attempts / 2.0)

        # 4. Authentication Failure Score [0, 1]
        auth_fail_anomaly = min(1.0, prof.auth_failures / 2.0)

        # 5. Connection Anomaly Score [0, 1]
        # High reconnection churn indicates instability or session hijacking
        conn_anomaly = min(1.0, prof.reconnections / 3.0)

        # 6. Replay Anomaly Score [0, 1]
        replay_anomaly = min(1.0, prof.replay_attempts / 1.0)

        features = {
            "device_id": device_id,
            "window_sec": window_sec,
            "msg_count": msg_count,
            "rate_hz": current_rate_hz,
            "rate_anomaly": round(rate_anomaly, 3),
            "payload_mean": round(payload_mean, 1),
            "payload_std": round(payload_std, 1),
            "payload_anomaly": round(payload_anomaly, 3),
            "unauth_attempts": prof.unauth_attempts,
            "unauth_anomaly": round(unauth_anomaly, 3),
            "auth_failures": prof.auth_failures,
            "auth_fail_anomaly": round(auth_fail_anomaly, 3),
            "reconnections": prof.reconnections,
            "conn_anomaly": round(conn_anomaly, 3),
            "replay_attempts": prof.replay_attempts,
            "replay_anomaly": round(replay_anomaly, 3)
        }

        # Save record to DB
        self.db.log_behavior(device_id, features)
        return features

    def reset_counters(self, device_id: Optional[str] = None):
        """Resets sliding counters after evaluation cycle."""
        if device_id:
            if device_id in self.profiles:
                p = self.profiles[device_id]
                p.unauth_attempts = 0
                p.auth_failures = 0
                p.reconnections = 0
                p.replay_attempts = 0
        else:
            for p in self.profiles.values():
                p.unauth_attempts = 0
                p.auth_failures = 0
                p.reconnections = 0
                p.replay_attempts = 0

