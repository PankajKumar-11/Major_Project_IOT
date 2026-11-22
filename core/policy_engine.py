"""
Zero Trust Policy Engine for IoT Networks.
Computes dynamic access decisions: ALLOW, RESTRICT, CHALLENGE, DENY
based on continuous trust score, empirical confidence, resource sensitivity, and network context.
"""
import logging
from typing import Dict, Any, Tuple
from config import DEFAULT_THRESHOLDS, SENSITIVE_TOPICS

logger = logging.getLogger("PolicyEngine")

class PolicyDecision:
    ALLOW = "ALLOW"
    RESTRICT = "RESTRICT"
    CHALLENGE = "CHALLENGE"
    DENY = "DENY"

class ZeroTrustPolicyEngine:
    def __init__(self, thresholds: Dict[str, float] = None):
        self.thresholds = thresholds or dict(DEFAULT_THRESHOLDS)

    def set_thresholds(self, new_thresholds: Dict[str, float]):
        self.thresholds.update(new_thresholds)
        logger.info(f"Updated policy thresholds: {self.thresholds}")

    def evaluate_policy(
        self,
        device_id: str,
        trust_score: float,
        confidence_score: float,
        behavior: Dict[str, Any],
        sensitivity: str = "LOW"
    ) -> Tuple[str, str, str]:
        """
        Determines access control decision:
        Returns: (decision: str, risk_level: str, explanation: str)
        """
        t_allow = self.thresholds.get("allow_trust", 80.0)
        t_restrict = self.thresholds.get("restrict_trust", 50.0)
        min_conf = self.thresholds.get("min_confidence_for_allow", 0.60)
        challenge_conf = self.thresholds.get("challenge_confidence_threshold", 0.40)

        unauth_anomaly = behavior.get("unauth_anomaly", 0.0)
        auth_fail_anomaly = behavior.get("auth_fail_anomaly", 0.0)
        replay_anomaly = behavior.get("replay_anomaly", 0.0)

        # 1. Critical High-Severity Rule: Immediate DENY
        # Unauthorized topic access, severe brute force, or replay attacks must be blocked immediately
        if unauth_anomaly >= 0.5:
            return (
                PolicyDecision.DENY,
                "HIGH",
                "CRITICAL SECURITY VIOLATION: Unauthorized topic access attempt detected. Access revoked."
            )
        if auth_fail_anomaly >= 0.6:
            return (
                PolicyDecision.DENY,
                "HIGH",
                "CRITICAL SECURITY VIOLATION: Repeated authentication credential failures. Device quarantined."
            )
        if replay_anomaly >= 0.5:
            return (
                PolicyDecision.DENY,
                "HIGH",
                "CRITICAL SECURITY VIOLATION: Replay attack with duplicate nonce detected. Access blocked."
            )

        # 2. Risk Level Assignment
        if trust_score >= t_allow:
            risk_level = "LOW"
        elif trust_score >= t_restrict:
            risk_level = "MEDIUM"
        else:
            risk_level = "HIGH"

        # 3. Confidence-Aware Decision Logic
        # If confidence is too low (< 0.40), avoid hasty isolation unless trust is already disastrous
        if confidence_score < challenge_conf and trust_score >= t_restrict:
            return (
                PolicyDecision.CHALLENGE,
                risk_level,
                f"Insufficient observation evidence (Confidence: {confidence_score} < {challenge_conf}). "
                "Issuing cryptographic challenge to verify device integrity without premature isolation."
            )

        # 4. Standard Zero Trust Decision Thresholds
        if trust_score >= t_allow and confidence_score >= min_conf:
            return (
                PolicyDecision.ALLOW,
                "LOW",
                f"High trust ({trust_score}) and verified confidence ({confidence_score}). Full authorized access granted."
            )
        elif trust_score >= t_restrict:
            # RESTRICT sensitive operations
            return (
                PolicyDecision.RESTRICT,
                "MEDIUM",
                f"Moderate trust ({trust_score}). Access restricted: critical control topics and sensitive actuators isolated."
            )
        else:
            # Low trust with sufficient confidence
            return (
                PolicyDecision.DENY,
                "HIGH",
                f"Low trust score ({trust_score} < {t_restrict}) backed by sufficient evidence ({confidence_score}). Access revoked."
            )

