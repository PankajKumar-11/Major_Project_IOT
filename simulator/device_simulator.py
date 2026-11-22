"""
Virtual IoT Device Simulator.
Models realistic smart factory devices:
- temperature_sensor_01: Environmental telemetry
- humidity_sensor_02: Environmental telemetry
- energy_meter_03: Power and voltage telemetry
- motor_controller_04: Industrial drive controller (Critical actuator)
- smart_camera_05: Surveillance vision stream metadata
"""
import time
import json
import random
import secrets
from typing import Dict, Any, Optional

class VirtualIoTDevice:
    def __init__(self, device_id: str, device_type: str, role: str, typical_rate_hz: float = 1.0, typical_payload_bytes: int = 64, sensitivity: str = "LOW"):
        self.device_id = device_id
        self.device_type = device_type
        self.role = role
        self.typical_rate_hz = typical_rate_hz
        self.typical_payload_bytes = typical_payload_bytes
        self.sensitivity = sensitivity
        self.secret_key = f"{device_id}_secret_2026"
        
        # State
        self.mode = "NORMAL"  # NORMAL, FLOODING, COMPROMISED, UNAUTHORIZED, REPLAY, LOW_SLOW
        self.seq_num = 0
        self.last_sent_time = 0.0
        self.is_active = True
        
        # Stored message for replay attack simulation
        self.saved_replay_msg: Optional[Dict[str, Any]] = None

    def set_mode(self, mode: str):
        self.mode = mode

    def generate_next_message(self) -> Optional[Dict[str, Any]]:
        """
        Generates next simulated MQTT message depending on device state and mode.
        """
        if not self.is_active:
            return None

        now = time.time()
        self.seq_num += 1
        nonce = secrets.token_hex(8)

        # 1. NORMAL MODE
        if self.mode == "NORMAL":
            topic, payload_data = self._generate_normal_telemetry()
            payload_str = json.dumps(payload_data)
            
            # Store copy for potential replay simulation later
            self.saved_replay_msg = {
                "topic": topic,
                "payload": payload_str,
                "seq_num": self.seq_num,
                "nonce": nonce
            }

            return {
                "device_id": self.device_id,
                "topic": topic,
                "payload": payload_str,
                "seq_num": self.seq_num,
                "nonce": nonce,
                "size_bytes": len(payload_str.encode())
            }

        # 2. FLOODING MODE
        elif self.mode == "FLOODING":
            topic, payload_data = self._generate_normal_telemetry()
            payload_data["flood_tag"] = "DoS_TRAFFIC_BURST"
            payload_str = json.dumps(payload_data)
            return {
                "device_id": self.device_id,
                "topic": topic,
                "payload": payload_str,
                "seq_num": self.seq_num,
                "nonce": nonce,
                "size_bytes": len(payload_str.encode())
            }

        # 3. UNAUTHORIZED TOPIC ACCESS (Privilege Escalation)
        elif self.mode == "UNAUTHORIZED":
            # Attempt to publish to high sensitivity actuator topic (forbidden for sensors)
            unauth_topic = "factory/motor/commands"
            malicious_payload = {
                "command": "EMERGENCY_OVERRIDE_SHUTDOWN",
                "target_rpm": 9999,
                "source": self.device_id,
                "timestamp": now
            }
            payload_str = json.dumps(malicious_payload)
            return {
                "device_id": self.device_id,
                "topic": unauth_topic,
                "payload": payload_str,
                "seq_num": self.seq_num,
                "nonce": nonce,
                "size_bytes": len(payload_str.encode())
            }

        # 4. COMPROMISED AUTHENTICATED DEVICE
        elif self.mode == "COMPROMISED":
            # Authenticated device sending malicious payloads or exfiltration
            topic = f"factory/telemetry/{self.device_id}"
            exfil_data = {
                "exfil": "A" * 800,  # Giant abnormal payload size
                "malicious_inject": "' OR '1'='1' --",
                "exploit_signature": "CVE-2026-IOT-EXEC",
                "timestamp": now
            }
            payload_str = json.dumps(exfil_data)
            return {
                "device_id": self.device_id,
                "topic": topic,
                "payload": payload_str,
                "seq_num": self.seq_num,
                "nonce": nonce,
                "size_bytes": len(payload_str.encode())
            }

        # 5. REPLAY ATTACK MODE
        elif self.mode == "REPLAY":
            if self.saved_replay_msg:
                # Re-send previous packet with exact same nonce and old sequence number!
                return {
                    "device_id": self.device_id,
                    "topic": self.saved_replay_msg["topic"],
                    "payload": self.saved_replay_msg["payload"],
                    "seq_num": self.saved_replay_msg["seq_num"], # Stale seq!
                    "nonce": self.saved_replay_msg["nonce"],     # Stale nonce!
                    "size_bytes": len(self.saved_replay_msg["payload"].encode())
                }
            else:
                return self.generate_next_message()

        # 6. LOW AND SLOW ANOMALY
        elif self.mode == "LOW_SLOW":
            # Subtle payload drift (+200 bytes) and occasional sensitive probes
            topic, payload_data = self._generate_normal_telemetry()
            payload_data["stealth_probe"] = "x" * 150
            payload_str = json.dumps(payload_data)
            return {
                "device_id": self.device_id,
                "topic": topic,
                "payload": payload_str,
                "seq_num": self.seq_num,
                "nonce": nonce,
                "size_bytes": len(payload_str.encode())
            }

        return None

    # pyrefly: ignore[invalid-annotation]
    def _generate_normal_telemetry(self) -> (str, dict):
        """Generates realistic telemetry dictionary according to device profile."""
        now = time.time()
        if "temperature" in self.device_id:
            return (
                f"factory/temperature/{self.device_id}",
                {
                    "device_id": self.device_id,
                    "temperature_c": round(22.5 + random.uniform(-1.5, 1.5), 2),
                    "status": "NOMINAL",
                    "timestamp": now
                }
            )
        elif "humidity" in self.device_id:
            return (
                f"factory/humidity/{self.device_id}",
                {
                    "device_id": self.device_id,
                    "relative_humidity_pct": round(45.0 + random.uniform(-3.0, 3.0), 1),
                    "status": "NOMINAL",
                    "timestamp": now
                }
            )
        elif "energy" in self.device_id:
            return (
                f"factory/energy/{self.device_id}",
                {
                    "device_id": self.device_id,
                    "voltage_v": round(230.0 + random.uniform(-2.0, 2.0), 1),
                    "current_a": round(14.2 + random.uniform(-0.5, 0.5), 2),
                    "active_power_kw": 3.26,
                    "timestamp": now
                }
            )
        elif "motor" in self.device_id:
            return (
                "factory/motor/status",
                {
                    "device_id": self.device_id,
                    "rpm": round(1450 + random.uniform(-15, 15), 0),
                    "bearing_temp_c": round(54.0 + random.uniform(-1.0, 1.0), 1),
                    "vibration_mm_s": 1.2,
                    "status": "RUNNING",
                    "timestamp": now
                }
            )
        elif "camera" in self.device_id:
            return (
                "factory/camera/stream_meta",
                {
                    "device_id": self.device_id,
                    "frame_id": self.seq_num,
                    "resolution": "1920x1080",
                    "fps": 30,
                    "detections": ["forklift_01", "worker_safety_vest"],
                    "timestamp": now
                }
            )
        else:
            return (
                f"factory/telemetry/{self.device_id}",
                {"device_id": self.device_id, "timestamp": now, "val": random.randint(10, 100)}
            )

