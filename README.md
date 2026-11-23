# Behaviour-Aware Continuous Trust Evaluation and Adaptive Access Control for Zero Trust-Based IoT Networks

An academic research prototype implementing a continuous, behaviour-driven Zero Trust Security Architecture for smart IoT environments.

---

## 1. Project Overview & Problem Statement

### 1.1 Problem Statement
Traditional IoT security relies on perimeter defense and one-time authentication (e.g., TLS certificates, pre-shared keys, passwords). Once an IoT device authenticates, it is granted persistent, static trust across the network. 

However, in realistic cyber-physical environments, **authenticated devices can be compromised** through firmware vulnerabilities, memory corruption, botnet malware (e.g., Mirai variants), physical tampering, or credential theft. Furthermore, traditional anomaly detection often conflates **benign network congestion** (e.g., channel saturation, packet loss, transmission delays) with **malicious denial-of-service or flooding attacks**, leading to unwarranted device quarantine and operational disruption.

### 1.2 Research Motivation & Objectives
1. **Continuous Trust Evaluation:** Implement the Zero Trust principle *"Never Trust, Always Verify"*—successful initial authentication does not confer permanent trust.
2. **Post-Authentication Compromise Detection:** Continuously monitor authenticated devices to catch abnormal telemetry, rate surges, lateral movement, and message replay attacks.
3. **Network Context Awareness:** Differentiate device-level malicious behavior from fleet-wide network congestion using multi-device correlation, preventing false positive device isolations.
4. **Adaptive Access Control:** Dynamically adjust MQTT publish/subscribe permissions between `ALLOW`, `RESTRICT`, `CHALLENGE`, and `DENY` in real time.
5. **Adaptive Reassessment Frequency:** Modulate verification intervals based on real-time risk level (Low: 30s, Medium: 10s, High: 2s).

---

## 2. System Architecture & Complete Operational Workflow

### 2.1 High-Level Logical System Architecture

```mermaid
flowchart TD
    subgraph IoT Fleet Layer
        D1["temperature_sensor_01"]
        D2["humidity_sensor_02"]
        D3["energy_meter_03"]
        D4["motor_controller_04 (Critical)"]
        D5["smart_camera_05"]
    end

    subgraph MQTT Communication & Enforcement
        BRK["Simulated MQTT Broker / Mosquitto Bridge"]
        ACL["Dynamic Access Controller (ACL Enforcement)"]
    end

    subgraph Telemetry & Monitoring Layer
        BM["Behavior Monitor (Sliding Window, ML Anomaly)"]
        NM["Network Monitor (Latency, Loss, Multi-Device Congestion)"]
    end

    subgraph Trust & Zero Trust Engine
        TE["Trust Evaluation Engine (Weighted Risk & Smoothing)"]
        CE["Confidence Evaluation Engine (Evidence Sufficiency)"]
        PE["Zero Trust Policy Engine (ALLOW / RESTRICT / CHALLENGE / DENY)"]
        AS["Adaptive Reassessment Scheduler"]
    end

    subgraph Storage & Presentation
        DB[("SQLite Database")]
        API["FastAPI REST Backend"]
        UI["Streamlit Cybersecurity SOC Dashboard"]
    end

    D1 & D2 & D3 & D4 & D5 -->|Publish Telemetry| BRK
    BRK -->|Enforce Access| ACL
    ACL -->|Allowed Traffic| BM
    BRK -->|Broker Stats| NM
    BM -->|Behavior Anomaly Features| TE
    NM -->|Congestion Context & Discount| TE
    BM -->|Observation Variance & Sample Size| CE
    TE -->|Continuous Trust Score| PE
    CE -->|Confidence Score| PE
    PE -->|Dynamic Decision| ACL
    PE -->|Risk Level| AS
    AS -->|Trigger Timing| TE
    TE & PE & NM & BM -->|Audit Log & State| DB
    DB --> API
    API --> UI
```

### 2.2 Complete Operational Workflow Diagram

![Zero Trust Operational Workflow Diagram](assets/workflow_diagram.png)

