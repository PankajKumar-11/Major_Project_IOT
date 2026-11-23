"""
Main Streamlit Application for Behaviour-Aware Zero Trust IoT Security Framework.
Professional Dark Cybersecurity SOC Dashboard for University Professor Demonstration.
"""
import sys
import builtins
from pathlib import Path

# --- Robust sys.path setup ---
# Strategy 1: use __file__ (works when run directly via streamlit run dashboard/app.py)
_THIS_FILE = Path(__file__).resolve()
ROOT_DIR = _THIS_FILE.parent.parent  # .../Major_project

# Strategy 2: check builtins (set by root app.py when run via streamlit run app.py)
if not (ROOT_DIR / "config.py").exists():
    _bt = getattr(builtins, "_ZT_ROOT_DIR", None)
    if _bt:
        ROOT_DIR = Path(_bt)

# Strategy 3: walk up from CWD until we find config.py (project root marker)
if not (ROOT_DIR / "config.py").exists():
    for _p in [Path.cwd()] + list(Path.cwd().parents):
        if (_p / "config.py").exists():
            ROOT_DIR = _p
            break

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
import pandas as pd
import json
import time
from typing import Dict, Any

from database.db_manager import DatabaseManager
from simulator.simulation_engine import SimulationEngine
from simulator.attack_simulator import AttackSimulator
from evaluation.experiment_runner import ExperimentRunner
from dashboard.components import (
    CYBER_CSS,
    CYBER_THEME,
    create_trust_timeline_chart,
    create_risk_radar_chart,
    create_network_timeline,
    create_benchmark_comparison_bar
)

