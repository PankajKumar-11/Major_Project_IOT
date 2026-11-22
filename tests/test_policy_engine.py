"""
Unit Tests for Zero Trust Policy Engine.
"""
from core.policy_engine import ZeroTrustPolicyEngine, PolicyDecision

def test_policy_decisions():
    pe = ZeroTrustPolicyEngine()

    # 1. High trust & high confidence -> ALLOW
    decision, risk, _ = pe.evaluate_policy("dev_01", trust_score=92.0, confidence_score=0.85, behavior={})
    assert decision == PolicyDecision.ALLOW
    assert risk == "LOW"

    # 2. Medium trust -> RESTRICT
    decision, risk, _ = pe.evaluate_policy("dev_01", trust_score=68.0, confidence_score=0.80, behavior={})
    assert decision == PolicyDecision.RESTRICT
    assert risk == "MEDIUM"

    # 3. Low trust -> DENY
    decision, risk, _ = pe.evaluate_policy("dev_01", trust_score=35.0, confidence_score=0.75, behavior={})
    assert decision == PolicyDecision.DENY
    assert risk == "HIGH"

    # 4. Low confidence with borderline trust -> CHALLENGE
    decision, risk, _ = pe.evaluate_policy("dev_01", trust_score=75.0, confidence_score=0.25, behavior={})
    assert decision == PolicyDecision.CHALLENGE

    # 5. Critical unauthorized anomaly -> Immediate DENY
    decision, risk, _ = pe.evaluate_policy("dev_01", trust_score=95.0, confidence_score=0.90, behavior={"unauth_anomaly": 0.8})
    assert decision == PolicyDecision.DENY

