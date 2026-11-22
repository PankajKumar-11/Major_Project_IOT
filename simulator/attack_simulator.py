"""
Attack and Network Simulation Controller.
Controls the launch and lifecycle of 8 distinct research scenarios:
1. Normal device behaviour
2. MQTT message flooding (DoS)
3. Compromised authenticated device
4. Unauthorized topic access (lateral movement)
5. Repeated authentication failures
6. Replay attack simulation
7. Benign network congestion
8. Low-and-slow suspicious behaviour
"""
import time
import logging
from typing import Dict, Any, Optional, List

logger = logging.getLogger("AttackSimulator")

class AttackSimulator:
    SCENARIOS = {
        "NORMAL": "Normal Baseline IoT Operation",
        "FLOODING": "MQTT Message Flooding (High-Rate DoS)",
        "COMPROMISED": "Compromised Authenticated Device (Exploit / Data Exfiltration)",
        "UNAUTHORIZED": "Unauthorized Topic Access (Privilege Escalation)",
        "AUTH_FAIL": "Repeated Authentication Failures (Credential Attack)",
        "REPLAY": "Message Replay Attack (Stale Nonce & Sequence)",
        "CONGESTION": "Benign Network Congestion (Multi-Device Latency Surge)",
        "LOW_SLOW": "Low-and-Slow Stealth Anomaly"
    }

    def __init__(self, simulation_engine):
        self.engine = simulation_engine
        self.active_scenario: str = "NORMAL"
        self.target_device: str = "temperature_sensor_01"
        self.scenario_start_time: float = time.time()
        self.duration_seconds: float = 30.0
        self.execution_logs: List[str] = []

    def start_scenario(self, scenario_key: str, target_device: str = "temperature_sensor_01", duration_sec: float = 30.0):
        """Launches an attack or network scenario."""
        if scenario_key not in self.SCENARIOS:
            raise ValueError(f"Unknown scenario: {scenario_key}")

        self.active_scenario = scenario_key
        self.target_device = target_device
        self.duration_seconds = duration_sec
        self.scenario_start_time = time.time()

        log_msg = f"[{time.strftime('%H:%M:%S')}] Started scenario: {self.SCENARIOS[scenario_key]} on target '{target_device}' for {duration_sec}s"
        self.execution_logs.append(log_msg)
        logger.info(log_msg)

        # 1. Reset all devices to normal first
        for dev in self.engine.devices.values():
            dev.set_mode("NORMAL")
        self.engine.network_monitor.set_congestion_simulation(False)

        # 2. Configure target according to scenario
        if scenario_key == "NORMAL":
            pass # All already normal

        elif scenario_key == "FLOODING":
            if target_device in self.engine.devices:
                self.engine.devices[target_device].set_mode("FLOODING")

        elif scenario_key == "COMPROMISED":
            if target_device in self.engine.devices:
                self.engine.devices[target_device].set_mode("COMPROMISED")

        elif scenario_key == "UNAUTHORIZED":
            if target_device in self.engine.devices:
                self.engine.devices[target_device].set_mode("UNAUTHORIZED")

        elif scenario_key == "AUTH_FAIL":
            # Simulate bad credential attempts in authentication module
            for _ in range(3):
                self.engine.auth_manager.authenticate_device(target_device, "WRONG_ATTACKER_SECRET_KEY")
                self.engine.behavior_monitor.record_auth_failure(target_device)
            self.engine.adaptive_scheduler.trigger_immediate_evaluation(target_device)

        elif scenario_key == "REPLAY":
            if target_device in self.engine.devices:
                self.engine.devices[target_device].set_mode("REPLAY")

        elif scenario_key == "CONGESTION":
            # Simulate multi-device network latency spike & packet jitter
            self.engine.network_monitor.set_congestion_simulation(True, intensity=0.85)

        elif scenario_key == "LOW_SLOW":
            if target_device in self.engine.devices:
                self.engine.devices[target_device].set_mode("LOW_SLOW")

    def check_scenario_timer(self):
        """Checks if current scenario has expired, reverting back to NORMAL."""
        if self.active_scenario != "NORMAL":
            elapsed = time.time() - self.scenario_start_time
            if elapsed >= self.duration_seconds:
                log_msg = f"[{time.strftime('%H:%M:%S')}] Scenario '{self.active_scenario}' expired ({self.duration_seconds}s). Reverting to NORMAL."
                self.execution_logs.append(log_msg)
                logger.info(log_msg)
                self.start_scenario("NORMAL")

    def get_status(self) -> Dict[str, Any]:
        elapsed = time.time() - self.scenario_start_time
        remaining = max(0.0, self.duration_seconds - elapsed) if self.active_scenario != "NORMAL" else 0.0
        return {
            "active_scenario": self.active_scenario,
            "scenario_name": self.SCENARIOS.get(self.active_scenario, "Normal"),
            "target_device": self.target_device,
            "duration_seconds": self.duration_seconds,
            "elapsed_seconds": round(elapsed, 1),
            "remaining_seconds": round(remaining, 1),
            "recent_logs": self.execution_logs[-10:]
        }