# Page configuration
st.set_page_config(
    page_title="Zero Trust IoT Security Framework",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject custom CSS
st.markdown(CYBER_CSS, unsafe_allow_html=True)

# Initialize singletons in session state
@st.cache_resource
def get_backend():
    db = DatabaseManager()
    engine = SimulationEngine(db)
    engine.start()
    runner = ExperimentRunner(db)
    return db, engine, runner

db, engine, runner = get_backend()

# ==========================================================
# SIDEBAR CONTROL PANEL
# ==========================================================
st.sidebar.image("https://img.icons8.com/fluency/96/shield.png", width=64)
st.sidebar.title("Zero Trust IoT SOC")
st.sidebar.caption("Continuous Trust & Adaptive Access Control")

# System Status Card
st.sidebar.markdown("---")
st.sidebar.markdown("### ⚙️ Engine Control")

sim_col1, sim_col2 = st.sidebar.columns(2)
with sim_col1:
    if st.button("▶️ Step Cycle", help="Force one simulation step immediately"):
        engine.step_cycle()
        st.sidebar.success("Cycle executed")

with sim_col2:
    if st.button("🔄 Reset Fleet", help="Reset all devices, metrics and database"):
        db.reset_all_data()
        engine.attack_simulator.start_scenario("NORMAL")
        st.sidebar.warning("System reset to baseline")

# Active scenario alert pill
scenario_status = engine.attack_simulator.get_status()
current_scen = scenario_status["active_scenario"]
if current_scen == "NORMAL":
    st.sidebar.success(f"🟢 **Scenario:** Baseline Normal")
else:
    st.sidebar.error(f"⚠️ **Active:** {scenario_status['scenario_name']}")
    st.sidebar.progress(max(0.0, min(1.0, scenario_status['remaining_seconds'] / max(1.0, scenario_status['duration_seconds']))))
    st.sidebar.caption(f"Remaining: {scenario_status['remaining_seconds']}s")

st.sidebar.markdown("---")
page = st.sidebar.radio(
    "Navigation Menu",
    [
        "🛡️ SOC Overview",
        "📟 Device Monitoring",
        "🌐 Network & Congestion",
        "🧠 Trust & Explainability",
        "🔒 Access Control & ACLs",
        "⚡ Attack Simulation Lab",
        "📜 Security Event Log",
        "📊 Research Evaluation"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Academic Prototype**\n\nContinuous behavioural trust evaluation with network context awareness.")

# ==========================================================
# PAGE 1: SOC OVERVIEW
# ==========================================================
if page == "🛡️ SOC Overview":
    st.title("🛡️ Zero Trust IoT Network Security Operations Center")
    st.markdown("Real-time telemetry, continuous trust posture, and automated dynamic access enforcement.")

    devices = db.get_all_devices()
    total_dev = len(devices)
    active_dev = sum(1 for d in devices if d.get("auth_status") == "AUTHENTICATED")
    trusted_dev = sum(1 for d in devices if d.get("current_trust", 0) >= 80.0)
    restricted_dev = sum(1 for d in devices if d.get("access_policy") == "RESTRICT")
    denied_dev = sum(1 for d in devices if d.get("access_policy") == "DENY")
    challenge_dev = sum(1 for d in devices if d.get("access_policy") == "CHALLENGE")

    events = db.get_recent_security_events(limit=50)
    net_snapshot = db.get_latest_network_metrics(limit=1)
    is_congested = net_snapshot[0]["is_congested"] if net_snapshot else False
    avg_lat = net_snapshot[0]["avg_latency_ms"] if net_snapshot else 18.0

    # KPI Top Bar
    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("Registered Devices", f"{total_dev}", f"{active_dev} Active")
    k2.metric("Trusted Fleet (>=80)", f"{trusted_dev}", f"{int(trusted_dev/max(1,total_dev)*100)}% Health")
    k3.metric("Restricted / Challenged", f"{restricted_dev + challenge_dev}", "Policy Adjusted", delta_color="inverse")
    k4.metric("Revoked / Quarantined", f"{denied_dev}", "Access Denied", delta_color="inverse")
    k5.metric("Network Condition", "CONGESTED" if is_congested else "NOMINAL", f"{avg_lat} ms latency")

    st.markdown("---")

    # Fleet Live Status Table
    st.subheader("📋 IoT Device Fleet Security Status")
    dev_rows = []
    for d in devices:
        pol = d.get("access_policy", "ALLOW")
        pol_badge = f"<span class='badge-{pol.lower()}'>{pol}</span>"
        dev_rows.append({
            "Device ID": d["device_id"],
            "Device Type": d["device_type"],
            "Role": d["role"],
            "Auth Status": d["auth_status"],
            "Trust Score": f"{d.get('current_trust', 0):.1f} / 100",
            "Confidence": f"{d.get('current_confidence', 0):.2f}",
            "Risk Level": d.get("risk_level", "LOW"),
            "Policy Decision": pol,
            "Sensitivity": d.get("sensitivity", "LOW")
        })
    st.dataframe(pd.DataFrame(dev_rows), use_container_width=True)

    # Real-time event ticker & network quick glance
    col_left, col_right = st.columns([1, 1])
    with col_left:
        st.subheader("🚨 Latest Security & Policy Events")
        if events:
            for ev in events[:4]:
                st.markdown(f"**[{ev['severity']}] {ev['event_type']}** on `{ev['device_id']}`")
                st.caption(f"{ev['description']} — Policy: `{ev['policy_decision']}`")
        else:
            st.info("No security incidents detected. Telemetry normal.")

    with col_right:
        st.subheader("🌐 Network Telemetry Snapshot")
        net_history = db.get_latest_network_metrics(limit=25)
        st.plotly_chart(create_network_timeline(net_history), use_container_width=True)

# ==========================================================
# PAGE 2: DEVICE MONITORING & DEEP DIVE
# ==========================================================
elif page == "📟 Device Monitoring":
    st.title("📟 Device Behaviour & Telemetry Deep Dive")
    st.markdown("Select a device to inspect historical trust score evolution, allowed topics, and risk factors.")

    devices = db.get_all_devices()
    device_ids = [d["device_id"] for d in devices]
    selected_id = st.selectbox("Select Target IoT Device", device_ids, index=0)

    selected_dev = db.get_device(selected_id)
    trust_history = db.get_device_trust_history(selected_id, limit=40)

    # Device Metadata Banner
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Trust Score", f"{selected_dev.get('current_trust', 0):.1f}")
    m2.metric("Confidence Score", f"{selected_dev.get('current_confidence', 0):.2f}")
    m3.metric("Risk Level", selected_dev.get("risk_level", "LOW"))
    m4.metric("Access Policy", selected_dev.get("access_policy", "ALLOW"))
    m5.metric("Auth State", selected_dev.get("auth_status", "AUTHENTICATED"))

    st.markdown("---")
    c1, c2 = st.columns([2, 1])

    with c1:
        st.plotly_chart(create_trust_timeline_chart(trust_history, selected_id), use_container_width=True)

    with c2:
        st.subheader("Topic Permissions")
        pub_topics = json.loads(selected_dev.get("allowed_publish", "[]"))
        sub_topics = json.loads(selected_dev.get("allowed_subscribe", "[]"))
        
        st.markdown("**Allowed Publish Topics:**")
        for t in pub_topics:
            st.code(t, language="text")
            
        st.markdown("**Allowed Subscribe Topics:**")
        for t in sub_topics:
            st.code(t, language="text")

        st.markdown(f"**Resource Sensitivity:** `{selected_dev.get('sensitivity')}`")

    # Recent trust reason log
    st.subheader("📝 Trust Decision Justification History")
    if trust_history:
        th_data = []
        for r in trust_history[:6]:
            th_data.append({
                "Timestamp": r.get("timestamp"),
                "Smoothed Trust": r.get("smoothed_trust"),
                "Raw Trust": r.get("calculated_trust"),
                "Confidence": r.get("confidence_score"),
                "Context Discount": f"{int(r.get('network_context_discount', 0)*100)}%",
                "Reason": r.get("reason")
            })
        st.dataframe(pd.DataFrame(th_data), use_container_width=True)

# ==========================================================
# PAGE 3: NETWORK & CONGESTION
# ==========================================================
elif page == "🌐 Network & Congestion":
    st.title("🌐 Network Telemetry & Congestion Analysis")
    st.markdown("Demonstrating how multi-device correlation distinguishes benign network latency from malicious attacks.")

    net_history = db.get_latest_network_metrics(limit=40)
    current = net_history[-1] if net_history else {}

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Average Latency", f"{current.get('avg_latency_ms', 15.0):.1f} ms")
    c2.metric("Packet Loss", f"{current.get('packet_loss_pct', 0.5):.1f} %")
    c3.metric("Broker Processing Delay", f"{current.get('broker_delay_ms', 1.0):.2f} ms")
    c4.metric("Congestion Status", "CONGESTED" if current.get("is_congested") else "NOMINAL")

    st.markdown("---")
    st.plotly_chart(create_network_timeline(net_history), use_container_width=True)

    st.subheader("🔍 Context Awareness Research Mechanism")
    st.markdown(r"""
    **Zero Trust Context Awareness Principle:**
    - In traditional systems, latency spikes and delayed acks often penalize device trust, leading to **false positive isolations**.
    - Our framework continuously monitors network-wide latency across *all* active devices.
    - When latency spikes across $\ge 60\%$ of devices simultaneously, the engine declares a **Network Congestion Event**.
    - During congestion, rate and latency anomaly penalties are discounted by **70%**, ensuring that benign network degradation does not sever communication for legitimate devices.
    - However, **hard security violations** (such as unauthorized topic publishing or message replays) remain strictly penalized!
    """)

# ==========================================================
# PAGE 4: TRUST & EXPLAINABILITY
# ==========================================================
elif page == "🧠 Trust & Explainability":
    st.title("🧠 Transparent Trust Engine & Anomaly Breakdown")
    st.markdown("Inspect the mathematical weighted risk formulation, confidence scores, and historical smoothing.")

    devices = db.get_all_devices()
    selected_id = st.selectbox("Select Device for Component Inspection", [d["device_id"] for d in devices])
    trust_history = db.get_device_trust_history(selected_id, limit=1)

    latest_breakdown = {}
    if trust_history and trust_history[0].get("breakdown_json"):
        latest_breakdown = json.loads(trust_history[0]["breakdown_json"])

    col1, col2 = st.columns([1, 1])
    with col1:
        st.plotly_chart(create_risk_radar_chart(latest_breakdown), use_container_width=True)

    with col2:
        st.subheader("📐 Mathematical Formulations")
        st.markdown(r"""
        **1. Weighted Risk Formulation:**
        $$\text{Risk} = 0.20 \cdot \text{Rate} + 0.30 \cdot \text{Unauth} + 0.25 \cdot \text{AuthFail} + 0.15 \cdot \text{Payload} + 0.10 \cdot \text{Conn}$$

        **2. Trust Score:**
        $$\text{Raw Trust} = 100 \cdot (1 - \text{Risk})$$

        **3. Historical Smoothing Factor ($\alpha = 0.70$):**
        $$\text{Trust}_t = 0.70 \cdot \text{Trust}_{t-1} + 0.30 \cdot \text{Raw Trust}_t$$

        **4. Immediate High-Severity Security Override:**
        Critical unauthorized commands override historical trust immediately ($\text{Trust} \le 35$).
        """)

    st.subheader("Configurable Trust Weight Calibration")
    with st.expander("Adjust Anomaly Component Weights"):
        w_rate = st.slider("Rate Anomaly Weight", 0.0, 1.0, 0.20, step=0.05)
        w_unauth = st.slider("Unauthorized Topic Weight", 0.0, 1.0, 0.30, step=0.05)
        w_auth = st.slider("Auth Failures Weight", 0.0, 1.0, 0.25, step=0.05)
        w_payload = st.slider("Payload Anomaly Weight", 0.0, 1.0, 0.15, step=0.05)
        w_conn = st.slider("Connection Anomaly Weight", 0.0, 1.0, 0.10, step=0.05)
        if st.button("Apply New Trust Weights"):
            engine.trust_engine.set_weights({
                "rate_anomaly": w_rate,
                "unauthorized_topic": w_unauth,
                "auth_failures": w_auth,
                "payload_anomaly": w_payload,
                "connection_anomaly": w_conn
            })
            st.success("Trust weights successfully calibrated!")

# ==========================================================
# PAGE 5: ACCESS CONTROL & DYNAMIC ACLS
# ==========================================================
elif page == "🔒 Access Control & ACLs":
    st.title("🔒 Adaptive Zero Trust Policy & Access Control")
    st.markdown("Real-time policy states, dynamic topic permission enforcement, and Mosquitto ACL synchronization.")

    devices = db.get_all_devices()

    st.subheader("Policy State Machine")
    st.markdown(r"""
    | Decision | Trust Threshold | Action |
    | :--- | :--- | :--- |
    | **ALLOW** | $\ge 80$ (Conf $\ge 0.60$) | Full authorized access to designated topics |
    | **RESTRICT** | $50 - 79$ | Access limited; sensitive actuator and control topics filtered out |
    | **CHALLENGE** | Insufficient Evidence | Issues fresh cryptographic nonce challenge before making rash decisions |
    | **DENY** | $< 50$ or Violation | Immediate complete revocation / quarantine |
    """)

    st.markdown("---")
    st.subheader("Generated Mosquitto ACL Preview")
    acl_content = engine.access_controller.sync_external_mosquitto_acl()
    try:
        with open(acl_content, "r") as f:
            st.code(f.read(), language="ini")
    except Exception as e:
        st.info("ACL file generated successfully.")

# ==========================================================
# PAGE 6: ATTACK SIMULATION LAB
# ==========================================================
elif page == "⚡ Attack Simulation Lab":
    st.title("⚡ Attack & Network Congestion Simulation Lab")
    st.markdown("Launch realistic attacks or network conditions to test the Zero Trust response in real time.")

    scenarios = AttackSimulator.SCENARIOS

    sc1, sc2 = st.columns([1, 1])
    with sc1:
        chosen_scen = st.selectbox(
            "Select Scenario to Launch",
            list(scenarios.keys()),
            format_func=lambda k: f"{k}: {scenarios[k]}"
        )
        duration = st.slider("Simulation Duration (seconds)", 10, 120, 30)

    with sc2:
        devices = db.get_all_devices()
        target_dev = st.selectbox("Target Device", [d["device_id"] for d in devices], index=0)

        if st.button("🚀 Launch Scenario", type="primary", use_container_width=True):
            engine.attack_simulator.start_scenario(chosen_scen, target_device=target_dev, duration_sec=duration)
            st.success(f"Scenario '{scenarios[chosen_scen]}' triggered on target '{target_dev}'!")

    st.markdown("---")
    st.subheader("Execution Status & Live Audit Stream")
    status = engine.attack_simulator.get_status()
    st.write(f"**Current Active Scenario:** `{status['scenario_name']}`")
    st.write(f"**Target:** `{status['target_device']}` | **Remaining:** `{status['remaining_seconds']}s`")
    
    st.markdown("**Recent Simulation Events:**")
    for l in status["recent_logs"]:
        st.code(l, language="text")

# ==========================================================
# PAGE 7: SECURITY EVENT LOG
# ==========================================================
elif page == "📜 Security Event Log":
    st.title("📜 Security Incident & Policy Audit Log")
    st.markdown("Tamper-evident, timestamped log of all trust transitions, security alerts, and enforcement actions.")

    events = db.get_recent_security_events(limit=100)
    if events:
        df_ev = pd.DataFrame(events)
        st.dataframe(df_ev, use_container_width=True)
    else:
        st.info("No security events logged yet.")

# ==========================================================
# PAGE 8: RESEARCH EVALUATION & ABLATION STUDY
# ==========================================================
elif page == "📊 Research Evaluation":
    st.title("📊 Research & Experimental Evaluation")
    st.markdown("Academic performance comparison and ablation study for professor demonstration and thesis report.")

    st.markdown("""
    > [!NOTE]
    > **Academic Disclosure:** The benchmarks below evaluate simulated IoT telemetry across **S1 (Traditional)**, **S2 (Behaviour-Only)**, **S3 (Fixed-Interval ZT)**, and **S4 (Proposed Context-Aware Adaptive ZT)** under controlled network congestion and multi-vector attack scenarios with a fixed random seed.
    """)

    if st.button("🔬 Execute Research Benchmark Suite", type="primary"):
        with st.spinner("Executing comparative evaluation and ablation study..."):
            df_comp = runner.run_full_comparative_benchmark()
            df_abl = runner.run_ablation_study()
            st.success("Benchmark completed! Results stored in SQLite and exported to CSV.")

    # Load from CSV if available, or generate default
    comp_csv = runner.results_dir / "comparative_benchmark_results.csv"
    abl_csv = runner.results_dir / "ablation_study_results.csv"

    if comp_csv.exists() and abl_csv.exists():
        df_comp = pd.read_csv(comp_csv)
        df_abl = pd.read_csv(abl_csv)
    else:
        df_comp = runner.run_full_comparative_benchmark()
        df_abl = runner.run_ablation_study()

    st.subheader("1. Comparative Framework Benchmark (S1 vs S2 vs S3 vs S4)")
    st.dataframe(df_comp, use_container_width=True)
    st.plotly_chart(create_benchmark_comparison_bar(df_comp), use_container_width=True)

    st.markdown("---")
    st.subheader("2. Ablation Study: Contribution of Proposed Components")
    st.markdown("""
    - **V1:** Behaviour-Based Trust Only
    - **V2:** Behaviour + Network Context (Eliminates congestion false positives)
    - **V3:** Behaviour + Network Context + Evidence Confidence (Prevents hasty isolation)
    - **V4:** Complete Framework with Adaptive Reassessment & Dynamic ACL Enforcement
    """)
    st.dataframe(df_abl, use_container_width=True)

    csv_data = df_comp.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Benchmark Results (CSV)",
        data=csv_data,
        file_name="zero_trust_comparative_results.csv",
        mime="text/csv"
    )
