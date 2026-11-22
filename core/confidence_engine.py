"""
Confidence Evaluation Engine for Behaviour-Aware Zero Trust Framework.
Measures the quality, stability, and quantity of available empirical evidence.
Academic notice: This confidence score is an empirical measure of evidence sufficiency,
not a calibrated Bayesian probability of device safety.
"""
import numpy as np
import logging
from typing import Dict, Any

logger = logging.getLogger("ConfidenceEngine")

class ConfidenceEvaluationEngine:
    def __init__(self, min_sample_size: int = 10, stability_weight: float = 0.4, sample_weight: float = 0.4, consensus_weight: float = 0.2):
        self.min_sample_size = min_sample_size
        self.w_sample = sample_weight
        self.w_stability = stability_weight
        self.w_consensus = consensus_weight

    def evaluate_confidence(self, behavior: Dict[str, Any], network_metric: Dict[str, Any]) -> float:
        """
        Computes Confidence Score in [0.0, 1.0].
        Components:
        1. Sample Size Sufficiency (Observation quantity): ratio of observations to required minimum.
        2. Measurement Stability: inverse of payload/rate variance jitter.
        3. Feature Agreement: whether behavioral indicators align consistently.
        """
        msg_count = behavior.get("msg_count", 0)
        rate_anomaly = behavior.get("rate_anomaly", 0.0)
        unauth_anomaly = behavior.get("unauth_anomaly", 0.0)
        payload_anomaly = behavior.get("payload_anomaly", 0.0)
        conn_anomaly = behavior.get("conn_anomaly", 0.0)

        # 1. Observation Sufficiency Score [0.1, 1.0]
        # At 0 messages, confidence is low (0.15). At min_sample_size (10 msgs), it reaches 1.0.
        c_sample = min(1.0, max(0.15, msg_count / float(self.min_sample_size)))

        # 2. Measurement Stability Score [0.2, 1.0]
        # High jitter in payload standard deviation or rate decreases stability
        payload_std = behavior.get("payload_std", 0.0)
        payload_mean = behavior.get("payload_mean", 64.0)
        cv = payload_std / max(1.0, payload_mean) # coefficient of variation
        c_stability = max(0.2, 1.0 - min(0.8, cv))

        # 3. Indicator Agreement Score [0.3, 1.0]
        # Check standard deviation of anomaly signals.
        signals = [rate_anomaly, unauth_anomaly, payload_anomaly, conn_anomaly]
        signal_std = float(np.std(signals))
        # High disagreement between indicators slightly lowers confidence
        c_consensus = max(0.4, 1.0 - min(0.6, signal_std))

        # Weighted combination
        raw_confidence = (
            self.w_sample * c_sample +
            self.w_stability * c_stability +
            self.w_consensus * c_consensus
        )

        final_confidence = round(max(0.1, min(1.0, raw_confidence)), 2)
        return final_confidence

