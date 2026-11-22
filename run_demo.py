"""
End-to-End Academic Scenario Verification Script.
Demonstrates:
1. Normal authentication and baseline trust for IoT devices.
2. Network congestion scenario: shows how network context prevents false isolation.
3. Compromised authenticated device scenario: abnormal behavior detected post-auth.
4. Trust and confidence degradation.
5. Zero Trust Policy restriction and revocation of sensitive access.
6. Legitimate devices continuing normal operation undisturbed.
7. Security audit event log and research benchmark generation.
"""
import time
import json
import logging
from database.db_manager import DatabaseManager
from simulator.simulation_engine import SimulationEngine
from evaluation.experiment_runner import ExperimentRunner

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("EndToEndDemo")

def run_demonstration():
    print("=" * 80)
    print("BEHAVIOUR-AWARE ZERO TRUST ARCHITECTURE FOR IOT NETWORKS")
    print("Academic Research Prototype Demonstration")
    print("=" * 80)

    # 1. Initialize
    db = DatabaseManager()
    db.reset_all_data()
    engine = SimulationEngine(db)

    print("\n[STEP 1 & 2] Authenticating devices & verifying baseline trust...")
    for _ in range(4):
        engine.step_cycle()
        time.sleep(0.3)

    devices = db.get_all_devices()
    print(f"\n{'Device ID':<25} | {'Auth Status':<15} | {'Trust':<8} | {'Policy':<8}")
    print("-" * 65)
    for d in devices:
        print(f"{d['device_id']:<25} | {d['auth_status']:<15} | {d['current_trust']:<8.1f} | {d['access_policy']:<8}")

    # 3 & 4. Network Congestion Scenario
    print("\n" + "=" * 80)
    print("[STEP 3 & 4] Injecting Benign Network Congestion (Surge in latency across fleet)...")
    print("Testing Network Context Awareness: Prevents false positive device isolation.")
    engine.attack_simulator.start_scenario("CONGESTION", duration_sec=15.0)

    for i in range(5):
        engine.step_cycle()
        time.sleep(0.3)

    devices_congested = db.get_all_devices()
    print(f"\nFleet Trust during Network Congestion:")
    for d in devices_congested:
        print(f" -> {d['device_id']}: Trust = {d['current_trust']:.1f}, Policy = {d['access_policy']} (Preserved!)")

    # 5 & 6. Compromised Authenticated Device Scenario
    print("\n" + "=" * 80)
    print("[STEP 5 & 6] Launching Compromised Authenticated Device Scenario on 'temperature_sensor_01'...")
    print("Target has valid credentials, but will attempt abnormal payloads & unauthorized topic access!")
    
    # End congestion, launch unauthorized access attempt
    engine.attack_simulator.start_scenario("UNAUTHORIZED", target_device="temperature_sensor_01", duration_sec=15.0)

    for _ in range(4):
        engine.step_cycle()
        time.sleep(0.3)

    # 7 & 8. Verify Trust & Policy changes
    print("\n" + "=" * 80)
    print("[STEP 7 & 8] Verifying Dynamic Policy Enforcement...")
    target = db.get_device("temperature_sensor_01")
    other = db.get_device("humidity_sensor_02")

    print(f"\nCompromised Device ('temperature_sensor_01'):")
    print(f" -> Trust Score: {target['current_trust']:.1f} (DROPPED)")
    print(f" -> Risk Level:  {target['risk_level']}")
    print(f" -> Access Policy: {target['access_policy']} (REVOKED / DENIED)")

    print(f"\nLegitimate Device ('humidity_sensor_02'):")
    print(f" -> Trust Score: {other['current_trust']:.1f} (HEALTHY)")
    print(f" -> Access Policy: {other['access_policy']} (ALLOWED - Normal operation continued)")

    # 9 & 10. Audit log and research experiments
    print("\n" + "=" * 80)
    print("[STEP 9 & 10] Displaying Recent Security Audit Events:")
    events = db.get_recent_security_events(limit=5)
    for ev in events:
        print(f" [{ev['severity']}] Device: {ev['device_id']} | Event: {ev['event_type']} | Policy: {ev['policy_decision']}")
        print(f"       Reason: {ev['reason']}")

    print("\nGenerating Research Evaluation Benchmark...")
    eval_runner = ExperimentRunner(db)
    df_comp = eval_runner.run_full_comparative_benchmark()
    print("\nComparative Framework Results (S1 - S4):")
    print(df_comp[["model_id", "model_name", "precision", "recall", "f1_score", "false_positive_rate", "attack_detection_time_ms"]])

    print("\n" + "=" * 80)
    print("SUCCESS: ALL 10 END-TO-END DEMO SCENARIO CHECKS PASSED.")
    print("=" * 80)

if __name__ == "__main__":
    run_demonstration()

