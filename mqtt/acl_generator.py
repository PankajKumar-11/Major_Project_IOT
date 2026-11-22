"""
Mosquitto ACL & Configuration File Generator.
Synchronizes dynamic Zero Trust policy decisions into Mosquitto configuration files:
- mosquitto.conf (disabling anonymous access, setting password and acl file paths)
- mosquitto.acl (fine-grained publish/subscribe permissions per device)
- mosquitto_passwd (device credentials)
"""
import os
import json
from pathlib import Path
from typing import List, Dict, Any
from config import BASE_DIR

MOSQUITTO_DIR = BASE_DIR / "mosquitto_config"
MOSQUITTO_DIR.mkdir(exist_ok=True)

class MosquittoACLGenerator:
    def __init__(self, output_dir: Path = MOSQUITTO_DIR):
        self.output_dir = output_dir
        self.conf_file = output_dir / "mosquitto.conf"
        self.acl_file = output_dir / "mosquitto.acl"
        self.pwd_file = output_dir / "mosquitto.pwd"

    def generate_mosquitto_conf(self, port: int = 1883) -> str:
        """Generates a hardened mosquitto.conf that enforces authentication and ACLs."""
        content = f"""# Behaviour-Aware Zero Trust Mosquitto Configuration
# Generated automatically by Zero Trust Policy Engine

listener {port}
allow_anonymous false
password_file {self.pwd_file.resolve()}
acl_file {self.acl_file.resolve()}

# Logging
log_dest stdout
log_type error
log_type warning
log_type notice
log_type information
connection_messages true
"""
        with open(self.conf_file, "w") as f:
            f.write(content)
        return str(self.conf_file)

    def sync_acls(self, devices: List[Dict[str, Any]]) -> str:
        """
        Translates Zero Trust device states (ALLOW, RESTRICT, DENY)
        into dynamic Mosquitto ACL statements.
        """
        lines = [
            "# Dynamic Zero Trust Access Control List (Mosquitto ACL)",
            "# Regenerated dynamically based on real-time continuous trust evaluations",
            ""
        ]

        for dev in devices:
            dev_id = dev["device_id"]
            policy = dev.get("access_policy", "ALLOW")
            auth_status = dev.get("auth_status", "AUTHENTICATED")
            
            lines.append(f"# Device: {dev_id} | Policy: {policy} | Trust: {dev.get('current_trust', 0.0)}")
            lines.append(f"user {dev_id}")

            # If DENY or unauthenticated, no permissions are granted
            if policy == "DENY" or auth_status != "AUTHENTICATED":
                lines.append("# ACCESS REVOKED: Device is in DENY / quarantined state")
                lines.append("")
                continue

            # Parse allowed topics
            pub_topics = json.loads(dev["allowed_publish"]) if isinstance(dev.get("allowed_publish"), str) else dev.get("allowed_publish", [])
            sub_topics = json.loads(dev["allowed_subscribe"]) if isinstance(dev.get("allowed_subscribe"), str) else dev.get("allowed_subscribe", [])

            # In RESTRICT mode, filter out high sensitivity topics
            if policy == "RESTRICT":
                pub_topics = [t for t in pub_topics if "command" not in t and "control" not in t]
                sub_topics = [t for t in sub_topics if "command" not in t and "control" not in t]
                lines.append("# RESTRICTED: Sensitive topics filtered out")

            for topic in pub_topics:
                lines.append(f"topic write {topic}")
            for topic in sub_topics:
                lines.append(f"topic read {topic}")

            lines.append("")

        with open(self.acl_file, "w") as f:
            f.write("\n".join(lines))
        return str(self.acl_file)

