"""
Unit and Integration Tests for Simulation Engine and Virtual IoT Broker.
"""
from database.db_manager import DatabaseManager
from simulator.simulation_engine import SimulationEngine

def test_simulation_step_and_broker(tmp_path):
    db_file = tmp_path / "test_sim.db"
    db = DatabaseManager(db_file)
    engine = SimulationEngine(db)

    # 1. Execute multiple simulation steps
    for _ in range(5):
        engine.step_cycle()

    # 2. Verify that network metrics and behavior records were generated
    net_metrics = db.get_latest_network_metrics(limit=5)
    assert len(net_metrics) > 0

    # 3. Test Attack scenario triggering
    engine.attack_simulator.start_scenario("FLOODING", target_device="temperature_sensor_01", duration_sec=5.0)
    assert engine.devices["temperature_sensor_01"].mode == "FLOODING"

    # Step simulation with flooding
    for _ in range(4):
        engine.step_cycle()

    # Verify high throughput logged
    assert engine.broker.total_published > 10

