"""
Unit Tests for Network Monitoring & Congestion Context.
"""
from database.db_manager import DatabaseManager
from core.network_monitor import NetworkMonitor

def test_network_monitoring_and_congestion(tmp_path):
    db_file = tmp_path / "test_net.db"
    db = DatabaseManager(db_file)
    net_mon = NetworkMonitor(db)

    # 1. Normal network state
    snapshot = net_mon.collect_network_snapshot(broker_delay_ms=1.1, throughput_msg_sec=12.5)
    assert not snapshot["is_congested"]
    assert snapshot["avg_latency_ms"] < 50.0

    # 2. Simulate congestion
    net_mon.set_congestion_simulation(True, intensity=0.9)
    congested_snapshot = net_mon.collect_network_snapshot(broker_delay_ms=15.0, throughput_msg_sec=4.0)
    assert congested_snapshot["is_congested"]
    assert congested_snapshot["avg_latency_ms"] >= 150.0
    assert net_mon.get_network_context_discount() > 0.5

