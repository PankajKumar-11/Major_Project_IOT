"""
Global Configuration for Behaviour-Aware Zero Trust IoT Network Framework.
Academic Research Prototype.
"""
import os
from pathlib import Path
from pydantic import BaseModel
from typing import Dict, List

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
DB_PATH = DATA_DIR / "zerotrust_iot.db"
RESULTS_DIR = BASE_DIR / "evaluation" / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# Default Device Profiles
DEFAULT_DEVICES = [
    {
        "device_id": "temperature_sensor_01",
        "device_type": "sensor",
        "role": "environmental_monitor",
        "allowed_publish": ["factory/temperature/temperature_sensor_01", "factory/telemetry/heartbeat"],
        "allowed_subscribe": ["factory/config/temperature_sensor_01"],
        "typical_rate_hz": 1.0,
        "typical_payload_bytes": 64,
        "sensitivity": "LOW",
        "initial_trust": 95.0
    },
    {
        "device_id": "humidity_sensor_02",
        "device_type": "sensor",
        "role": "environmental_monitor",
        "allowed_publish": ["factory/humidity/humidity_sensor_02", "factory/telemetry/heartbeat"],
        "allowed_subscribe": ["factory/config/humidity_sensor_02"],
        "typical_rate_hz": 0.5,
        "typical_payload_bytes": 56,
        "sensitivity": "LOW",
        "initial_trust": 95.0
    },
    {
        "device_id": "energy_meter_03",
        "device_type": "meter",
        "role": "power_monitor",
        "allowed_publish": ["factory/energy/energy_meter_03", "factory/telemetry/heartbeat"],
        "allowed_subscribe": ["factory/config/energy_meter_03"],
        "typical_rate_hz": 2.0,
        "typical_payload_bytes": 128,
        "sensitivity": "MEDIUM",
        "initial_trust": 95.0
    },
    {
        "device_id": "motor_controller_04",
        "device_type": "actuator",
        "role": "production_control",
        "allowed_publish": ["factory/motor/status", "factory/telemetry/heartbeat"],
        "allowed_subscribe": ["factory/motor/commands"],
        "typical_rate_hz": 1.0,
        "typical_payload_bytes": 192,
        "sensitivity": "CRITICAL",
        "initial_trust": 95.0
    },
    {
        "device_id": "smart_camera_05",
        "device_type": "camera",
        "role": "surveillance",
        "allowed_publish": ["factory/camera/stream_meta", "factory/camera/events", "factory/telemetry/heartbeat"],
        "allowed_subscribe": ["factory/camera/config"],
        "typical_rate_hz": 5.0,
        "typical_payload_bytes": 1024,
        "sensitivity": "HIGH",
        "initial_trust": 95.0
    }
]

# Sensitive Topics (Unauthorized access triggers critical overrides)
SENSITIVE_TOPICS = [
    "factory/motor/commands",
    "factory/safety/shutdown",
    "factory/admin/credentials",
    "factory/firmware/update"
]

# Trust Calculation Weights (Configurable)
DEFAULT_TRUST_WEIGHTS = {
    "rate_anomaly": 0.20,
    "unauthorized_topic": 0.30,
    "auth_failures": 0.25,
    "payload_anomaly": 0.15,
    "connection_anomaly": 0.10
}

# Smoothing Factor: Current Trust = alpha * Previous + (1 - alpha) * Newly Calculated
SMOOTHING_ALPHA = 0.70

# Zero Trust Policy Decision Thresholds
DEFAULT_THRESHOLDS = {
    "allow_trust": 80.0,
    "restrict_trust": 50.0,
    "min_confidence_for_allow": 0.60,
    "challenge_confidence_threshold": 0.40
}

# Adaptive Reassessment Intervals (in seconds)
REASSESSMENT_INTERVALS = {
    "LOW_RISK": 30.0,     # Normal conditions
    "MEDIUM_RISK": 10.0,  # Suspicious activity
    "HIGH_RISK": 2.0      # Critical / anomaly active
}

# Network Congestion Thresholds
NETWORK_THRESHOLDS = {
    "congestion_latency_ms": 120.0,
    "congestion_packet_loss_pct": 8.0,
    "multi_device_affected_ratio": 0.60  # At least 60% devices affected = network congestion
}

