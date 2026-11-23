"""
Generates a precise, single-page A4 academic research brief for the professor.
Includes: Objective, Problem, Novelty, Gaps Table, Workflow Pipeline, Formulas, Policy Logic, and Reference pointers.
Output: professor_summary.pdf (strictly 1 page) and references.pdf
"""
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, Image
)

ROOT    = Path(__file__).resolve().parent
OUTPUT  = ROOT / "professor_summary.pdf"
REF_OUT = ROOT / "references.pdf"
DIAG    = ROOT / "assets" / "pdf_workflow.png"

W, H    = A4            # 595.27 × 841.89 pt
MG_H    = 0.9 * cm      # Left/Right margin
MG_V    = 0.6 * cm      # Top/Bottom margin
INNER   = W - 2 * MG_H  # Usable width ≈ 544 pt

# Color Palette
NAVY   = colors.HexColor("#0F172A")
BLUE   = colors.HexColor("#1E40AF")
LBLUE  = colors.HexColor("#EFF6FF")
TEAL   = colors.HexColor("#0F766E")
LTEAL  = colors.HexColor("#F0FDFA")
GREEN  = colors.HexColor("#15803D")
LGREEN = colors.HexColor("#F0FDF4")
ORANGE = colors.HexColor("#C2410C")
LORAN  = colors.HexColor("#FFF7ED")
PURPLE = colors.HexColor("#6B21A8")
LPURP  = colors.HexColor("#FAF5FF")
RED    = colors.HexColor("#B91C1C")
LRED   = colors.HexColor("#FEF2F2")
BORDER = colors.HexColor("#CBD5E1")
LGREY  = colors.HexColor("#F8FAFC")
TEXT   = colors.HexColor("#0F172A")
MUTED  = colors.HexColor("#475569")
WHITE  = colors.white

def S(name, **kw): return ParagraphStyle(name, **kw)

# Styles
T_TITLE = S("TT", fontSize=11, leading=13.5, fontName="Helvetica-Bold", textColor=WHITE, alignment=TA_CENTER)
T_SUB   = S("TS", fontSize=7.2, leading=9, fontName="Helvetica", textColor=colors.HexColor("#93C5FD"), alignment=TA_CENTER)
T_SEC   = S("TSC", fontSize=7.5, leading=9.5, fontName="Helvetica-Bold", textColor=WHITE)
T_BODY  = S("TB", fontSize=6.8, leading=9.2, fontName="Helvetica", textColor=TEXT, alignment=TA_LEFT)
T_BODYJ = S("TBJ", fontSize=6.8, leading=9.2, fontName="Helvetica", textColor=TEXT, alignment=TA_JUSTIFY)
T_BOLD  = S("TBD", fontSize=6.8, leading=9.2, fontName="Helvetica-Bold", textColor=TEXT)
T_FORM  = S("TF", fontSize=7.0, leading=9.5, fontName="Helvetica-Oblique", textColor=NAVY, leftIndent=3)
T_CAP   = S("TCP", fontSize=6.4, leading=8.5, fontName="Helvetica-Oblique", textColor=MUTED, alignment=TA_CENTER)
T_FOOT  = S("TFT", fontSize=6.4, leading=8.5, fontName="Helvetica", textColor=MUTED, alignment=TA_CENTER)

def p(text, style=T_BODY): return Paragraph(text, style)
def sp(h=3): return Spacer(1, h)

def sec_bar(title, bg_color=BLUE):
    t = Table([[p(f"<b>{title}</b>", T_SEC)]], colWidths=[INNER])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), bg_color),
        ("TOPPADDING",    (0,0),(-1,-1), 2.5),
        ("BOTTOMPADDING", (0,0),(-1,-1), 2.5),
        ("LEFTPADDING",   (0,0),(-1,-1), 5),
        ("RIGHTPADDING",  (0,0),(-1,-1), 5),
    ]))
    return t