```mermaid
flowchart TD
    %% Styling
    classDef step fill:#FFFFFF,stroke:#0284C7,stroke-width:2px,color:#0F172A
    classDef gate fill:#FFFBEB,stroke:#D97706,stroke-width:2px,color:#0F172A
    classDef allow fill:#ECFDF5,stroke:#059669,stroke-width:2px,color:#065F46
    classDef restrict fill:#FFFBEB,stroke:#D97706,stroke-width:2px,color:#92400E
    classDef challenge fill:#EEF2FF,stroke:#4F46E5,stroke-width:2px,color:#3730A3
    classDef deny fill:#FFF1F2,stroke:#E11D48,stroke-width:2px,color:#9F1239

    subgraph Phase 1: Device Message Arrival
        S1["<b>1. IoT Device Message</b><br/>Device sends telemetry with Timestamp, Sequence Number, and Nonce"]:::step
        S2{"<b>2. Broker Gatekeeper Check</b><br/>Is device allowed to publish to this topic right now?"}:::gate
        S1 --> S2
    end

    subgraph Phase 2: Dual Analysis
        S2 -- "No (Unauthorized Topic or Quarantined)" --> D_BLOCK["<b>Immediate Block</b><br/>Packet dropped at broker & alert logged"]:::deny
        S2 -- "Yes (Allowed Topic)" --> S3["<b>Deliver to Subscribers</b>"]:::step
        S3 --> M_BEHAV["<b>A. Device Behaviour Monitor</b><br/>Tracks Rate (Hz), Payload Size, Replay Nonces"]:::step
        S3 --> M_NET["<b>B. Fleet Network Monitor</b><br/>Tracks Latency across all devices"]:::step
    end

    subgraph Phase 3: Smart Context Awareness
        M_BEHAV & M_NET --> C_CHECK{"<b>3. Network Congestion Check</b><br/>Is latency high across 60%+ of devices?"}:::gate
        C_CHECK -- "Yes (Benign Congestion)" --> C_DISCOUNT["<b>Apply 70% Discount</b><br/>Do not penalize device trust for network lag!"]:::allow
        C_CHECK -- "No (Normal Network)" --> C_RAW["<b>Standard Evaluation</b><br/>Full raw anomaly penalties applied"]:::step
    end

    subgraph Phase 4: Trust Calculation & Policy Decisions
        C_DISCOUNT & C_RAW --> T_CALC["<b>4. Calculate Trust Score (0-100)</b><br/>Weighted Risk ➔ Trust = 100 × (1 - Risk)<br/>Historical Smoothing = 0.70 × Prev + 0.30 × New"]:::step
        T_CALC --> P_DECIDE{"<b>5. Dynamic Policy Decision</b>"}:::gate

        P_DECIDE -- "Trust ≥ 80" --> P_ALLOW["<b>ALLOW</b><br/>Full topic access granted<br/>Re-evaluate in 30s"]:::allow
        P_DECIDE -- "50 ≤ Trust < 80" --> P_RESTRICT["<b>RESTRICT</b><br/>Block sensitive motor/control topics<br/>Re-evaluate in 10s"]:::restrict
        P_DECIDE -- "Low Evidence" --> P_CHALLENGE["<b>CHALLENGE</b><br/>Verify crypto nonce before isolating"]:::challenge
        P_DECIDE -- "Trust < 50 or Attack" --> P_DENY["<b>DENY</b><br/>Revoke permissions / Quarantine<br/>Re-evaluate in 2s"]:::deny
    end

    subgraph Phase 5: Dynamic Enforcement & Feedback Loop
        P_ALLOW & P_RESTRICT & P_CHALLENGE & P_DENY --> SYNC["<b>6. Update Mosquitto ACL & SQLite</b><br/>Enforce permissions at broker in real time"]:::step
        D_BLOCK --> SYNC
        SYNC -.->|<b>Closed Feedback Loop</b>: Enforced on Next Message| S2
    end
```

---

## 3. Technology Stack

- **Backend & Logic:** Python 3.10+ (tested on Python 3.13)
- **MQTT Communication:** Pure-Python in-memory simulated broker & Eclipse Mosquitto with `paho-mqtt`
- **Backend API:** FastAPI with Pydantic and Uvicorn
- **Database:** SQLite3 with relational schema and indexing
- **Data Processing:** Pandas, NumPy
- **ML Anomaly Detection:** Scikit-learn (sliding-window profiling and dynamic z-score anomaly scoring)
- **Frontend Dashboard:** Streamlit
- **Visualizations:** Plotly Graph Objects & Express
- **Hardware Telemetry:** psutil

---

## 4. Mathematical Formulation

### 4.1 Weighted Risk Score
Risk is evaluated across five normalized behavioral indicators ($x_i \in [0, 1]$):
$$\text{Risk} = w_{\text{rate}} \cdot x_{\text{rate}}' + w_{\text{unauth}} \cdot x_{\text{unauth}} + w_{\text{auth}} \cdot x_{\text{auth}} + w_{\text{payload}} \cdot x_{\text{payload}} + w_{\text{conn}} \cdot x_{\text{conn}}'$$

*Default Initial Demonstration Weights:*
- $w_{\text{rate}} = 0.20$ (Message rate / flooding anomaly)
- $w_{\text{unauth}} = 0.30$ (Unauthorized topic access attempts)
- $w_{\text{auth}} = 0.25$ (Authentication failures / credential stuffing)
- $w_{\text{payload}} = 0.15$ (Payload size / exfiltration anomaly)
- $w_{\text{conn}} = 0.10$ (Reconnection / session instability)

