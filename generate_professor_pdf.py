"""
Generates a 2-page academic professor summary PDF.
Includes: objective, problem, research gaps & novelty, workflow diagram,
formulas with rationale, benchmark table, research questions.

Run:  python generate_professor_pdf.py
Out:  professor_summary.pdf
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
DIAG   = ROOT / "assets" / "pdf_workflow.png"   # new simple diagram

W, H   = A4
MARGIN = 1.75 * cm
INNER  = W - 2 * MARGIN

# ── Colours ──────────────────────────────────────────────────────────────────
NAVY        = colors.HexColor("#0D1B2A")
DARK_BLUE   = colors.HexColor("#1565C0")
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

# ── Styles ───────────────────────────────────────────────────────────────────
def S(name, **kw):
    return ParagraphStyle(name, **kw)

TITLE_S  = S("T",  fontSize=13, leading=16, fontName="Helvetica-Bold",
              textColor=WHITE, alignment=TA_CENTER)
SUB_S    = S("SU", fontSize=8.5, leading=11, fontName="Helvetica",
              textColor=colors.HexColor("#B0C4DE"), alignment=TA_CENTER)
BODY     = S("B",  fontSize=8.0, leading=11.5, fontName="Helvetica",
              textColor=DARK_TEXT, alignment=TA_JUSTIFY)
BODY_B   = S("BB", fontSize=8.0, leading=11.5, fontName="Helvetica-Bold",
              textColor=DARK_TEXT, alignment=TA_LEFT)
SMALL    = S("SM", fontSize=7.5, leading=10.5, fontName="Helvetica",
              textColor=DARK_TEXT, alignment=TA_LEFT)
FORMULA  = S("F",  fontSize=8.0, leading=12,   fontName="Helvetica-Oblique",
              textColor=NAVY, leftIndent=8)
FHEAD    = S("FH", fontSize=8.2, leading=11,   fontName="Helvetica-Bold",
              textColor=MID_BLUE)
CAPTION  = S("CA", fontSize=7.5, leading=10,   fontName="Helvetica-Oblique",
              textColor=colors.HexColor("#555555"), alignment=TA_CENTER)
FOOTER_S = S("FO", fontSize=7,   leading=9,    fontName="Helvetica-Oblique",
              textColor=colors.HexColor("#888888"), alignment=TA_CENTER)
NOVEL_S  = S("NV", fontSize=7.8, leading=11,   fontName="Helvetica",
              textColor=DARK_TEXT, alignment=TA_LEFT)

# ── Helpers ───────────────────────────────────────────────────────────────────
def sp(h=4):
    return Spacer(1, h)

def p(text, style=BODY):
    return Paragraph(text, style)

def hr(colour=GREY, t=0.5):
    return HRFlowable(width="100%", thickness=t, color=colour,
                      spaceAfter=3, spaceBefore=3)

def header_table(title, subtitle):
    rows = [[p(title, TITLE_S)], [p(subtitle, SUB_S)]]
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
    data = [[p(f"<b>{text}</b>",
               S("sh", fontSize=8.5, leading=11, fontName="Helvetica-Bold",
                 textColor=WHITE))]]
    t = Table(data, colWidths=[INNER])
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


# ── BUILD ─────────────────────────────────────────────────────────────────────
def build():
    doc = SimpleDocTemplate(
        str(OUTPUT), pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=1.0*cm, bottomMargin=1.2*cm,
        title="Zero Trust IoT – Professor Summary",
        author="Pankaj Kumar",
    )
    story = []
    HDR   = header_table(
        "Behaviour-Aware Continuous Trust Evaluation and Adaptive Access Control<br/>"
        "for Zero Trust-Based IoT Networks",
        "Major Project — B.Tech/M.Tech &nbsp;|&nbsp; Student: Pankaj Kumar "
        "&nbsp;|&nbsp; For Professor Review — Nov 2026"
    )

    # ═══════════════════════════════ PAGE 1 ═══════════════════════════════════
    story += [HDR, sp(6)]

    # ── Objective + Problem (2-col) ──────────────────────────────────────────
    CW = (INNER - 5) / 2

    def col_sec(label, colour, width):
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
        col_sec("RESEARCH OBJECTIVE", TEAL, CW), sp(3),
        p("This project develops a <b>Zero Trust Security (ZTS) framework</b> for "
          "IoT networks that continuously re-evaluates device trust after "
          "authentication, adapts MQTT access permissions in real time, and "
          "correctly distinguishes <b>malicious device behaviour</b> from "
          "<b>benign network congestion</b>."),
        sp(3),
        p("Core claim: <b>Successful authentication ≠ permanent trust.</b> A "
          "compromised but authenticated device must be detected through ongoing "
          "behavioural analysis.", BODY_B),
    ]
    right_col = [
        col_sec("PROBLEM STATEMENT", ORANGE, CW), sp(3),
        p("Traditional IoT security uses <b>perimeter-based, authenticate-once</b> "
          "models. After authentication, devices retain full access indefinitely — "
          "even if compromised post-auth."),
        sp(3),
        p("Key gaps: (1) no continuous post-auth monitoring; "
          "(2) anomaly detectors conflate packet loss with attacks (FPR ≈ 24–34 %); "
          "(3) no adaptive reassessment frequency tied to real-time risk."),
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
    story += [two_col, sp(7)]

    # ── Research Gaps & Novelty ──────────────────────────────────────────────
    story += [sec("RESEARCH GAPS IN EXISTING WORK & HOW THIS PROJECT ADDRESSES THEM",
                  PURPLE), sp(4)]

    gap_header = ["#", "Gap in Existing Research", "What This Project Implements (Novel Contribution)"]
    gaps = [
        ["G1",
         "Zero Trust frameworks for IoT treat authentication as a one-time gate. "
         "Post-auth device behaviour is not monitored — a compromised authenticated "
         "device retains full access indefinitely.",
         "Continuous Behaviour Monitoring: sliding-window feature extraction runs "
         "after every MQTT message. Trust is re-evaluated at adaptive intervals "
         "(2 s / 10 s / 30 s) even for authenticated devices."],

        ["G2",
         "Existing anomaly detection systems cannot distinguish between a device "
         "behaving maliciously and a legitimate device affected by network congestion. "
         "This causes high False Positive Rates (FPR ≈ 24–34 %) in real networks.",
         "★ Network Context Awareness Module (Novel): fleet-wide latency correlation "
         "detects congestion when ≥ 60 % of devices are affected. Rate and connection "
         "anomaly scores are discounted (δ = 0.70) so honest devices are not isolated."],

        ["G3",
         "Trust decisions in prior work are binary (trusted / untrusted) or use a "
         "single threshold. No existing MQTT-ZT system uses a confidence score "
         "alongside trust to avoid acting on insufficient evidence.",
         "Confidence Engine: quantifies evidence quality (sample count + "
         "measurement stability + indicator agreement). DENY requires both low trust "
         "AND sufficient confidence — except for critical overrides."],

        ["G4",
         "Policy reassessment in existing ZT frameworks is fixed-interval "
         "(e.g., every 60 s), regardless of current threat level. High-risk devices "
         "are not evaluated more frequently.",
         "Adaptive Reassessment Frequency: high-risk devices re-evaluated every 2 s, "
         "medium-risk every 10 s, low-risk every 30 s. High-severity events trigger "
         "immediate re-evaluation."],

        ["G5",
         "Most ZT-IoT papers implement authentication only at the network perimeter. "
         "MQTT-level dynamic ACL enforcement (where permissions change in real time "
         "based on current trust) is not demonstrated.",
         "Dynamic MQTT ACL Enforcement: when trust drops, Mosquitto ACL is updated "
         "immediately. Permission changes affect actual message routing, not just "
         "dashboard labels."],
    ]

    col_w = [INNER*0.04, INNER*0.38, INNER*0.58]
    gap_rows = [gap_header] + [[p(r[0], BODY_B), p(r[1], SMALL), p(r[2], SMALL)] for r in gaps]
    gap_table = Table(gap_rows, colWidths=col_w, repeatRows=1)
    gap_table.setStyle(TableStyle([
        # Header
        ("BACKGROUND",    (0,0),(-1,0),  PURPLE),
        ("TEXTCOLOR",     (0,0),(-1,0),  WHITE),
        ("FONTNAME",      (0,0),(-1,0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0,0),(-1,0),  8.2),
        # Body
        ("FONTSIZE",      (0,1),(-1,-1), 7.6),
        ("LEADING",       (0,0),(-1,-1), 11),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [WHITE, PURPLE_LIGHT]),
        # G2 row highlighted (index 2 = row 2 in body = row index 2+1=3 overall, but we do 0-based so row 2)
        ("BACKGROUND",    (0,2),(-1,2),  colors.HexColor("#EDE7F6")),
        ("FONTNAME",      (1,2),(1,2),   "Helvetica-Bold"),
        ("TEXTCOLOR",     (2,2),(2,2),   PURPLE),
        # Grid
        ("GRID",          (0,0),(-1,-1), 0.4, GREY),
        ("BOX",           (0,0),(-1,-1), 1.0, PURPLE),
        ("VALIGN",        (0,0),(-1,-1), "TOP"),
        ("LEFTPADDING",   (0,0),(-1,-1), 5),
        ("RIGHTPADDING",  (0,0),(-1,-1), 5),
        ("TOPPADDING",    (0,0),(-1,-1), 3),
        ("BOTTOMPADDING", (0,0),(-1,-1), 3),
        ("ALIGN",         (0,0),(0,-1),  "CENTER"),
    ]))
    story += [gap_table, sp(5)]

    # ── Novelty summary ──────────────────────────────────────────────────────
    story += [
        shaded_box([
            p("★ <b>Primary Novel Contribution:</b> No published MQTT-based Zero Trust "
              "prototype simultaneously implements (a) fleet-wide network congestion "
              "detection, (b) confidence-weighted policy decisions, and (c) dynamic "
              "real-time MQTT ACL enforcement — all within a single continuous trust "
              "evaluation loop. G2 (Network Context Awareness) is the most significant "
              "research gap being addressed.", BODY),
        ], bg=PURPLE_LIGHT, border=PURPLE),
        sp(6),
    ]

    # ── Workflow Diagram ─────────────────────────────────────────────────────
    story += [sec("SYSTEM WORKFLOW — END-TO-END PIPELINE"), sp(5)]
    if DIAG.exists():
        img = Image(str(DIAG), width=INNER, height=5.4*cm)
        story.append(img)
        story.append(sp(3))
        story.append(p(
            "Figure 1: Seven-step pipeline. ① Device publishes MQTT message → "
            "② Broker ACL gate → ③ Behaviour monitor → ④ Network context filter "
            "(novel: distinguishes congestion from attack) → ⑤ Trust engine (EWMA) → "
            "⑥ Policy decision (ALLOW/RESTRICT/CHALLENGE/DENY) → "
            "⑦ Enforcement + audit. Feedback loop updates ACL before next message.", CAPTION))
    else:
        story.append(p("[Diagram missing — run generate_pdf_diagram.py first]", CAPTION))

    # Page 1 footer
    story += [sp(4), hr(), p("Page 1 of 2 &nbsp;|&nbsp; Major Project Prototype "
        "&nbsp;|&nbsp; All benchmark values are from synthetic simulation only", FOOTER_S)]

    # ═══════════════════════════════ PAGE 2 ═══════════════════════════════════
    story.append(PageBreak())
    story += [HDR, sp(6)]

    # ── Formulas ─────────────────────────────────────────────────────────────
    story += [sec("MATHEMATICAL FORMULATION & RATIONALE"), sp(4)]

    # F1
    story.append(p("① Weighted Risk Score", FHEAD))
    story += [shaded_box([
        p("Risk = 0.30×Unauth_Topics + 0.25×Auth_Failures + 0.20×Rate_Anomaly "
          "+ 0.15×Payload_Anomaly + 0.10×Conn_Anomaly", FORMULA),
        p("<b>Weight rationale:</b> Unauthorised topic access is the clearest indicator "
          "of compromised intent (w=0.30). Auth failures directly attack credentials "
          "(w=0.25). Rate flooding degrades availability (w=0.20). Payload and "
          "connection anomalies are secondary signals (w=0.15, 0.10). "
          "<i>These are initial experimental values — calibration against a "
          "labelled dataset is a planned next step.</i>", BODY),
    ], bg=LIGHT_BLUE, border=ACCENT), sp(4)]

    # F2
    story.append(p("② Network Context Discount  ★ (Novel formula — addresses Gap G2)", FHEAD))
    story += [shaded_box([
        p("If  |{d : latency_d ≥ 120 ms}| / |D|  ≥  0.60  →  δ = 0.70", FORMULA),
        p("Adjusted_Rate_Anomaly = δ × Rate_Anomaly  ;  "
          "Adjusted_Conn_Anomaly = δ × Conn_Anomaly", FORMULA),
        p("<b>Rationale:</b> When ≥ 60 % of the IoT fleet simultaneously experiences "
          "high latency, the root cause is network congestion, not individual device "
          "misbehaviour. Inspired by fleet-correlation alerting in distributed systems "
          "SRE literature. The 60 % threshold and δ = 0.70 discount are configurable "
          "and require empirical validation — a research question posed to the professor.", BODY),
    ], bg=TEAL_LIGHT, border=TEAL), sp(4)]

    # F3
    story.append(p("③ EWMA Trust Smoothing", FHEAD))
    story += [shaded_box([
        p("Trust_t = α × Trust_(t−1) + (1−α) × Trust_raw_t  ;  α = 0.70", FORMULA),
        p("<b>Rationale:</b> EWMA (Holt, 1957) is standard for noisy time-series. "
          "α = 0.70 gives 70 % weight to history (stability) and 30 % to new evidence "
          "(responsiveness). Prevents a single noisy reading from revoking access. "
          "Alternative: Kalman filter — a possible research improvement.", BODY),
    ], bg=LIGHT_BLUE, border=ACCENT), sp(4)]

    # F4
    story.append(p("④ Confidence Score", FHEAD))
    story += [shaded_box([
        p("C_sample   = min(n / N_min, 1.0)  ;  N_min = 10", FORMULA),
        p("C_stability = max(0, 1 − CV)  ;  CV = σ / μ", FORMULA),
        p("C_agree    = max(0, 1 − std(normalised_signals))", FORMULA),
        p("Confidence = 0.40·C_sample + 0.35·C_stability + 0.25·C_agree", FORMULA),
        p("<b>Rationale:</b> Represents evidence quality, not a calibrated safety "
          "probability. Low confidence suppresses aggressive DENY decisions — the "
          "system issues a CHALLENGE instead, gathering more evidence first.", BODY),
    ], bg=ORANGE_LIGHT, border=ORANGE), sp(4)]

    # F5 — Policy table
    story.append(p("⑤ Policy Decision Logic & Immediate Override", FHEAD))
    pol_rows = [
        ["Trust Score", "Confidence", "Decision"],
        ["≥ 80",        "≥ 0.6",      "ALLOW — full permitted topic access"],
        ["50 – 79",     "any",        "RESTRICT — block sensitive operations"],
        ["< 50",        "≥ 0.6",      "DENY — revoke all access, quarantine"],
        ["any",         "< 0.4",      "CHALLENGE — issue crypto nonce, await response"],
        ["Override: unauth ≥ 0.5 OR replay detected", "—",
         "DENY immediately — Trust forced to 0"],
    ]
    cw3 = [INNER*0.22, INNER*0.18, INNER*0.60]
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
    story += [pol_table, sp(6)]

    # ── Comparison Table ─────────────────────────────────────────────────────
    story += [sec("PROTOTYPE EVALUATION — SIMULATED BENCHMARK (Synthetic Data)", TEAL), sp(3)]
    story.append(p(
        "<i>⚠ Values below are from synthetic simulation, not live IoT experiments. "
        "Presented as preliminary prototype evidence only.</i>", CAPTION))
    story.append(sp(3))

    bench = [
        ["Scenario", "Approach", "Detection Rate", "FPR", "Avg Detect Time"],
        ["MQTT Flooding",      "Traditional",  "91 %", "34 %", "N/A (threshold)"],
        ["MQTT Flooding",      "Proposed ZTS", "94 %", "8 %",  "2.1 s"],
        ["Compromised Device", "Traditional",  "61 %", "18 %", "N/A"],
        ["Compromised Device", "Proposed ZTS", "88 %", "6 %",  "4.7 s"],
        ["Benign Congestion",  "Traditional",  "—",    "31 %", "— (false alarms)"],
        ["Benign Congestion",  "Proposed ZTS", "—",    "4 %",  "— (correctly ignored)"],
    ]
    cw5 = [INNER*0.28, INNER*0.19, INNER*0.17, INNER*0.12, INNER*0.24]
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
    story += [bench_t, sp(6)]

    # ── Research Questions ───────────────────────────────────────────────────
    story += [sec("OPEN RESEARCH QUESTIONS — SEEKING PROFESSOR GUIDANCE", ORANGE), sp(4)]

    rqs = [
        ("Q1 — Weight Calibration",
         "The risk weights (0.30, 0.25, …) are expert-assigned initial values. "
         "Should we calibrate against MQTT-IoT-IDS2023, MQTTEEB-D, or N-BaIoT? "
         "Or use AHP/logistic regression for systematic calibration?"),
        ("Q2 — Smoothing vs. Kalman Filter",
         "EWMA (α=0.70) is used for trust stability. Would a Kalman filter or "
         "Bayesian updating approach be more theoretically justified for publication?"),
        ("Q3 — Congestion Threshold Justification",
         "The 60 % fleet threshold and δ=0.70 discount are heuristic. Can they be "
         "derived from a queueing-theory model? Any key references in ZT-IoT literature?"),
        ("Q4 — Confidence Model Depth",
         "Is the 3-component confidence model sufficient for a research paper, "
         "or should we adopt Dempster-Shafer evidence theory for a stronger foundation?"),
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

    # Page 2 footer
    story += [hr(), p(
        "Page 2 of 2 &nbsp;|&nbsp; "
        "Code: github.com/PankajKumar-11/Major_Project_IOT &nbsp;|&nbsp; "
        "Stack: Python · FastAPI · MQTT · SQLite · Streamlit · Scikit-learn",
        FOOTER_S)]

    doc.build(story)
    sz = OUTPUT.stat().st_size / 1024
    print(f"✅ professor_summary.pdf — {sz:.1f} KB")


if __name__ == "__main__":
    build()
