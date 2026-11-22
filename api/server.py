"""
FastAPI REST API Server for Zero Trust IoT Framework.
Exposes control, telemetry, security audit, and evaluation endpoints.
Ensures that the Streamlit frontend acts purely as a presentation layer.
"""
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from fastapi import FastAPI, HTTPException, Query, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
import logging

from database.db_manager import DatabaseManager
from simulator.simulation_engine import SimulationEngine
from evaluation.experiment_runner import ExperimentRunner

logger = logging.getLogger("API")

app = FastAPI(
    title="Behaviour-Aware Zero Trust IoT Security Framework API",
    description="Research-Oriented Continuous Trust Evaluation & Adaptive Access Control for IoT Networks",
    version="1.0.0"
)

# Shared instances
db = DatabaseManager()
engine = SimulationEngine(db)
eval_runner = ExperimentRunner(db)

# Auto-start simulation engine on startup
@app.on_event("startup")
def startup_event():
    engine.start()
    logger.info("FastAPI: Simulation engine background service activated.")

@app.on_event("shutdown")
def shutdown_event():
    engine.stop()
    logger.info("FastAPI: Simulation engine background service deactivated.")

# --- Pydantic Request Models ---
class ScenarioRequest(BaseModel):
    scenario_key: str = Field(..., description="NORMAL, FLOODING, COMPROMISED, UNAUTHORIZED, AUTH_FAIL, REPLAY, CONGESTION, LOW_SLOW")
    target_device: str = Field("temperature_sensor_01", description="Device ID to target")
    duration_sec: float = Field(30.0, ge=5.0, le=300.0)

class WeightsRequest(BaseModel):
    weights: Dict[str, float]

class ThresholdsRequest(BaseModel):
    thresholds: Dict[str, float]

# --- REST Endpoints ---
@app.get("/api/health")
def health_check():
    return {"status": "HEALTHY", "service": "ZeroTrust IoT Security Engine"}

@app.get("/api/overview")
def get_fleet_overview():
    devices = db.get_all_devices()
    total = len(devices)
    active = sum(1 for d in devices if d.get("auth_status") == "AUTHENTICATED")
    trusted = sum(1 for d in devices if d.get("current_trust", 0) >= 80.0)
    restricted = sum(1 for d in devices if d.get("access_policy") == "RESTRICT")
    revoked = sum(1 for d in devices if d.get("access_policy") == "DENY")
    challenges = sum(1 for d in devices if d.get("access_policy") == "CHALLENGE")
    
    events = db.get_recent_security_events(limit=10)
    net_history = db.get_latest_network_metrics(limit=1)
    current_net = net_history[0] if net_history else {}

    return {
        "total_devices": total,
        "active_devices": active,
        "trusted_devices": trusted,
        "restricted_devices": restricted,
        "revoked_devices": revoked,
        "challenge_devices": challenges,
        "total_security_events": len(events),
        "network_congested": bool(current_net.get("is_congested", False)),
        "current_latency_ms": current_net.get("avg_latency_ms", 15.0),
        "recent_events": events[:5]
    }

@app.get("/api/devices")
def list_devices():
    return db.get_all_devices()

@app.get("/api/devices/{device_id}")
def get_device_details(device_id: str):
    dev = db.get_device(device_id)
    if not dev:
        raise HTTPException(status_code=404, detail="Device not found")
    trust_history = db.get_device_trust_history(device_id, limit=30)
    return {
        "device": dev,
        "trust_history": trust_history
    }

@app.get("/api/network/status")
def get_network_status(limit: int = Query(30, ge=5, le=100)):
    return {
        "history": db.get_latest_network_metrics(limit=limit),
        "is_congested": engine.network_monitor.manual_congestion_active
    }

@app.get("/api/security/events")
def get_security_events(limit: int = Query(50, ge=5, le=200)):
    return db.get_recent_security_events(limit=limit)

@app.post("/api/simulation/scenario")
def trigger_scenario(req: ScenarioRequest):
    try:
        engine.attack_simulator.start_scenario(
            scenario_key=req.scenario_key,
            target_device=req.target_device,
            duration_sec=req.duration_sec
        )
        return {
            "status": "SUCCESS",
            "message": f"Scenario {req.scenario_key} initiated on {req.target_device}",
            "details": engine.attack_simulator.get_status()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/simulation/status")
def get_simulation_status():
    return engine.attack_simulator.get_status()

@app.post("/api/simulation/reset")
def reset_simulation():
    engine.attack_simulator.start_scenario("NORMAL")
    db.reset_all_data()
    return {"status": "SUCCESS", "message": "Simulation and database records reset to baseline."}

@app.post("/api/evaluation/run")
def run_evaluation_experiments(background_tasks: BackgroundTasks):
    df_comp = eval_runner.run_full_comparative_benchmark()
    df_abl = eval_runner.run_ablation_study()
    return {
        "status": "SUCCESS",
        "comparative_benchmark": df_comp.to_dict(orient="records"),
        "ablation_study": df_abl.to_dict(orient="records")
    }

@app.get("/api/evaluation/results")
def get_evaluation_results():
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM experiment_results ORDER BY id DESC LIMIT 20;")
        rows = [dict(r) for r in cursor.fetchall()]
        return rows

@app.post("/api/trust/weights")
def update_trust_weights(req: WeightsRequest):
    try:
        engine.trust_engine.set_weights(req.weights)
        return {"status": "SUCCESS", "weights": engine.trust_engine.weights}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/policy/thresholds")
def update_policy_thresholds(req: ThresholdsRequest):
    engine.policy_engine.set_thresholds(req.thresholds)
    return {"status": "SUCCESS", "thresholds": engine.policy_engine.thresholds}