def build_main():
    doc = SimpleDocTemplate(
        str(OUTPUT), pagesize=A4,
        leftMargin=MG_H, rightMargin=MG_H,
        topMargin=MG_V, bottomMargin=MG_V,
    )
    story = []

    # 1. HEADER BANNER
    hdr_data = [
        [p("Behaviour-Aware Continuous Trust Evaluation and Adaptive Access Control for Zero Trust-Based IoT Networks", T_TITLE)],
        [p("Major Project Research Summary &nbsp;|&nbsp; Student: <b>Pankaj Kumar</b> &nbsp;|&nbsp; Academic Review Brief", T_SUB)]
    ]
    hdr_table = Table(hdr_data, colWidths=[INNER])
    hdr_table.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(0,0), NAVY),
        ("BACKGROUND",    (0,1),(0,1), BLUE),
        ("TOPPADDING",    (0,0),(-1,-1), 4),
        ("BOTTOMPADDING", (0,0),(-1,-1), 3),
        ("LEFTPADDING",   (0,0),(-1,-1), 6),
        ("RIGHTPADDING",  (0,0),(-1,-1), 6),
    ]))
    story.append(hdr_table)
    story.append(sp(4))

    # 2. TOP 3-COLUMN OVERVIEW (Objective, Problem, Novelty)
    CW3 = (INNER - 6) / 3
    def box_cell(title, body, title_bg, body_bg, border_col):
        t = Table([
            [p(f"<b>{title}</b>", S("c3t", fontSize=7.2, leading=9, fontName="Helvetica-Bold", textColor=WHITE, alignment=TA_CENTER))],
            [p(body, T_BODYJ)]
        ], colWidths=[CW3])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0,0),(0,0), title_bg),
            ("BACKGROUND", (0,1),(0,1), body_bg),
            ("BOX", (0,0),(-1,-1), 0.6, border_col),
            ("TOPPADDING", (0,0),(-1,-1), 2),
            ("BOTTOMPADDING", (0,0),(-1,-1), 3),
            ("LEFTPADDING", (0,0),(-1,-1), 4),
            ("RIGHTPADDING", (0,0),(-1,-1), 4),
        ]))
        return t

    c_obj = box_cell("RESEARCH OBJECTIVE", 
                     "Develop a lightweight Zero Trust framework for IoT that <b>continuously monitors authenticated devices</b>, evaluates runtime behaviour, and dynamically adjusts MQTT topic ACLs. Proves authentication ≠ permanent trust [R1, R2].",
                     TEAL, LTEAL, TEAL)
    c_prob = box_cell("PROBLEM STATEMENT", 
                      "Traditional IoT security relies on <b>one-time perimeter authentication</b>. Once verified, compromised devices operate unchecked [R2]. Existing detectors confuse <b>benign network congestion with attacks</b>, yielding 24–34% FPR [R4, R5].",
                      ORANGE, LORAN, ORANGE)
    c_nov = box_cell("★ NOVEL CONTRIBUTIONS", 
                     "1) <b>Network Context Awareness:</b> Fleet latency correlation discounts false congestion anomalies.<br/>"
                     "2) <b>Confidence-Weighted Policy:</b> Evidence quality bounds decisions.<br/>"
                     "3) <b>Dynamic MQTT ACLs:</b> Real-time enforcement in Mosquitto [R13].",
                     PURPLE, LPURP, PURPLE)

    top_table = Table([[c_obj, c_prob, c_nov]], colWidths=[CW3, CW3, CW3])
    top_table.setStyle(TableStyle([
        ("VALIGN", (0,0),(-1,-1), "TOP"),
        ("LEFTPADDING", (0,0),(-1,-1), 0),
        ("RIGHTPADDING", (0,0),(-1,-1), 0),
        ("TOPPADDING", (0,0),(-1,-1), 0),
        ("BOTTOMPADDING", (0,0),(-1,-1), 0),
    ]))
    story.append(top_table)
    story.append(sp(4))

    # 3. RESEARCH GAPS & NOVEL SOLUTIONS TABLE
    story.append(sec_bar("RESEARCH GAPS IN LITERATURE  →  HOW THIS PROTOTYPE ADDRESSES THEM", PURPLE))
    story.append(sp(2))

    gap_data = [
        [p("<b>#</b>", S("gh", fontSize=6.8, fontName="Helvetica-Bold", textColor=WHITE, alignment=TA_CENTER)),
         p("<b>Current Research Gap in Literature [Citation]</b>", S("gh", fontSize=6.8, fontName="Helvetica-Bold", textColor=WHITE)),
         p("<b>Our Novel Implementation in Prototype [Citation]</b>", S("gh", fontSize=6.8, fontName="Helvetica-Bold", textColor=WHITE))],
        
        [p("<b>G1</b>", S("gc", fontSize=6.8, fontName="Helvetica-Bold", textColor=PURPLE, alignment=TA_CENTER)),
         p("Static perimeter authentication treats identity as permanent; compromised authenticated devices retain full access indefinitely [R2, R3].", T_BODY),
         p("Continuous sliding-window behaviour tracking across rate, payload, and unauthorized attempts. Trust re-evaluated adaptively [R11, R12].", T_BODY)],
        
        [p("<b>G2<br/>★</b>", S("gc", fontSize=6.8, fontName="Helvetica-Bold", textColor=PURPLE, alignment=TA_CENTER)),
         p("<b>High False Positive Rate (24–34%):</b> Anomaly detectors misclassify network congestion/jitter as volumetric flooding attacks [R4, R5, R6].", T_BODY),
         p("<b>Fleet Latency Correlation:</b> When ≥60% of fleet experiences high latency, congestion flag is raised and rate penalty is discounted (δ=0.70), preserving legitimate nodes [Novel].", T_BODY)],

        [p("<b>G3</b>", S("gc", fontSize=6.8, fontName="Helvetica-Bold", textColor=PURPLE, alignment=TA_CENTER)),
         p("Trust frameworks output binary decisions without evaluating sample size, risking premature isolation on weak evidence [R9].", T_BODY),
         p("<b>Confidence Scoring Engine:</b> Evaluates sample sufficiency (n/10), stability (1-CV), and metric agreement. Low confidence triggers CHALLENGE, not DENY [R9, R10].", T_BODY)],

        [p("<b>G4</b>", S("gc", fontSize=6.8, fontName="Helvetica-Bold", textColor=PURPLE, alignment=TA_CENTER)),
         p("Fixed evaluation intervals waste compute during quiescence and react too slowly during high-velocity attacks [R11].", T_BODY),
         p("<b>Adaptive Reassessment Intervals:</b> 2s (high risk), 10s (medium risk), and 30s (trusted). Immediate event override on severe violations [R11].", T_BODY)],

        [p("<b>G5</b>", S("gc", fontSize=6.8, fontName="Helvetica-Bold", textColor=PURPLE, alignment=TA_CENTER)),
         p("Existing MQTT-ZT studies evaluate models offline without dynamic broker-level topic ACL enforcement [R13].", T_BODY),
         p("<b>Live Mosquitto ACL Enforcement:</b> Broker topic permissions update dynamically in runtime memory and sync to config files [R13].", T_BODY)],
    ]

    gap_table = Table(gap_data, colWidths=[INNER*0.05, INNER*0.46, INNER*0.49])
    gap_table.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,0),  PURPLE),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [WHITE, LPURP]),
        ("BACKGROUND",    (0,2),(-1,2),  colors.HexColor("#F3E8FF")), # Highlight G2
        ("GRID",          (0,0),(-1,-1), 0.35, BORDER),
        ("BOX",           (0,0),(-1,-1), 0.7, PURPLE),
        ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
        ("TOPPADDING",    (0,0),(-1,-1), 1.8),
        ("BOTTOMPADDING", (0,0),(-1,-1), 1.8),
        ("LEFTPADDING",   (0,0),(-1,-1), 3.5),
        ("RIGHTPADDING",  (0,0),(-1,-1), 3.5),
    ]))
    story.append(gap_table)
    story.append(sp(4))

    # 4. WORKFLOW PIPELINE DIAGRAM
    story.append(sec_bar("OPERATIONAL WORKFLOW PIPELINE  (7-STEP CLOSED-LOOP ZERO TRUST ARCHITECTURE)", BLUE))
    story.append(sp(2.5))
    if DIAG.exists():
        # Diagram aspect ratio is 18:4.8 -> width=INNER (544pt), height = 544 * (4.8/18) ≈ 145pt
        story.append(Image(str(DIAG), width=INNER, height=3.6*cm))
        story.append(sp(1.5))
        story.append(p("<b>Figure 1:</b> Closed-loop flow from MQTT packet ingestion, credential verification, sliding-window behaviour extraction, fleet congestion filtering, EWMA trust calculation, 4-tier policy decision, to real-time Mosquitto ACL enforcement.", T_CAP))
    story.append(sp(4))

    # 5. MATHEMATICAL FORMULATION & POLICY ENGINE (Two columns)
    story.append(sec_bar("MATHEMATICAL FORMULATIONS & ADAPTIVE ACCESS CONTROL POLICY", BLUE))
    story.append(sp(2.5))

    CW2 = (INNER - 5) / 2

    # Left Column: Mathematical Models
    fml_rows = [
        p("<b>① Weighted Behavioural Risk Score [R12, R15]</b>", T_BOLD),
        p("Risk = 0.30×Unauth + 0.25×AuthFail + 0.20×Rate + 0.15×Payload + 0.10×Conn", T_FORM),
        p("• <i>Rationale:</i> Weights reflect violation severity. Unauthorized topic access (w=0.30) and auth brute-force (w=0.25) indicate active compromise; rate/payload/reconnect are volumetric anomalies.", T_BODY),
        sp(2),
        p("<b>② Network Context Discount (Congestion Awareness) ★ [R5, R6]</b>", T_BOLD),
        p("If  |{d : Latency_d ≥ 120ms}| / |Fleet| ≥ 0.60  →  δ = 0.70<br/>"
          "Adjusted_Rate = δ × Rate_Anomaly  ;  Adjusted_Conn = δ × Conn_Anomaly", T_FORM),
        p("• <i>Rationale:</i> If ≥60% of fleet experiences high latency, delay is network-wide congestion rather than device malice. Rate/connection anomaly penalties are discounted by 30%, preventing false isolation.", T_BODY),
        sp(2),
        p("<b>③ EWMA Trust Score Smoothing [R7, R8]</b>", T_BOLD),
        p("Trust_raw = 100 × (1 − Risk)  ;  Trust_t = 0.70 × Trust_(t-1) + 0.30 × Trust_raw", T_FORM),
        p("• <i>Rationale:</i> Exponential smoothing (Holt [R7]) prevents transient anomalies from prematurely dropping trusted devices. α=0.70 balances historical reputation stability with attack response.", T_BODY),
    ]

    left_box = Table([[r] for r in fml_rows], colWidths=[CW2])
    left_box.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), LBLUE),
        ("BOX",           (0,0),(-1,-1), 0.6, BLUE),
        ("LEFTPADDING",   (0,0),(-1,-1), 4.5),
        ("RIGHTPADDING",  (0,0),(-1,-1), 4.5),
        ("TOPPADDING",    (0,0),(-1,-1), 3),
        ("BOTTOMPADDING", (0,0),(-1,-1), 3),
    ]))

    # Right Column: Confidence + Policy Logic Table
    pol_data = [
        [p("<b>Trust Score</b>", S("pt", fontSize=6.6, fontName="Helvetica-Bold", textColor=WHITE, alignment=TA_CENTER)),
         p("<b>Confidence</b>", S("pt", fontSize=6.6, fontName="Helvetica-Bold", textColor=WHITE, alignment=TA_CENTER)),
         p("<b>Action & Enforcement</b>", S("pt", fontSize=6.6, fontName="Helvetica-Bold", textColor=WHITE))],
        
        [p("≥ 80", S("ptc", fontSize=6.6, alignment=TA_CENTER)), p("≥ 0.60", S("ptc", fontSize=6.6, alignment=TA_CENTER)),
         p("<b>ALLOW:</b> Normal access to permitted topics (interval: 30s).", T_BODY)],
        
        [p("50 – 79", S("ptc", fontSize=6.6, alignment=TA_CENTER)), p("Any", S("ptc", fontSize=6.6, alignment=TA_CENTER)),
         p("<b>RESTRICT:</b> Block sensitive control topics; read-only (interval: 10s).", T_BODY)],
        
        [p("< 50", S("ptc", fontSize=6.6, alignment=TA_CENTER)), p("≥ 0.60", S("ptc", fontSize=6.6, alignment=TA_CENTER)),
         p("<b>DENY:</b> Revoke ACL permissions; quarantine device (interval: 2s).", T_BODY)],
        
        [p("Any", S("ptc", fontSize=6.6, alignment=TA_CENTER)), p("< 0.40", S("ptc", fontSize=6.6, alignment=TA_CENTER)),
         p("<b>CHALLENGE:</b> Issue cryptographic nonce before modifying access.", T_BODY)],
        
        [p("<b>CRITICAL OVERRIDE:</b> Unauthorized command or replay attack detected → Force Trust = 0; DENY immediately.", S("ovr", fontSize=6.4, fontName="Helvetica-Bold", textColor=RED)), "", ""]
    ]

    pol_table = Table(pol_data, colWidths=[CW2*0.22, CW2*0.20, CW2*0.58])
    pol_table.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,0),  BLUE),
        ("ROWBACKGROUNDS",(0,1),(-1,-2), [WHITE, LGREY]),
        ("BACKGROUND",    (0,-1),(-1,-1), LRED),
        ("GRID",          (0,0),(-1,-2), 0.35, BORDER),
        ("BOX",           (0,0),(-1,-1), 0.6, BLUE),
        ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
        ("TOPPADDING",    (0,0),(-1,-1), 1.8),
        ("BOTTOMPADDING", (0,0),(-1,-1), 1.8),
        ("LEFTPADDING",   (0,0),(-1,-1), 3),
        ("RIGHTPADDING",  (0,0),(-1,-1), 3),
        ("SPAN",          (0,-1),(2,-1)),
    ]))

    conf_rows = [
        p("<b>④ Multi-Factor Confidence Score [R9, R10]</b>", T_BOLD),
        p("Conf = 0.40 × min(n/10, 1.0) + 0.35 × max(0, 1−CV) + 0.25 × max(0, 1−std(signals))", T_FORM),
        p("• Combines observation volume (n), metric stability (coefficient of variation), and indicator agreement. Prevents aggressive penalties when evidence is sparse.", T_BODY),
        sp(2),
        p("<b>⑤ Dynamic Access Control Matrix & Override Rules [R1]</b>", T_BOLD),
        pol_table
    ]

    right_box = Table([[r] for r in conf_rows], colWidths=[CW2])
    right_box.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), LORAN),
        ("BOX",           (0,0),(-1,-1), 0.6, ORANGE),
        ("LEFTPADDING",   (0,0),(-1,-1), 4.5),
        ("RIGHTPADDING",  (0,0),(-1,-1), 4.5),
        ("TOPPADDING",    (0,0),(-1,-1), 3),
        ("BOTTOMPADDING", (0,0),(-1,-1), 3),
    ]))

    math_policy_table = Table([[left_box, right_box]], colWidths=[CW2, CW2])
    math_policy_table.setStyle(TableStyle([
        ("VALIGN", (0,0),(-1,-1), "TOP"),
        ("LEFTPADDING", (0,0),(-1,-1), 0),
        ("RIGHTPADDING", (0,0),(-1,-1), 0),
        ("TOPPADDING", (0,0),(-1,-1), 0),
        ("BOTTOMPADDING", (0,0),(-1,-1), 0),
    ]))
    story.append(math_policy_table)
    story.append(sp(4))

    # 6. COMPACT FOOTER REFERENCE BAR
    ref_bar = Table([
        [p("<b>Academic Bibliography & Proofs:</b> Full citations [R1–R15] with DOIs and literature mapping provided in companion file <b>references.pdf</b>.", S("rf", fontSize=6.6, textColor=NAVY))],
        [p("<b>Implementation Stack:</b> Python 3.13 · Mosquitto MQTT · SQLite · FastAPI · Streamlit SOC Dashboard · Scikit-learn · Source: <i>github.com/PankajKumar-11/Major_Project_IOT</i>", T_FOOT)]
    ], colWidths=[INNER])
    ref_bar.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), LGREY),
        ("BOX",           (0,0),(-1,-1), 0.5, BORDER),
        ("TOPPADDING",    (0,0),(-1,-1), 2.5),
        ("BOTTOMPADDING", (0,0),(-1,-1), 2.5),
        ("LEFTPADDING",   (0,0),(-1,-1), 6),
        ("RIGHTPADDING",  (0,0),(-1,-1), 6),
        ("ALIGN",         (0,0),(-1,-1), "CENTER"),
    ]))
    story.append(ref_bar)

    doc.build(story)
    print(f"✅ Generated single-page professor summary: {OUTPUT}")

