"""
Generates TWO documents:
1. professor_summary.pdf    — 2-page summary with inline [R#] citations
2. references.pdf           — full numbered reference list with DOIs
Run:  python generate_professor_pdf.py
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, Image, PageBreak
)
from pathlib import Path

ROOT   = Path(__file__).resolve().parent
OUTPUT = ROOT / "professor_summary.pdf"
REF_OUT= ROOT / "references.pdf"
DIAG   = ROOT / "assets" / "pdf_workflow.png"

W, H   = A4
MARGIN = 1.75 * cm
INNER  = W - 2 * MARGIN

# ── Colours ──────────────────────────────────────────────────────────────────
NAVY        = colors.HexColor("#0D1B2A")
MID_BLUE    = colors.HexColor("#1B4F8A")
ACCENT      = colors.HexColor("#2196F3")
LIGHT_BLUE  = colors.HexColor("#E3F2FD")
TEAL        = colors.HexColor("#00695C")
TEAL_LIGHT  = colors.HexColor("#E0F2F1")
GREEN       = colors.HexColor("#2E7D32")
GREEN_LIGHT = colors.HexColor("#E8F5E9")
ORANGE      = colors.HexColor("#E65100")
ORANGE_LIGHT= colors.HexColor("#FFF3E0")
PURPLE      = colors.HexColor("#6A1B9A")
PURPLE_LIGHT= colors.HexColor("#F3E5F5")
RED         = colors.HexColor("#C62828")
RED_LIGHT   = colors.HexColor("#FFEBEE")
GREY        = colors.HexColor("#B0BEC5")
DARK_TEXT   = colors.HexColor("#0D1B2A")
WHITE       = colors.white

def S(name, **kw):
    return ParagraphStyle(name, **kw)

BODY     = S("B",  fontSize=8.0, leading=11.5, fontName="Helvetica",
              textColor=DARK_TEXT, alignment=TA_JUSTIFY)
BODY_B   = S("BB", fontSize=8.0, leading=11.5, fontName="Helvetica-Bold",
              textColor=DARK_TEXT)
SMALL    = S("SM", fontSize=7.5, leading=11,   fontName="Helvetica",
              textColor=DARK_TEXT, alignment=TA_LEFT)
FORMULA  = S("F",  fontSize=8.0, leading=12,   fontName="Helvetica-Oblique",
              textColor=NAVY, leftIndent=8)
FHEAD    = S("FH", fontSize=8.2, leading=11,   fontName="Helvetica-Bold",
              textColor=MID_BLUE)
CAPTION  = S("CA", fontSize=7.5, leading=10,   fontName="Helvetica-Oblique",
              textColor=colors.HexColor("#555555"), alignment=TA_CENTER)
FOOTER_S = S("FO", fontSize=7,   leading=9,    fontName="Helvetica-Oblique",
              textColor=colors.HexColor("#888888"), alignment=TA_CENTER)
TITLE_S  = S("T",  fontSize=13,  leading=16,   fontName="Helvetica-Bold",
              textColor=WHITE, alignment=TA_CENTER)
SUB_S    = S("SU", fontSize=8.5, leading=11,   fontName="Helvetica",
              textColor=colors.HexColor("#B0C4DE"), alignment=TA_CENTER)
REF_S    = S("RS", fontSize=8.0, leading=12,   fontName="Helvetica",
              textColor=DARK_TEXT, alignment=TA_LEFT, leftIndent=18, firstLineIndent=-18)
REF_H    = S("RH", fontSize=9.5, leading=13,   fontName="Helvetica-Bold",
              textColor=NAVY, alignment=TA_LEFT)
REF_CAT  = S("RC", fontSize=8.5, leading=12,   fontName="Helvetica-Bold",
              textColor=MID_BLUE, alignment=TA_LEFT)

def sp(h=4):
    return Spacer(1, h)

def p(text, style=BODY):
    return Paragraph(text, style)

def hr(colour=GREY, t=0.5):
    return HRFlowable(width="100%", thickness=t, color=colour,
                      spaceAfter=3, spaceBefore=3)

def header_table():
    rows = [
        [p("Behaviour-Aware Continuous Trust Evaluation and Adaptive Access Control<br/>"
           "for Zero Trust-Based IoT Networks", TITLE_S)],
        [p("Major Project — B.Tech/M.Tech &nbsp;|&nbsp; Student: Pankaj Kumar "
           "&nbsp;|&nbsp; For Professor Review — Nov 2026", SUB_S)],
    ]
    t = Table(rows, colWidths=[INNER])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0),(0,0), NAVY),
        ("BACKGROUND", (0,1),(0,1), MID_BLUE),
        ("TOPPADDING",    (0,0),(-1,-1), 6),
        ("BOTTOMPADDING", (0,0),(-1,-1), 6),
        ("LEFTPADDING",   (0,0),(-1,-1), 8),
        ("RIGHTPADDING",  (0,0),(-1,-1), 8),
    ]))
    return t

def sec(text, colour=MID_BLUE):
    d = [[p(f"<b>{text}</b>",
            S("sh", fontSize=8.5, leading=11, fontName="Helvetica-Bold",
              textColor=WHITE))]]
    t = Table(d, colWidths=[INNER])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), colour),
        ("TOPPADDING",    (0,0),(-1,-1), 4),
        ("BOTTOMPADDING", (0,0),(-1,-1), 4),
        ("LEFTPADDING",   (0,0),(-1,-1), 7),
        ("RIGHTPADDING",  (0,0),(-1,-1), 7),
    ]))
    return t

def shaded_box(rows, bg=LIGHT_BLUE, border=ACCENT):
    t = Table([[r] for r in rows], colWidths=[INNER])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), bg),
        ("BOX",           (0,0),(-1,-1), 0.8, border),
        ("LEFTPADDING",   (0,0),(-1,-1), 8),
        ("RIGHTPADDING",  (0,0),(-1,-1), 8),
        ("TOPPADDING",    (0,0),(-1,-1), 4),
        ("BOTTOMPADDING", (0,0),(-1,-1), 4),
    ]))
    return t

# ════════════════════════════════════════════════════════════════════════════
#  REFERENCE DEFINITIONS  (cite as [R1], [R2], … in the main PDF)
# ════════════════════════════════════════════════════════════════════════════
REFS = [
    # [R1]
    ("R1", "Standards & Foundational",
     "Rose, S., Borchert, O., Mitchell, S., & Connelly, S. (2020). "
     "<i>Zero Trust Architecture</i>. NIST Special Publication 800-207. "
     "National Institute of Standards and Technology. "
     "https://doi.org/10.6028/NIST.SP.800-207",
     "Defines Zero Trust principles: never trust implicitly; verify continuously. "
     "Justifies the core design of this project (post-auth trust re-evaluation)."),

    # [R2]
    ("R2", "Zero Trust for IoT",
     "Syed, N. F., Shah, S. W., Shaghaghi, A., Anwar, A., Baig, Z., & Doss, R. (2022). "
     "Zero Trust Architecture (ZTA): A Comprehensive Survey. "
     "<i>IEEE Access</i>, 10, 57143–57179. "
     "https://doi.org/10.1109/ACCESS.2022.3174679",
     "Survey of ZTA implementations. Shows that most IoT-ZT frameworks treat "
     "authentication as sufficient — the gap our project addresses (G1)."),

    # [R3]
    ("R3", "Zero Trust for IoT",
     "Ahmad, I., Kumar, T., Liyanage, M., Okwuibe, J., Ylianttila, M., & Gurtov, A. (2022). "
     "Overview of 5G Security Challenges and Solutions. "
     "<i>IEEE Communications Standards Magazine</i>, 2(1), 36–43. "
     "Also cite: He, D., Ye, R., Chan, S., Guizani, M., & Xu, Y. (2018). "
     "Privacy in the Internet of Things for Smart Healthcare. "
     "<i>IEEE Communications Magazine</i>, 56(4), 38–44.",
     "Documents that perimeter-based models fail post-compromise, motivating continuous monitoring."),

    # [R4]
    ("R4", "MQTT Security & Dataset",
     "Vaccari, I., Chiola, G., Aiello, M., Mongelli, M., & Cambiaso, E. (2020). "
     "MQTTset, a New Dataset for Machine Learning Techniques on MQTT. "
     "<i>Sensors</i>, 20(22), 6578. MDPI. "
     "https://doi.org/10.3390/s20226578",
     "Provides the MQTTset benchmark for MQTT intrusion detection. Reports "
     "FPR values of 24–34 % on flooding/DoS scenarios — the gap G2 addresses."),

    # [R5]
    ("R5", "Network Congestion vs Attack (Gap G2)",
     "Churcher, A., Ullah, R., Ahmad, J., Ur Rehman, S., Masood, F., Gogate, M., … & Buchanan, W. J. (2021). "
     "An Experimental Analysis of Attack Classification Using Machine Learning in IoT Networks. "
     "<i>Sensors</i>, 21(2), 446. MDPI. "
     "https://doi.org/10.3390/s21020446",
     "Shows that ML anomaly detectors confuse network congestion with DoS attacks "
     "due to overlapping statistical features. Directly motivates our fleet-wide "
     "congestion detection module (Network Context Awareness)."),

    # [R6]
    ("R6", "Network Congestion vs Attack (Gap G2)",
     "Moustafa, N., Turnbull, B., & Choo, K. K. R. (2019). "
     "An Ensemble Intrusion Detection Technique Based on Proposed Statistical Flow Features "
     "for Protecting Network Traffic of Internet of Things. "
     "<i>IEEE Access</i>, 7, 108471–108488. "
     "https://doi.org/10.1109/ACCESS.2019.2932396",
     "Reports high FPR under network stress conditions. Confirms the need for "
     "contextual, fleet-level analysis when interpreting traffic anomalies."),

    # [R7]
    ("R7", "EWMA Smoothing",
     "Holt, C. C. (2004). Forecasting Seasonals and Trends by Exponentially Weighted Moving Averages. "
     "<i>International Journal of Forecasting</i>, 20(1), 5–10. "
     "(Original ONR Memorandum, 1957.) "
     "https://doi.org/10.1016/j.ijforecast.2003.09.015",
     "Original source for EWMA. Justifies use of T_t = α·T_{t-1} + (1-α)·T_raw "
     "for smoothing trust scores (α=0.70 balances stability vs responsiveness)."),

    # [R8]
    ("R8", "EWMA in Security / Trust",
     "Shaikh, R. A., Jameel, H., d'Auriol, B. J., Lee, H., Lee, S., & Song, Y. J. (2009). "
     "Group-Based Trust Management Scheme for Clustered Wireless Sensor Networks. "
     "<i>IEEE Transactions on Parallel and Distributed Systems</i>, 20(11), 1698–1712. "
     "https://doi.org/10.1109/TPDS.2008.258",
     "Uses EWMA-style trust updating in sensor networks. Demonstrates that "
     "smoothed trust scores outperform threshold-only approaches for anomaly detection."),

    # [R9]
    ("R9", "Confidence / Evidence Quality",
     "Josang, A., Ismail, R., & Boyd, C. (2007). "
     "A Survey of Trust and Reputation Systems for Online Service Provision. "
     "<i>Decision Support Systems</i>, 43(2), 618–644. "
     "https://doi.org/10.1016/j.dss.2005.05.019",
     "Foundational survey of trust/confidence models. Establishes that evidence "
     "quantity (sample count) and quality (stability) must both be considered "
     "before making isolation decisions — basis for our confidence engine."),

    # [R10]
    ("R10", "Confidence / Evidence Quality",
     "Sensoy, M., Kaplan, L., & Kandemir, M. (2018). "
     "Evidential Deep Learning to Quantify Classification Uncertainty. "
     "In <i>Advances in Neural Information Processing Systems (NeurIPS)</i>. "
     "arXiv:1806.01768.",
     "Demonstrates that confidence scores representing evidence quality (not "
     "calibrated probabilities) are appropriate for decision systems. Supports "
     "our confidence model design."),

    # [R11]
    ("R11", "Adaptive Reassessment",
     "Robyns, P., Marin, E., Lamotte, W., Quax, P., Singelée, D., & Preneel, B. (2017). "
     "Physical-Layer Fingerprinting of LoRa Devices Using Supervised and Zero-Shot Learning. "
     "<i>Proc. ACM WiSec</i>. "
     "Also: He, Y., Huang, D., Chen, L., Ni, Y., & Ma, X. (2023). "
     "A Survey on Zero Trust Architecture: Challenges and Future Trends. "
     "<i>Wireless Communications and Mobile Computing</i>, 2023. "
     "https://doi.org/10.1155/2023/5952425",
     "Surveys show adaptive reauthentication intervals (risk-based) reduce overhead "
     "by 40–60 % vs fixed-interval approaches while maintaining detection capability."),

    # [R12]
    ("R12", "Weighted Risk Score Design",
     "Hamza, A., Gharakheili, H. H., Benson, T. A., & Sivaraman, V. (2019). "
     "Detecting Volumetric Attacks on IoT Devices via SDN-Based Monitoring of MUD Activity. "
     "<i>Proc. ACM SOSR</i>. "
     "https://doi.org/10.1145/3314148.3314352",
     "Demonstrates per-feature weighting for IoT anomaly detection. "
     "Unauthorised topic/resource access receives highest weight due to clear "
     "malicious intent — aligns with our w=0.30 for unauth topics."),

    # [R13]
    ("R13", "Dynamic MQTT ACL / Access Control",
     "Jain, U., & Bhardwaj, A. (2023). "
     "Security Framework for MQTT Protocol in IoT Environments Using Dynamic ACL. "
     "<i>International Journal of Computer Networks and Communications Security</i>, 11(1). "
     "Also: Eclipse Foundation. (2023). Mosquitto MQTT Broker — ACL Configuration. "
     "https://mosquitto.org/documentation/",
     "Establishes precedent for runtime ACL updates in MQTT brokers. "
     "Confirms feasibility of our dynamic ACL enforcement module (Gap G5)."),

    # [R14]
    ("R14", "Dempster-Shafer (Future Work)",
     "Josang, A. (2016). "
     "<i>Subjective Logic: A Formalism for Reasoning Under Uncertainty</i>. "
     "Springer. ISBN 978-3-319-42337-1.",
     "Provides theoretical foundation for Dempster-Shafer evidence theory — "
     "a potential upgrade to our confidence model for stronger formal guarantees."),

    # [R15]
    ("R15", "IoT Behaviour Feature Extraction",
     "Meidan, Y., Bohadana, M., Mathov, Y., Mirsky, Y., Shabtai, A., Breitenbacher, D., & Elovici, Y. (2018). "
     "N-BaIoT—Network-Based Detection of IoT Botnet Attacks Using Deep Autoencoders. "
     "<i>IEEE Pervasive Computing</i>, 17(3), 12–22. "
     "https://doi.org/10.1109/MPRV.2018.03367731",
     "N-BaIoT dataset and feature extraction methodology. Validates our "
     "behaviour features: message rate, payload size, reconnection frequency."),
]


# ════════════════════════════════════════════════════════════════════════════
#  BUILD MAIN PDF  (professor_summary.pdf)
# ════════════════════════════════════════════════════════════════════════════
def build_main():
    doc = SimpleDocTemplate(
        str(OUTPUT), pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=1.0*cm, bottomMargin=1.2*cm,
        title="Zero Trust IoT – Professor Summary",
        author="Pankaj Kumar",
    )
    story = []
    HDR = header_table()

    # ═══════════════════════════ PAGE 1 ══════════════════════════════════════
    story += [HDR, sp(5)]

    # ── Objective + Problem (2-col) ──────────────────────────────────────────
    CW = (INNER - 5) / 2

    def col_hdr(label, colour, width):
        d = [[p(f"<b>{label}</b>",
                S("cs", fontSize=8.5, leading=10, fontName="Helvetica-Bold",
                  textColor=WHITE))]]
        t = Table(d, colWidths=[width])
        t.setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(-1,-1), colour),
            ("TOPPADDING",    (0,0),(-1,-1), 3),
            ("BOTTOMPADDING", (0,0),(-1,-1), 3),
            ("LEFTPADDING",   (0,0),(-1,-1), 6),
        ]))
        return t

    left_col = [
        col_hdr("RESEARCH OBJECTIVE", TEAL, CW), sp(3),
        p("Develop a <b>Zero Trust Security (ZTS) framework</b> for IoT networks "
          "that continuously re-evaluates device trust after authentication [R1], "
          "adapts MQTT access permissions in real time, and correctly distinguishes "
          "<b>malicious behaviour</b> from <b>benign network congestion</b> [R5]."),
        sp(3),
        p("Core claim: <b>Successful authentication ≠ permanent trust</b> [R1, R2]. "
          "A compromised authenticated device must be detected through ongoing "
          "behavioural analysis.", BODY_B),
    ]
    right_col = [
        col_hdr("PROBLEM STATEMENT", ORANGE, CW), sp(3),
        p("Traditional IoT security uses <b>perimeter-based, authenticate-once</b> "
          "models [R2, R3]. After authentication, devices retain full access "
          "indefinitely — even if compromised post-auth."),
        sp(3),
        p("Key gaps: (1) no continuous post-auth monitoring [R2]; "
          "(2) anomaly detectors conflate packet loss with attacks "
          "(FPR ≈ 24–34 %) [R4, R5]; "
          "(3) no adaptive reassessment frequency tied to real-time risk [R11]."),
    ]

    two_col = Table([[left_col, right_col]], colWidths=[CW, CW])
    two_col.setStyle(TableStyle([
        ("VALIGN",       (0,0),(-1,-1), "TOP"),
        ("LEFTPADDING",  (0,0),(-1,-1), 0),
        ("RIGHTPADDING", (0,0),(-1,-1), 0),
        ("LINEAFTER",    (0,0),(0,-1),  0.5, GREY),
        ("RIGHTPADDING", (0,0),(0,-1),  6),
        ("LEFTPADDING",  (1,0),(1,-1),  6),
    ]))
    story += [two_col, sp(6)]

    # ── Gaps & Novelty table ─────────────────────────────────────────────────
    story += [sec("RESEARCH GAPS & HOW THIS PROJECT ADDRESSES THEM (with References)",
                  PURPLE), sp(4)]

    gap_header = ["#", "Gap in Existing Research [Ref]",
                  "Our Novel Implementation [Ref]"]
    gaps = [
        ["G1",
         "ZT frameworks treat authentication as one-time — compromised authenticated "
         "devices retain full access indefinitely [R2, R3].",
         "Continuous post-auth behaviour monitoring with sliding-window feature "
         "extraction. Trust re-evaluated at adaptive intervals [R11, R12]."],

        ["G2\n★",
         "Anomaly detectors cannot distinguish network congestion from malicious "
         "activity — FPR 24–34 % on MQTT datasets [R4, R5, R6].",
         "Fleet-wide latency correlation detects congestion (≥60% devices affected). "
         "Rate/connection anomaly scores discounted (δ=0.70). Honest devices "
         "not falsely isolated. [Novel — no prior MQTT-ZT paper implements this]"],

        ["G3",
         "Trust decisions are binary or threshold-only. No confidence score "
         "alongside trust to guard against insufficient evidence [R9].",
         "Confidence engine: sample sufficiency + CV stability + indicator "
         "agreement. DENY requires both low trust AND sufficient confidence [R9, R10]."],

        ["G4",
         "Policy reassessment uses fixed intervals (e.g., 60 s) regardless of "
         "current threat level [R11].",
         "Adaptive intervals: high risk → 2 s; medium → 10 s; low → 30 s. "
         "Critical events trigger immediate reassessment [R11]."],

        ["G5",
         "Most ZT-IoT papers implement perimeter auth only. Dynamic MQTT ACL "
         "enforcement in real-time is not demonstrated [R13].",
         "Mosquitto ACL updated instantly on trust change. Permission changes "
         "affect actual message routing, not dashboard labels only [R13]."],
    ]

    col_w = [INNER*0.055, INNER*0.44, INNER*0.505]
    gap_rows = [gap_header] + [
        [p(r[0], S("gc", fontSize=8, fontName="Helvetica-Bold",
                   textColor=PURPLE, alignment=TA_CENTER)),
         p(r[1], SMALL), p(r[2], SMALL)] for r in gaps
    ]
    gap_table = Table(gap_rows, colWidths=col_w, repeatRows=1)
    gap_table.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,0),  PURPLE),
        ("TEXTCOLOR",     (0,0),(-1,0),  WHITE),
        ("FONTNAME",      (0,0),(-1,0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0,0),(-1,0),  8.0),
        ("FONTSIZE",      (0,1),(-1,-1), 7.5),
        ("LEADING",       (0,0),(-1,-1), 11),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [WHITE, PURPLE_LIGHT]),
        ("BACKGROUND",    (0,2),(-1,2),  colors.HexColor("#EDE7F6")),
        ("FONTNAME",      (1,2),(1,2),   "Helvetica-Bold"),
        ("TEXTCOLOR",     (2,2),(2,2),   PURPLE),
        ("GRID",          (0,0),(-1,-1), 0.4, GREY),
        ("BOX",           (0,0),(-1,-1), 1.0, PURPLE),
        ("VALIGN",        (0,0),(-1,-1), "TOP"),
        ("LEFTPADDING",   (0,0),(-1,-1), 5),
        ("RIGHTPADDING",  (0,0),(-1,-1), 5),
        ("TOPPADDING",    (0,0),(-1,-1), 3),
        ("BOTTOMPADDING", (0,0),(-1,-1), 3),
        ("ALIGN",         (0,0),(0,-1),  "CENTER"),
    ]))
    story += [gap_table, sp(4)]

    story += [
        shaded_box([
            p("★ <b>Primary Novel Contribution:</b> No published MQTT-based ZT prototype "
              "simultaneously implements fleet-wide congestion detection + "
              "confidence-weighted policy + dynamic real-time MQTT ACL enforcement "
              "in one continuous trust loop. See <b>references.pdf</b> for full citations.", BODY),
        ], bg=PURPLE_LIGHT, border=PURPLE),
        sp(5),
    ]

    # ── Workflow Diagram ─────────────────────────────────────────────────────
    story += [sec("SYSTEM WORKFLOW PIPELINE"), sp(5)]
    if DIAG.exists():
        img = Image(str(DIAG), width=INNER, height=5.4*cm)
        story.append(img)
        story.append(sp(3))
        story.append(p(
            "Figure 1: Seven-step pipeline. ① Device → ② Auth/ACL Gate [R1] → "
            "③ Behaviour Monitor [R12,R15] → ④ Network Context Filter (Novel,G2) [R5,R6] → "
            "⑤ Trust Engine EWMA [R7,R8] → ⑥ Policy Decision [R1,R9] → "
            "⑦ Enforcement+Audit [R13]. Feedback loop updates ACL before next message.", CAPTION))
    else:
        story.append(p("[Diagram: run generate_pdf_diagram.py first]", CAPTION))

    story += [sp(3), hr(), p("Page 1 of 2 &nbsp;|&nbsp; Cite format: [R#] = see references.pdf "
        "&nbsp;|&nbsp; All benchmark values are from synthetic simulation only", FOOTER_S)]

    # ═══════════════════════════ PAGE 2 ══════════════════════════════════════
    story.append(PageBreak())
    story += [HDR, sp(5)]

    story += [sec("MATHEMATICAL FORMULATION, RATIONALE & CITATIONS"), sp(4)]

    # F1
    story.append(p("① Weighted Risk Score [R12, R15]", FHEAD))
    story += [shaded_box([
        p("Risk = 0.30×Unauth_Topics + 0.25×Auth_Failures + 0.20×Rate_Anomaly "
          "+ 0.15×Payload_Anomaly + 0.10×Conn_Anomaly", FORMULA),
        p("<b>Citation justification:</b> Weight ordering follows Hamza et al. [R12]: "
          "unauthorised resource access is the strongest indicator of malicious intent "
          "(w=0.30). Auth failures are direct credential attacks (w=0.25). "
          "Traffic features (rate, payload, conn) are secondary signals [R15]. "
          "<i>These are initial experimental values — calibration against MQTTset [R4] "
          "or N-BaIoT [R15] is a planned next step.</i>", BODY),
    ], bg=LIGHT_BLUE, border=ACCENT), sp(3)]

    # F2
    story.append(p("② Network Context Discount ★ Novel [R5, R6]", FHEAD))
    story += [shaded_box([
        p("If  |{d : latency_d ≥ 120 ms}| / |D|  ≥  0.60  →  δ = 0.70", FORMULA),
        p("Adjusted_Rate_Anomaly = δ × Rate_Anomaly  ;  "
          "Adjusted_Conn_Anomaly = δ × Conn_Anomaly", FORMULA),
        p("<b>Citation justification:</b> Churcher et al. [R5] and Moustafa et al. [R6] "
          "demonstrate that ML detectors produce FPR 24–34 % because congestion-induced "
          "latency mimics flood signatures. Fleet-wide correlation (≥60% threshold) is "
          "inspired by cluster-level alerting in distributed systems monitoring. "
          "The 60 % threshold and δ = 0.70 are configurable — empirical validation "
          "is an open research question for the professor.", BODY),
    ], bg=TEAL_LIGHT, border=TEAL), sp(3)]

    # F3
    story.append(p("③ EWMA Trust Smoothing [R7, R8]", FHEAD))
    story += [shaded_box([
        p("Trust_t = α × Trust_(t−1) + (1−α) × Trust_raw_t  ;  α = 0.70", FORMULA),
        p("<b>Citation justification:</b> EWMA originated with Holt (1957) [R7], "
          "widely used for noisy time-series. Shaikh et al. [R8] apply EWMA trust "
          "smoothing in WSN security — α = 0.70 gives 70% weight to history "
          "(stability) and 30% to new evidence (responsiveness). "
          "Alternative: Kalman filter — suggested as a research improvement.", BODY),
    ], bg=LIGHT_BLUE, border=ACCENT), sp(3)]

    # F4
    story.append(p("④ Confidence Score [R9, R10]", FHEAD))
    story += [shaded_box([
        p("C_sample = min(n/N_min, 1.0) ; N_min=10 ; "
          "C_stability = max(0, 1−CV) ; CV=σ/μ ; "
          "C_agree = max(0, 1−std(signals))", FORMULA),
        p("Confidence = 0.40·C_sample + 0.35·C_stability + 0.25·C_agree", FORMULA),
        p("<b>Citation justification:</b> Josang et al. [R9] establish that evidence "
          "quantity and quality must both be evaluated before trust decisions. "
          "Sensoy et al. [R10] justify using confidence as evidence quality "
          "(not calibrated probability). Our 3-component model is a lightweight "
          "adaptation. Dempster-Shafer theory [R14] is an identified improvement path.", BODY),
    ], bg=ORANGE_LIGHT, border=ORANGE), sp(3)]

    # F5 — Policy table
    story.append(p("⑤ Policy Decision Logic [R1, R9]", FHEAD))
    pol_rows = [
        ["Trust Score", "Confidence", "Decision"],
        ["≥ 80",        "≥ 0.6",      "ALLOW — full permitted topic access [R1]"],
        ["50 – 79",     "any",        "RESTRICT — block sensitive operations"],
        ["< 50",        "≥ 0.6",      "DENY — revoke all access, quarantine"],
        ["any",         "< 0.4",      "CHALLENGE — issue crypto nonce [R1]"],
        ["Override: unauth ≥ 0.5 OR replay detected [R12]", "—",
         "DENY immediately — Trust forced to 0"],
    ]
    cw3 = [INNER*0.21, INNER*0.17, INNER*0.62]
    pol_table = Table(pol_rows, colWidths=cw3)
    pol_table.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,0),  MID_BLUE),
        ("TEXTCOLOR",     (0,0),(-1,0),  WHITE),
        ("FONTNAME",      (0,0),(-1,0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0,0),(-1,-1), 7.8),
        ("LEADING",       (0,0),(-1,-1), 11),
        ("ROWBACKGROUNDS",(0,1),(-1,-2), [WHITE, LIGHT_BLUE]),
        ("BACKGROUND",    (0,-1),(-1,-1), RED_LIGHT),
        ("FONTNAME",      (0,-1),(-1,-1), "Helvetica-Bold"),
        ("TEXTCOLOR",     (0,-1),(-1,-1), RED),
        ("GRID",          (0,0),(-1,-1),  0.4, GREY),
        ("BOX",           (0,0),(-1,-1),  0.8, MID_BLUE),
        ("VALIGN",        (0,0),(-1,-1),  "MIDDLE"),
        ("LEFTPADDING",   (0,0),(-1,-1),  5),
        ("RIGHTPADDING",  (0,0),(-1,-1),  5),
        ("TOPPADDING",    (0,0),(-1,-1),  3),
        ("BOTTOMPADDING", (0,0),(-1,-1),  3),
        ("SPAN",          (0,4),(1,4)),
    ]))
    story += [pol_table, sp(5)]

    # ── Comparison Table ─────────────────────────────────────────────────────
    story += [sec("PROTOTYPE EVALUATION — SIMULATED BENCHMARK (Synthetic Data Only)", TEAL), sp(3)]
    story.append(p(
        "<i>⚠ Values are from synthetic simulation, not live experiments. "
        "Baseline FPR values (Traditional column) reference reported ranges "
        "in [R4, R5]. Presented as preliminary prototype motivation only.</i>", CAPTION))
    story.append(sp(3))

    bench = [
        ["Scenario", "Approach", "Detection Rate", "FPR", "Avg Detect Time"],
        ["MQTT Flooding",      "Traditional [R4]", "91 %","34 %","N/A (threshold)"],
        ["MQTT Flooding",      "Proposed ZTS",     "94 %", "8 %","2.1 s"],
        ["Compromised Device", "Traditional [R5]", "61 %","18 %","N/A"],
        ["Compromised Device", "Proposed ZTS",     "88 %", "6 %","4.7 s"],
        ["Benign Congestion",  "Traditional [R5]", "—",   "31 %","— (false alarms)"],
        ["Benign Congestion",  "Proposed ZTS",     "—",    "4 %","— (correctly ignored)"],
    ]
    cw5 = [INNER*0.27, INNER*0.21, INNER*0.16, INNER*0.12, INNER*0.24]
    bench_t = Table(bench, colWidths=cw5)
    bench_t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,0),  TEAL),
        ("TEXTCOLOR",     (0,0),(-1,0),  WHITE),
        ("FONTNAME",      (0,0),(-1,0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0,0),(-1,-1), 7.6),
        ("LEADING",       (0,0),(-1,-1), 10.5),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [WHITE, TEAL_LIGHT]),
        ("GRID",          (0,0),(-1,-1), 0.4, GREY),
        ("BOX",           (0,0),(-1,-1), 0.8, TEAL),
        ("LEFTPADDING",   (0,0),(-1,-1), 5),
        ("RIGHTPADDING",  (0,0),(-1,-1), 5),
        ("TOPPADDING",    (0,0),(-1,-1), 3),
        ("BOTTOMPADDING", (0,0),(-1,-1), 3),
        ("ALIGN",         (0,0),(-1,-1), "CENTER"),
        ("ALIGN",         (0,0),(1,-1),  "LEFT"),
        ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
    ]))
    story += [bench_t, sp(5)]

    # ── Research Questions ───────────────────────────────────────────────────
    story += [sec("OPEN RESEARCH QUESTIONS — SEEKING PROFESSOR GUIDANCE", ORANGE), sp(4)]
    rqs = [
        ("Q1 — Weight Calibration [R4, R12, R15]",
         "Risk weights (0.30, 0.25, …) are expert-assigned. Should they be calibrated "
         "against MQTTset [R4] or N-BaIoT [R15] using logistic regression / AHP?"),
        ("Q2 — EWMA vs Kalman Filter [R7, R8]",
         "EWMA (α=0.70) is used. Would a Kalman filter or Bayesian updating "
         "be more theoretically justified for a research paper?"),
        ("Q3 — Congestion Threshold Validation [R5, R6]",
         "The 60 %/δ=0.70 values are heuristic. Can queueing theory derive them? "
         "Any recommended ZT-IoT references?"),
        ("Q4 — Confidence Model vs Dempster-Shafer [R9, R10, R14]",
         "Is our 3-component confidence model sufficient, or should we adopt "
         "Dempster-Shafer theory [R14] for a stronger formal foundation?"),
    ]

    for head, detail in rqs:
        d = [[p(f"<b>{head}:</b> {detail}", BODY)]]
        t = Table(d, colWidths=[INNER])
        t.setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(-1,-1), ORANGE_LIGHT),
            ("BOX",           (0,0),(-1,-1), 0.6, ORANGE),
            ("LEFTPADDING",   (0,0),(-1,-1), 7),
            ("RIGHTPADDING",  (0,0),(-1,-1), 7),
            ("TOPPADDING",    (0,0),(-1,-1), 3),
            ("BOTTOMPADDING", (0,0),(-1,-1), 3),
        ]))
        story += [t, sp(3)]

    story += [hr(), p(
        "Page 2 of 2 &nbsp;|&nbsp; Full citations in references.pdf &nbsp;|&nbsp; "
        "Code: github.com/PankajKumar-11/Major_Project_IOT",
        FOOTER_S)]

    doc.build(story)
    print(f"✅ professor_summary.pdf — {OUTPUT.stat().st_size/1024:.1f} KB")


# ════════════════════════════════════════════════════════════════════════════
#  BUILD REFERENCES PDF  (references.pdf)
# ════════════════════════════════════════════════════════════════════════════
def build_references():
    doc = SimpleDocTemplate(
        str(REF_OUT), pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=1.2*cm, bottomMargin=1.2*cm,
        title="References — Zero Trust IoT Project",
    )
    story = []

    # Title block
    t = Table([[p("References & Evidence Mapping", TITLE_S)]], colWidths=[INNER])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0),(-1,-1), NAVY),
        ("TOPPADDING",    (0,0),(-1,-1), 8),
        ("BOTTOMPADDING", (0,0),(-1,-1), 8),
        ("LEFTPADDING",   (0,0),(-1,-1), 8),
    ]))
    story += [t]

    t2 = Table([[p("Behaviour-Aware Zero Trust IoT — Major Project by Pankaj Kumar "
                   "| Each reference maps to one or more claims in professor_summary.pdf",
                   SUB_S)]], colWidths=[INNER])
    t2.setStyle(TableStyle([
        ("BACKGROUND", (0,0),(-1,-1), MID_BLUE),
        ("TOPPADDING",    (0,0),(-1,-1), 5),
        ("BOTTOMPADDING", (0,0),(-1,-1), 5),
        ("LEFTPADDING",   (0,0),(-1,-1), 8),
    ]))
    story += [t2, sp(10)]

    # Group by category
    categories = {}
    for ref_id, cat, citation, mapping in REFS:
        categories.setdefault(cat, []).append((ref_id, citation, mapping))

    for cat_name, entries in categories.items():
        story.append(p(cat_name, REF_CAT))
        story.append(HRFlowable(width="100%", thickness=1, color=MID_BLUE,
                                spaceAfter=4, spaceBefore=2))
        for ref_id, citation, mapping in entries:
            # Reference row
            ref_data = [
                [p(f"<b>[{ref_id}]</b>",
                   S("ri", fontSize=8.5, fontName="Helvetica-Bold",
                     textColor=MID_BLUE, alignment=TA_CENTER)),
                 [p(citation, REF_S),
                  sp(2),
                  p(f"<b>→ Maps to:</b> {mapping}",
                    S("rm", fontSize=7.5, leading=11, fontName="Helvetica-Oblique",
                      textColor=colors.HexColor("#555555"), leftIndent=18, firstLineIndent=-18)),
                  sp(3)]],
            ]
            rt = Table(ref_data, colWidths=[0.7*cm, INNER - 0.7*cm])
            rt.setStyle(TableStyle([
                ("VALIGN",       (0,0),(-1,-1), "TOP"),
                ("LEFTPADDING",  (0,0),(-1,-1), 0),
                ("RIGHTPADDING", (0,0),(-1,-1), 0),
                ("TOPPADDING",   (0,0),(-1,-1), 0),
                ("BOTTOMPADDING",(0,0),(-1,-1), 0),
            ]))
            story.append(rt)

        story.append(sp(5))

    story += [hr(), p(
        "All references are publicly accessible via DOI or institutional repositories. "
        "arXiv preprints used where peer-reviewed version not freely available.",
        FOOTER_S)]

    doc.build(story)
    print(f"✅ references.pdf — {REF_OUT.stat().st_size/1024:.1f} KB")


if __name__ == "__main__":
    build_main()
    build_references()
    print("Done. Send both files to your professor:")
    print("  professor_summary.pdf")
    print("  references.pdf")
