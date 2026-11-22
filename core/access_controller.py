"""
Access Control and Dynamic Enforcement Module.
Enforces real-time access policies on every MQTT message.
Coordinates with simulated broker and Mosquitto ACL generator.
"""
import json
import logging
from typing import Dict, List, Tuple, Any, Optional
from database.db_manager import DatabaseManager
from mqtt.acl_generator import MosquittoACLGenerator
from config import SENSITIVE_TOPICS

logger = logging.getLogger("AccessController")

class DynamicAccessController:
    def __init__(self, db: DatabaseManager, acl_generator: Optional[MosquittoACLGenerator] = None):
        self.db = db
        self.acl_generator = acl_generator or MosquittoACLGenerator()

    def check_publish_permission(self, device_id: str, topic: str, message: Any) -> Tuple[bool, str]:
        """
        Determines if a device is permitted to publish to the specified topic right now.
        Returns: (allowed: bool, reason: str)
        """
        device = self.db.get_device(device_id)
        if not device:
            return False, f"Device {device_id} is not registered in system."

        policy = device.get("access_policy", "ALLOW")
        auth_status = device.get("auth_status", "UNAUTHENTICATED")

        # Zero Trust principle: Authentication is required
        if auth_status != "AUTHENTICATED":
            return False, f"Device {device_id} is not authenticated (status: {auth_status})."

        # 1. DENY Policy Check
        if policy == "DENY":
            return False, f"Access revoked by Zero Trust Policy Engine (Policy: DENY, Trust: {device.get('current_trust', 0)})."

        # Parse authorized topics
        allowed_publish_raw = device.get("allowed_publish", "[]")
        allowed_publish: List[str] = json.loads(allowed_publish_raw) if isinstance(allowed_publish_raw, str) else allowed_publish_raw

        # 2. Scope & Topic Authorization Check
        # Check if topic is in device's authorized list
        is_topic_authorized = any(
            topic == allowed or (allowed.endswith("#") and topic.startswith(allowed[:-1]))
            for allowed in allowed_publish
        )

        if not is_topic_authorized:
            # Unauthorized topic access attempt!
            self.db.log_security_event({
                "device_id": device_id,
                "event_type": "UNAUTHORIZED_TOPIC_ACCESS",
                "severity": "CRITICAL" if any(s in topic for s in SENSITIVE_TOPICS) else "HIGH",
                "description": f"Device attempted to publish to unauthorized topic: {topic}",
                "trust_before": device.get("current_trust", 90.0),
                "trust_after": max(10.0, device.get("current_trust", 90.0) - 45.0),
                "policy_decision": "DENY",
                "reason": f"Privilege escalation / lateral movement attempt on {topic}"
            })
            return False, f"Unauthorized topic {topic} for device {device_id}."

        # 3. RESTRICT Policy Check
        if policy == "RESTRICT":
            # If the topic is sensitive (e.g. motor commands, control, admin), block it!
            if any(sens in topic for sens in SENSITIVE_TOPICS) or "command" in topic or "control" in topic:
                return False, f"Topic {topic} blocked: Device {device_id} is under RESTRICT policy (Trust: {device.get('current_trust')})."

        # 4. CHALLENGE Policy Check
        if policy == "CHALLENGE":
            # When challenge is pending, critical commands are blocked until nonce verified
            if any(sens in topic for sens in SENSITIVE_TOPICS):
                return False, f"Action blocked: Pending cryptographic challenge verification for {device_id}."

        return True, "Access granted"

    def sync_external_mosquitto_acl(self):
        """Regenerates Mosquitto ACL files to mirror Zero Trust policies."""
        devices = self.db.get_all_devices()
        return self.acl_generator.sync_acls(devices)