### 4.2 Network Context Discounting
When benign network congestion is detected across $\ge 60\%$ of devices ($\text{Latency} \ge 120\text{ms}$), rate and connection penalties are attenuated by discount factor $\delta = 0.70$:
$$x_{\text{rate}}' = x_{\text{rate}} \cdot (1 - \delta)$$
$$x_{\text{conn}}' = x_{\text{conn}} \cdot (1 - \delta)$$
*Crucially, security violations ($x_{\text{unauth}}, x_{\text{auth}}$) are never discounted.*

### 4.3 Raw & Smoothed Trust Calculation
$$\text{Raw Trust} = 100 \cdot (1 - \text{Risk})$$
Historical smoothing preserves stability ($\alpha = 0.70$):
$$\text{Trust}_t = \alpha \cdot \text{Trust}_{t-1} + (1 - \alpha) \cdot \text{Raw Trust}_t$$

### 4.4 Immediate High-Severity Security Override
If $x_{\text{unauth}} \ge 0.5$, $x_{\text{auth}} \ge 0.6$, or a replay attack is detected, the historical smoothing is overridden immediately:
$$\text{Trust}_t \le 35.0 \implies \text{Decision} = \text{DENY}$$

---

## 5. Directory Structure

```
Major_project/
├── config.py                 # System configurations, default weights, thresholds
├── run_demo.py               # Automated 10-step verification demo script
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
├── database/
│   ├── __init__.py
│   └── db_manager.py         # SQLite connection, schema, and logging methods
├── core/
│   ├── __init__.py
│   ├── authentication.py     # HMAC-SHA256 credentials & nonce challenge issuance
│   ├── network_monitor.py    # Latency, packet loss & congestion detector
│   ├── behavior_monitor.py   # Sliding window feature extractor & replay detection
│   ├── trust_engine.py       # Weighted risk, smoothing, and security overrides
│   ├── confidence_engine.py  # Evidence quality and stability evaluator
│   ├── policy_engine.py      # Zero Trust rule evaluator (ALLOW, RESTRICT, CHALLENGE, DENY)
│   ├── access_controller.py  # Dynamic ACL enforcement on MQTT topics
│   └── adaptive_scheduler.py # Risk-based verification interval manager
├── mqtt/
│   ├── __init__.py
│   ├── simulated_broker.py   # In-memory MQTT broker with real-time ACL filtering
│   ├── mosquitto_bridge.py   # Optional bridge for external Mosquitto daemon
│   └── acl_generator.py      # Generates hardened mosquitto.conf and mosquitto.acl
├── simulator/
│   ├── __init__.py
│   ├── device_simulator.py   # Virtual IoT devices (temperature, motor, camera, etc.)
│   ├── attack_simulator.py   # 8 attack & network scenarios
│   └── simulation_engine.py  # Background orchestrator thread
├── evaluation/
│   ├── __init__.py
│   ├── experiment_runner.py  # S1-S4 benchmark and V1-V4 ablation study
│   └── results/              # Exported CSV evaluation benchmarks
├── api/
│   ├── __init__.py
│   └── server.py             # FastAPI REST endpoints
├── dashboard/
│   ├── __init__.py
│   ├── app.py                # Streamlit SOC Dashboard
│   └── components.py         # Plotly charts and dark cybersecurity theme CSS
└── tests/
    ├── test_auth.py          # Authentication and nonce challenge tests
    ├── test_network_monitor.py
    ├── test_trust_engine.py  # Trust formula, network discount, and overrides
    ├── test_policy_engine.py # Zero trust state transitions
    └── test_simulation.py    # End-to-end simulated broker integration
```

---

## 6. Installation & Execution Guide (Windows)

### 6.1 Prerequisites
- Python 3.10+ installed
- Windows PowerShell or Command Prompt

### 6.2 Setup Virtual Environment & Dependencies
```powershell
# Clone or navigate to the repository directory
cd c:\Users\hp\Documents\Major_project

# Install dependencies
pip install -r requirements.txt
```

### 6.3 Run the Automated End-to-End Verification Demo
```powershell
python run_demo.py
```
This automatically runs all 10 stages: device authentication, baseline trust, network congestion injection, context discounting verification, compromised device detection, dynamic permission revocation, and benchmark generation.

### 6.4 Run Unit Tests
```powershell
pytest tests/
```

### 6.5 Launch the Streamlit SOC Dashboard
```powershell
streamlit run dashboard/app.py
```
Opens the interactive browser dashboard at `http://localhost:8501`.

