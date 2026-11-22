"""
Trust Evaluation Engine for Behaviour-Aware Zero Trust IoT Architecture.
Calculates transparent, explainable trust scores using weighted risk,
network context discounts, historical smoothing, and critical security overrides.
"""
import json
import logging
from typing import Dict, Any, Tuple
from config import DEFAULT_TRUST_WEIGHTS, SMOOTHING_ALPHA
from database.db_manager import DatabaseManager

logger = logging.getLogger("TrustEngine")

class TrustEvaluationEngine:
    def __init__(self, db: DatabaseManager, weights: Dict[str, float] = None, alpha: float = SMOOTHING_ALPHA):
        self.db = db
        self.weights = weights or dict(DEFAULT_TRUST_WEIGHTS)
        self.alpha = alpha  # Smoothing factor (default 0.70)

    def set_weights(self, new_weights: Dict[str, float]):
        """Allows configuring weights at runtime for research experiments."""
        total = sum(new_weights.values())
        if total <= 0:
            raise ValueError("Sum of weights must be positive")
        self.weights = {k: v / total for k, v in new_weights.items()}
        logger.info(f"Trust engine weights updated: {self.weights}")

    def evaluate_device_trust(
        self,
        device_id: str,
        behavior: Dict[str, Any],
        network_metric: Dict[str, Any],
        confidence_score: float,
        previous_trust: float = 95.0,
        enable_network_context: bool = True
    ) -> Dict[str, Any]:
        """
        Executes continuous trust evaluation.
        1. Computes weighted risk from behaviour anomalies.
        2. Applies network context discount if network congestion is detected.
        3. Computes raw trust = 100 * (1 - Risk).
        4. Applies historical smoothing: Current = alpha * Previous + (1 - alpha) * Newly_Calculated.
        5. Applies immediate high-severity security overrides if critical violations exist.
        6. Generates human-readable explainability justification.
        """
        reasons = []

        # Extract normalized anomaly components [0.0 - 1.0]
        rate_anomaly = behavior.get("rate_anomaly", 0.0)
        unauth_anomaly = behavior.get("unauth_anomaly", 0.0)
        auth_fail_anomaly = behavior.get("auth_fail_anomaly", 0.0)
        payload_anomaly = behavior.get("payload_anomaly", 0.0)
        conn_anomaly = behavior.get("conn_anomaly", 0.0)
        replay_anomaly = behavior.get("replay_anomaly", 0.0)

        # Replay attacks carry high security penalty
        if replay_anomaly > 0:
            unauth_anomaly = max(unauth_anomaly, replay_anomaly)

        # Network Context Awareness
        network_discount = 0.0
        is_congested = network_metric.get("is_congested", False)
        
        effective_rate_anomaly = rate_anomaly
        effective_conn_anomaly = conn_anomaly

        if enable_network_context and is_congested:
            # Benign congestion causes latency and rate jitter across multiple devices
            network_discount = 0.70
            effective_rate_anomaly = rate_anomaly * (1.0 - network_discount)
            effective_conn_anomaly = conn_anomaly * (1.0 - network_discount)
            reasons.append(
                f"Network congestion detected ({network_metric.get('affected_devices_count', 0)} devices affected, "
                f"latency: {network_metric.get('avg_latency_ms', 0)}ms). "
                f"Rate/connection penalties discounted by {int(network_discount*100)}% to prevent false isolation."
            )

        # Weighted Risk Score [0.0 - 1.0]
        w = self.weights
        risk = (
            w.get("rate_anomaly", 0.20) * effective_rate_anomaly +
            w.get("unauthorized_topic", 0.30) * unauth_anomaly +
            w.get("auth_failures", 0.25) * auth_fail_anomaly +
            w.get("payload_anomaly", 0.15) * payload_anomaly +
            w.get("connection_anomaly", 0.10) * effective_conn_anomaly
        )
        risk = min(1.0, max(0.0, risk))

        # Raw Trust Score [0 - 100]
        raw_trust = 100.0 * (1.0 - risk)

        # Historical Trust Smoothing
        smoothed_trust = (self.alpha * previous_trust) + ((1.0 - self.alpha) * raw_trust)

        # Immediate High-Severity Security Overrides
        # A critical unauthorized command or replay must NOT remain trusted just because past trust was high!
        override_triggered = False
        if unauth_anomaly >= 0.5:
            override_triggered = True
            smoothed_trust = min(35.0, smoothed_trust - 50.0)
            reasons.append("CRITICAL OVERRIDE: Unauthorized topic access detected! Trust suppressed immediately regardless of historical score.")
        elif auth_fail_anomaly >= 0.6:
            override_triggered = True
            smoothed_trust = min(40.0, smoothed_trust - 40.0)
            reasons.append("CRITICAL OVERRIDE: Multiple authentication failures detected! Trust suppressed immediately.")
        elif replay_anomaly >= 0.5:
            override_triggered = True
            smoothed_trust = min(30.0, smoothed_trust - 55.0)
            reasons.append("CRITICAL OVERRIDE: Message replay attack detected! Nonce/Sequence mismatch.")

        if not reasons:
            if smoothed_trust >= 85.0:
                reasons.append("Device behavior matches normal baseline telemetry; no security violations detected.")
            else:
                reasons.append(f"Minor behavioral variance detected (raw risk score: {round(risk, 2)}).")

        final_trust = round(max(0.0, min(100.0, smoothed_trust)), 1)
        reason_str = " | ".join(reasons)

        breakdown = {
            "rate_anomaly": round(rate_anomaly, 3),
            "effective_rate_anomaly": round(effective_rate_anomaly, 3),
            "unauth_anomaly": round(unauth_anomaly, 3),
            "auth_fail_anomaly": round(auth_fail_anomaly, 3),
            "payload_anomaly": round(payload_anomaly, 3),
            "conn_anomaly": round(conn_anomaly, 3),
            "effective_conn_anomaly": round(effective_conn_anomaly, 3),
            "raw_risk": round(risk, 3),
            "raw_trust": round(raw_trust, 1),
            "previous_trust": round(previous_trust, 1),
            "smoothed_trust": final_trust,
            "network_discount_applied": network_discount > 0,
            "override_triggered": override_triggered
        }

        result = {
            "device_id": device_id,
            "raw_risk": round(risk, 3),
            "calculated_trust": round(raw_trust, 1),
            "previous_trust": round(previous_trust, 1),
            "smoothed_trust": final_trust,
            "confidence_score": round(confidence_score, 2),
            "network_context_discount": network_discount,
            "breakdown": breakdown,
            "reason": reason_str
        }

        # Save to database
        self.db.log_trust_evaluation(result)
        return result

