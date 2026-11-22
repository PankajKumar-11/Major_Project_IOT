"""
Simulation Engine and Orchestrator.
Main background loop that drives virtual IoT devices, MQTT messaging,
continuous trust assessment, and adaptive Zero Trust enforcement.
"""
import time
import threading
import logging
from typing import Dict, List, Any, Optional

from database.db_manager import DatabaseManager
from mqtt.simulated_broker import SimulatedMQTTBroker
from core.authentication import AuthenticationManager
from core.network_monitor import NetworkMonitor
from core.behavior_monitor import BehaviorMonitor
from core.trust_engine import TrustEvaluationEngine
from core.confidence_engine import ConfidenceEvaluationEngine
from core.policy_engine import ZeroTrustPolicyEngine, PolicyDecision
from core.access_controller import DynamicAccessController
from core.adaptive_scheduler import AdaptiveVerificationScheduler
from simulator.device_simulator import VirtualIoTDevice
from simulator.attack_simulator import AttackSimulator
from config import DEFAULT_DEVICES

logger = logging.getLogger("SimulationEngine")

class SimulationEngine:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SimulationEngine, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, db: Optional[DatabaseManager] = None):
        if self._initialized:
            return
        self._initialized = True
        
        # 1. Initialize Database
        self.db = db or DatabaseManager()
        
        # 2. Initialize Core Subsystems
        self.broker = SimulatedMQTTBroker()
        self.auth_manager = AuthenticationManager(self.db)
        self.network_monitor = NetworkMonitor(self.db)
        self.behavior_monitor = BehaviorMonitor(self.db)
        self.trust_engine = TrustEvaluationEngine(self.db)
        self.confidence_engine = ConfidenceEvaluationEngine()
        self.policy_engine = ZeroTrustPolicyEngine()
        self.access_controller = DynamicAccessController(self.db)
        self.adaptive_scheduler = AdaptiveVerificationScheduler()

        # Connect access controller to broker
        self.broker.set_access_controller(self.access_controller)

        # 3. Initialize Virtual IoT Devices
        self.devices: Dict[str, VirtualIoTDevice] = {}
        for d in DEFAULT_DEVICES:
            dev = VirtualIoTDevice(
                device_id=d["device_id"],
                device_type=d["device_type"],
                role=d["role"],
                typical_rate_hz=d.get("typical_rate_hz", 1.0),
                typical_payload_bytes=d.get("typical_payload_bytes", 64),
                sensitivity=d.get("sensitivity", "LOW")
            )
            self.devices[dev.device_id] = dev

        # 4. Initialize Attack Simulator
        self.attack_simulator = AttackSimulator(self)

        # 5. Thread control
        self.is_running = False
        self.thread: Optional[threading.Thread] = None
        self.lock = threading.Lock()
        
        # Timing
        self.tick_count = 0
        self.last_network_sample_time = 0.0

    def start(self):
        """Starts background simulation loop thread."""
        with self.lock:
            if not self.is_running:
                self.is_running = True
                self.thread = threading.Thread(target=self._run_loop, daemon=True)
                self.thread.start()
                logger.info("Simulation Engine thread started.")

    def stop(self):
        """Stops background simulation loop thread."""
        with self.lock:
            self.is_running = False
        if self.thread:
            self.thread.join(timeout=1.0)
            logger.info("Simulation Engine thread stopped.")

    def _run_loop(self):
        while self.is_running:
            try:
                self.step_cycle()
            except Exception as e:
                logger.error(f"Error in simulation cycle: {e}", exc_info=True)
            time.sleep(0.5)

    def step_cycle(self):
        """Executes one simulation step cycle."""
        now = time.time()
        self.tick_count += 1

        # A. Check Attack Simulator Timer
        self.attack_simulator.check_scenario_timer()

        # B. Generate & Publish Device Messages
        for dev_id, dev in self.devices.items():
            # If device is flooding, produce multiple messages per cycle
            burst = 8 if dev.mode == "FLOODING" else 1

            for _ in range(burst):
                msg_dict = dev.generate_next_message()
                if msg_dict:
                    # Check replay detection
                    is_replay = self.behavior_monitor.record_message(
                        device_id=dev_id,
                        topic=msg_dict["topic"],
                        payload_size=msg_dict["size_bytes"],
                        seq_num=msg_dict["seq_num"],
                        nonce=msg_dict["nonce"]
                    )

                    # Simulate network latency measurement
                    sim_lat = 18.0 + (150.0 if self.network_monitor.manual_congestion_active else 0.0)
                    self.network_monitor.record_device_network_ping(dev_id, sim_lat)

                    # Attempt publish through broker & Zero Trust Access Controller
                    allowed = self.broker.publish(
                        topic=msg_dict["topic"],
                        payload=msg_dict["payload"],
                        publisher_id=dev_id,
                        seq_num=msg_dict["seq_num"],
                        nonce=msg_dict["nonce"]
                    )

                    if not allowed:
                        # Record unauthorized attempt in behavior profile
                        self.behavior_monitor.record_unauthorized_attempt(dev_id, msg_dict["topic"])
                        self.adaptive_scheduler.trigger_immediate_evaluation(dev_id)

        # C. Periodic Network & System Monitoring (every 2 seconds)
        if now - self.last_network_sample_time >= 2.0:
            self.last_network_sample_time = now
            throughput = self.broker.get_throughput(window_sec=3.0)
            broker_delay = self.broker.get_average_broker_latency()
            net_metric = self.network_monitor.collect_network_snapshot(
                broker_delay_ms=broker_delay,
                throughput_msg_sec=throughput
            )
        else:
            net_metric = {
                "avg_latency_ms": 18.0,
                "packet_loss_pct": 0.5,
                "is_congested": self.network_monitor.manual_congestion_active,
                "affected_devices_count": 4 if self.network_monitor.manual_congestion_active else 0
            }

        # D. Continuous Zero Trust Evaluation for Due Devices
        for dev_id, dev in self.devices.items():
            db_dev = self.db.get_device(dev_id)
            if not db_dev:
                continue

            current_risk = db_dev.get("risk_level", "LOW")
            is_due = self.adaptive_scheduler.is_due_for_reassessment(dev_id, current_risk)

            if is_due:
                self.adaptive_scheduler.mark_evaluated(dev_id)
                self.evaluate_single_device(dev_id, db_dev, net_metric)

    def evaluate_single_device(self, dev_id: str, db_dev: Dict[str, Any], net_metric: Dict[str, Any]):
        """Evaluates trust, confidence, policy, and updates access state for one device."""
        # 1. Extract Behavioral Features
        behavior = self.behavior_monitor.compute_behavior_features(dev_id, window_sec=10.0)

        # 2. Evaluate Confidence
        confidence = self.confidence_engine.evaluate_confidence(behavior, net_metric)

        # 3. Continuous Trust Score Calculation
        prev_trust = db_dev.get("current_trust", 95.0)
        eval_result = self.trust_engine.evaluate_device_trust(
            device_id=dev_id,
            behavior=behavior,
            network_metric=net_metric,
            confidence_score=confidence,
            previous_trust=prev_trust,
            enable_network_context=True
        )

        new_trust = eval_result["smoothed_trust"]

        # 4. Dynamic Policy Engine Access Decision
        policy_decision, risk_level, reason = self.policy_engine.evaluate_policy(
            device_id=dev_id,
            trust_score=new_trust,
            confidence_score=confidence,
            behavior=behavior,
            sensitivity=db_dev.get("sensitivity", "LOW")
        )

        old_policy = db_dev.get("access_policy", "ALLOW")

        # 5. Handle CHALLENGE policy
        if policy_decision == PolicyDecision.CHALLENGE and old_policy != PolicyDecision.CHALLENGE:
            nonce = self.auth_manager.issue_challenge(dev_id)
            # Virtual device automatically responds if authentic
            secret = f"{dev_id}_secret_2026"
            import hmac, hashlib
            token = hmac.new(secret.encode(), nonce.encode(), hashlib.sha256).hexdigest()
            self.auth_manager.verify_challenge_response(dev_id, nonce, token, secret)

        # 6. Check Policy Transition & Security Event Logging
        if old_policy != policy_decision or abs(new_trust - prev_trust) >= 15.0:
            severity = "CRITICAL" if policy_decision == PolicyDecision.DENY else ("MEDIUM" if policy_decision == PolicyDecision.RESTRICT else "LOW")
            self.db.log_security_event({
                "device_id": dev_id,
                "event_type": f"POLICY_CHANGE_{policy_decision}",
                "severity": severity,
                "description": f"Access policy transitioned from {old_policy} -> {policy_decision}. Trust: {prev_trust} -> {new_trust}",
                "trust_before": prev_trust,
                "trust_after": new_trust,
                "policy_decision": policy_decision,
                "reason": reason
            })

        # 7. Update Database & Dynamic ACL
        self.db.update_device_trust(dev_id, new_trust, confidence, risk_level, policy_decision)
        
        # Reset counters after evaluation cycle
        self.behavior_monitor.reset_counters(dev_id)

