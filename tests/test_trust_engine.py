"""
Unit Tests for Trust Evaluation Engine.
"""
from database.db_manager import DatabaseManager
from core.trust_engine import TrustEvaluationEngine

def test_trust_calculation_normal(tmp_path):
    db_file = tmp_path / "test_trust.db"
    db = DatabaseManager(db_file)
    engine = TrustEvaluationEngine(db)

    behavior = {
        "rate_anomaly": 0.0,
        "unauth_anomaly": 0.0,
        "auth_fail_anomaly": 0.0,
        "payload_anomaly": 0.0,
        "conn_anomaly": 0.0,
        "replay_anomaly": 0.0
    }
    net_metric = {"is_congested": False, "avg_latency_ms": 15.0}

    res = engine.evaluate_device_trust(
        device_id="test_dev_01",
        behavior=behavior,
        network_metric=net_metric,
        confidence_score=0.90,
        previous_trust=95.0
    )

    assert res["smoothed_trust"] >= 90.0
    assert res["raw_risk"] == 0.0

def test_network_context_discounting(tmp_path):
    db_file = tmp_path / "test_trust_net.db"
    db = DatabaseManager(db_file)
    engine = TrustEvaluationEngine(db)

    # Device experiences high rate/delay anomaly
    behavior = {
        "rate_anomaly": 0.8,
        "unauth_anomaly": 0.0,
        "auth_fail_anomaly": 0.0,
        "payload_anomaly": 0.0,
        "conn_anomaly": 0.6,
        "replay_anomaly": 0.0
    }
    # Congested network
    net_congested = {
        "is_congested": True,
        "avg_latency_ms": 185.0,
        "affected_devices_count": 4
    }

    # Evaluate WITH network context awareness
    res_context = engine.evaluate_device_trust(
        device_id="test_dev_01",
        behavior=behavior,
        network_metric=net_congested,
        confidence_score=0.85,
        previous_trust=90.0,
        enable_network_context=True
    )

    # Evaluate WITHOUT network context awareness
    res_no_context = engine.evaluate_device_trust(
        device_id="test_dev_01",
        behavior=behavior,
        network_metric=net_congested,
        confidence_score=0.85,
        previous_trust=90.0,
        enable_network_context=False
    )

    # Network context awareness should preserve trust better (higher trust score)
    assert res_context["smoothed_trust"] > res_no_context["smoothed_trust"]
    assert res_context["network_context_discount"] > 0.0

def test_immediate_security_override(tmp_path):
    db_file = tmp_path / "test_override.db"
    db = DatabaseManager(db_file)
    engine = TrustEvaluationEngine(db)

    # Critical unauthorized access attempt
    behavior = {
        "rate_anomaly": 0.0,
        "unauth_anomaly": 1.0, # CRITICAL VIOLATION
        "auth_fail_anomaly": 0.0,
        "payload_anomaly": 0.0,
        "conn_anomaly": 0.0,
        "replay_anomaly": 0.0
    }
    net_metric = {"is_congested": False, "avg_latency_ms": 15.0}

    # Even with high previous trust of 99.0
    res = engine.evaluate_device_trust(
        device_id="test_dev_01",
        behavior=behavior,
        network_metric=net_metric,
        confidence_score=0.90,
        previous_trust=99.0
    )

    # Must be immediately dropped
    assert res["smoothed_trust"] <= 35.0
    assert res["breakdown"]["override_triggered"] is True