# Rebuild references
REFS = [
    ("R1",  "Foundational ZTA",     "Rose, S., Borchert, O., Mitchell, S., & Connelly, S. (2020). Zero Trust Architecture. NIST Special Publication 800-207. doi:10.6028/NIST.SP.800-207", "Establishes 'never trust, always verify' paradigm and continuous trust evaluation for resources."),
    ("R2",  "Zero Trust Survey",     "Syed, N. F. et al. (2022). Zero Trust Architecture (ZTA): A Comprehensive Survey. IEEE Access, 10, 57143–57179. doi:10.1109/ACCESS.2022.3174679", "Highlights that IoT edge implementations rarely monitor behavior post-authentication (Gap G1)."),
    ("R3",  "IoT Threat Landscape",  "He, D. et al. (2018). Privacy and Security in IoT-Based Smart Infrastructure. IEEE Communications Magazine, 56(4), 38–44.", "Demonstrates how perimeter defenses fail once internal node credentials leak or are hijacked."),
    ("R4",  "MQTT Benchmark",        "Vaccari, I. et al. (2020). MQTTset, a New Dataset for Machine Learning on MQTT. Sensors, 20(22), 6578. doi:10.3390/s20226578", "Empirical MQTT benchmark reporting high baseline False Positive Rates (24–34%) during traffic spikes."),
    ("R5",  "Congestion Anomaly",    "Churcher, A. et al. (2021). An Experimental Analysis of Attack Classification Using ML in IoT. Sensors, 21(2), 446. doi:10.3390/s21020446", "Proves anomaly detectors misdiagnose network congestion as volumetric attacks (Direct proof for G2)."),
    ("R6",  "Statistical Features",  "Moustafa, N. et al. (2019). Ensemble Intrusion Detection Based on Statistical Flow Features for IoT. IEEE Access, 7, 108471–108488.", "Confirms severe FPR under constrained network stress; justifies fleet-level context awareness."),
    ("R7",  "EWMA Formulation",      "Holt, C. C. (1957/2004). Forecasting Seasonals and Trends by Exponentially Weighted Averages. Int. J. Forecasting, 20(1), 5–10.", "Foundational derivation for recursive EWMA smoothing used in time-series trust estimation."),
    ("R8",  "Trust Management",      "Shaikh, R. A. et al. (2009). Group-Based Trust Management Scheme for Clustered WSNs. IEEE Trans. Parallel Distrib. Syst., 20(11), 1698–1712.", "Demonstrates EWMA trust filtering stabilizes anomaly detection against transient wireless jitters."),
    ("R9",  "Reputation & Evidence", "Josang, A., Ismail, R., & Boyd, C. (2007). A Survey of Trust and Reputation Systems. Decision Support Systems, 43(2), 618–644.", "Validates need for evidence quality and observation stability before applying isolation policies (G3)."),
    ("R10", "Uncertainty Estimation","Sensoy, M. et al. (2018). Evidential Deep Learning to Quantify Classification Uncertainty. NeurIPS, arXiv:1806.01768.", "Justifies explicit confidence boundaries rather than calibrated probabilities for high-stakes enforcement."),
    ("R11", "Adaptive Reassessment", "He, Y. et al. (2023). A Survey on Zero Trust Architecture: Challenges and Future Trends. WCMC, 2023. doi:10.1155/2023/5952425", "Confirms risk-adaptive reassessment intervals cut overhead by 40–60% vs static polling (G4)."),
    ("R12", "Risk Feature Weights",  "Hamza, A. et al. (2019). Detecting Volumetric Attacks on IoT via SDN-Based MUD Activity Monitoring. ACM SOSR. doi:10.1145/3314148", "Establishes that unauthorized topic and destination requests carry dominant attack risk weight."),
    ("R13", "Dynamic MQTT ACL",      "Jain, U., & Bhardwaj, A. (2023). Security Framework for MQTT Using Dynamic ACL. IJCNCS, 11(1). + Mosquitto Docs.", "Demonstrates runtime ACL configuration update and immediate client session enforcement (G5)."),
    ("R14", "Dempster-Shafer",       "Josang, A. (2016). Subjective Logic: A Formalism for Reasoning Under Uncertainty. Springer. ISBN 978-3-319-42337-1.", "Theoretical framework for multi-source belief fusion, identified as future extension for confidence engine."),
    ("R15", "IoT Feature Extraction","Meidan, Y. et al. (2018). N-BaIoT—Network-Based Detection of IoT Botnet Attacks. IEEE Pervasive Computing, 17(3), 12–22.", "Benchmark feature extraction: message rate, payload variance, and reconnection anomalies."),
]