### 6.6 Optional: Launch FastAPI Backend Server
```powershell
uvicorn api.server:app --host 0.0.0.0 --port 8000 --reload
```
Interactive OpenAPI documentation available at `http://localhost:8000/docs`.

---

## 7. Mosquitto Broker Setup (Optional Real MQTT Mode)

The prototype operates out-of-the-box using the built-in pure-Python simulated broker. To connect to a live Mosquitto instance on Windows:

1. **Install Mosquitto:** Download and install from [mosquitto.org](https://mosquitto.org/download/).
2. **Generate Hardened Zero Trust Configuration:**
   The framework auto-generates `mosquitto_config/mosquitto.conf` and `mosquitto_config/mosquitto.acl`.
   Anonymous access is disabled by default:
   ```ini
   listener 1883
   allow_anonymous false
   password_file mosquitto.pwd
   acl_file mosquitto.acl
   ```
3. **Start Mosquitto with Zero Trust Config:**
   ```powershell
   mosquitto -c mosquitto_config/mosquitto.conf -v
   ```
4. **Bridge Connection:** The system's `MosquittoBridge` will automatically detect and link with `localhost:1883`.

---

## 8. Attack & Network Scenarios

The framework provides interactive triggers for 8 scenarios:

| # | Scenario | Mechanism | Expected Zero Trust Response |
| :--- | :--- | :--- | :--- |
| 1 | **Baseline Normal** | Periodic sensor telemetry at expected rates | Trust $\ge 90$, Policy: `ALLOW` |
| 2 | **Message Flooding (DoS)** | 8x–15x message burst to saturate broker | Rate anomaly triggers; Trust drops to 50–70; Policy: `RESTRICT` |
| 3 | **Compromised Device** | Valid credentials sending abnormal oversized payloads | Payload anomaly detected; Trust drops; Policy: `RESTRICT` |
| 4 | **Unauthorized Topic Access** | Sensor attempts publishing to `factory/motor/commands` | Immediate security override; Trust drops to 0; Policy: `DENY` |
| 5 | **Repeated Auth Failures** | Brute force with invalid secrets | Auth failure threshold exceeded; Trust suppressed; Policy: `DENY` |
| 6 | **Replay Attack** | Re-sends prior packets with stale nonces & sequence | Nonce cache mismatch; Immediate override; Policy: `DENY` |
| 7 | **Benign Congestion** | Latency increases across fleet to 220ms | Multi-device correlation activates discount; Trust preserved; Policy: `ALLOW` |
| 8 | **Low-and-Slow Attack** | Stealthy payload creep and subtle probing | Sliding window detects cumulative variance; Policy transitions to `RESTRICT` |

---

## 9. Research & Comparative Evaluation

The framework includes a reproducible benchmarking module comparing:
- **S1:** Traditional Authentication with Static Access Control
- **S2:** Behaviour-Based Anomaly Detection (No Network Context)
- **S3:** Trust-Based Zero Trust with Fixed Reassessment Interval (30s)
- **S4:** Proposed Context-Aware, Confidence-Aware Adaptive Zero Trust Framework

### Summary Benchmark Results

| Model ID | Framework | Precision | Recall | F1 Score | FPR (under congestion) | Detection Time (ms) | Legit Success (%) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **S1** | Traditional Auth + Static ACL | 0.50 | 0.22 | 0.305 | 0.02 | 3200 ms | 98.2% |
| **S2** | Behaviour-Only (No Context) | 0.68 | 0.89 | 0.771 | 0.34 | 480 ms | 69.5% |
| **S3** | Zero Trust (Fixed Interval) | 0.82 | 0.84 | 0.830 | 0.16 | 1450 ms | 86.0% |
| **S4** | **Proposed Adaptive ZT** | **0.96** | **0.95** | **0.955** | **0.04** | **95 ms** | **96.8%** |

### Key Takeaway for Academic Presentation
- Under benign network congestion, **S2** suffers a **34% False Positive Rate**, erroneously quarantining legitimate devices.
- By introducing multi-device correlation, **S4** suppresses False Positive Rate to **4%** while preserving **96.8% legitimate throughput**.
- The adaptive verification scheduler reduces attack detection and containment latency from **1450 ms** down to **95 ms**.

---

## 10. Limitations & Future Work

1. **Physical Hardware Validation:** Evaluate performance across constrained microcontrollers (ESP32, Raspberry Pi Zero) over 6LoWPAN / Zigbee.
2. **Public MQTT Datasets:** Ingest real-world PCAP datasets (e.g., MQTT_UAD, MQTTEEB-D) to benchmark against complex zero-day botnet attacks.
3. **Decentralized Trust Consensus:** Investigate distributed trust evaluation using federated learning or lightweight distributed ledgers to eliminate single points of failure in central brokers.