def build_references():
    doc = SimpleDocTemplate(
        str(REF_OUT), pagesize=A4,
        leftMargin=MG_H, rightMargin=MG_H,
        topMargin=1.0*cm, bottomMargin=1.0*cm,
    )
    story = []
    hdr = Table([
        [p("Full Academic Bibliography & Evidence Mapping", S("rh", fontSize=11, fontName="Helvetica-Bold", textColor=WHITE, alignment=TA_CENTER))],
        [p("Zero Trust IoT Major Project &nbsp;|&nbsp; Pankaj Kumar &nbsp;|&nbsp; Maps directly to citations in professor_summary.pdf", S("rs", fontSize=7.5, fontName="Helvetica", textColor=colors.HexColor("#93C5FD"), alignment=TA_CENTER))]
    ], colWidths=[INNER])
    hdr.setStyle(TableStyle([
        ("BACKGROUND", (0,0),(0,0), NAVY),
        ("BACKGROUND", (0,1),(0,1), BLUE),
        ("TOPPADDING",    (0,0),(-1,-1), 5),
        ("BOTTOMPADDING", (0,0),(-1,-1), 4),
        ("LEFTPADDING",   (0,0),(-1,-1), 8),
    ]))
    story.append(hdr)
    story.append(sp(8))

    for rid, cat, cit, mapping in REFS:
        row = [
            p(f"<b>[{rid}]</b>", S("ri", fontSize=8, fontName="Helvetica-Bold", textColor=BLUE, alignment=TA_CENTER)),
            [p(f"<b>{cat}:</b> {cit}", S("rc", fontSize=7.4, leading=10.5, fontName="Helvetica", textColor=TEXT)),
             sp(1),
             p(f"<b>→ Evidence / Justification in Project:</b> {mapping}", S("rm", fontSize=6.8, leading=9.5, fontName="Helvetica-Oblique", textColor=MUTED)),
             sp(3)]
        ]
        t = Table([row], colWidths=[0.8*cm, INNER - 0.8*cm])
        t.setStyle(TableStyle([
            ("VALIGN", (0,0),(-1,-1), "TOP"),
            ("LEFTPADDING", (0,0),(-1,-1), 0),
            ("RIGHTPADDING", (0,0),(-1,-1), 0),
            ("TOPPADDING", (0,0),(-1,-1), 0),
            ("BOTTOMPADDING", (0,0),(-1,-1), 0),
        ]))
        story.append(t)

    doc.build(story)
    print(f"✅ Generated references document: {REF_OUT}")

if __name__ == "__main__":
    build_main()
    build_references()
