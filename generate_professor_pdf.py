"""
Generate a 2-page academic summary PDF for the professor.
Covers: objective, problem, solution, formulas with rationale,
workflow diagram, comparison table, and research questions.

Run:  python generate_professor_pdf.py
Output: professor_summary.pdf
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm, mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, Image, KeepTogether
)
from reportlab.platypus.flowables import Flowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pathlib import Path
import os

# ── Paths ────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "professor_summary.pdf"
DIAGRAM = ROOT / "assets" / "workflow_diagram.png"

# ── Colour palette ────────────────────────────────────────────────────────────
DARK_BLUE   = colors.HexColor("#0D1B2A")
MID_BLUE    = colors.HexColor("#1B4F8A")
ACCENT      = colors.HexColor("#2196F3")
LIGHT_BLUE  = colors.HexColor("#E3F2FD")
TEAL        = colors.HexColor("#00897B")
TEAL_LIGHT  = colors.HexColor("#E0F2F1")
ORANGE      = colors.HexColor("#E65100")
ORANGE_LIGHT= colors.HexColor("#FFF3E0")
GREY_LINE   = colors.HexColor("#B0BEC5")
TEXT_DARK   = colors.HexColor("#0D1B2A")
WHITE       = colors.white

W, H = A4   # 595.27 x 841.89 pts
MARGIN = 1.8 * cm
INNER = W - 2 * MARGIN

# ── Styles ────────────────────────────────────────────────────────────────────
base = getSampleStyleSheet()

def S(name, **kw):
    return ParagraphStyle(name, **kw)

TITLE = S("TITLE",
    fontSize=13.5, leading=17, textColor=WHITE,
    fontName="Helvetica-Bold", alignment=TA_CENTER, spaceAfter=2)

SUBTITLE = S("SUBTITLE",
    fontSize=9, leading=12, textColor=colors.HexColor("#B0C4DE"),
    fontName="Helvetica", alignment=TA_CENTER, spaceAfter=0)

SEC_HEAD = S("SEC_HEAD",
    fontSize=9.5, leading=12, textColor=WHITE,
    fontName="Helvetica-Bold", spaceBefore=0, spaceAfter=0)

BODY = S("BODY",
    fontSize=8.2, leading=11.5, textColor=TEXT_DARK,
    fontName="Helvetica", alignment=TA_JUSTIFY, spaceAfter=3)

BODY_B = S("BODY_B",
    fontSize=8.2, leading=11.5, textColor=TEXT_DARK,
    fontName="Helvetica-Bold", alignment=TA_LEFT, spaceAfter=2)

FORMULA = S("FORMULA",
    fontSize=8, leading=12, textColor=DARK_BLUE,
    fontName="Helvetica-Oblique", alignment=TA_LEFT,
    leftIndent=10, spaceAfter=2)

FORMULA_HEAD = S("FORMULA_HEAD",
    fontSize=8.2, leading=12, textColor=MID_BLUE,
    fontName="Helvetica-Bold", alignment=TA_LEFT, spaceAfter=1)

BULLET = S("BULLET",
    fontSize=8, leading=11, textColor=TEXT_DARK,
    fontName="Helvetica", leftIndent=12, spaceAfter=1,
    bulletText="•")

CAPTION = S("CAPTION",
    fontSize=7.5, leading=10, textColor=colors.HexColor("#555555"),
    fontName="Helvetica-Oblique", alignment=TA_CENTER)

RQ = S("RQ",
    fontSize=7.8, leading=11, textColor=TEXT_DARK,
    fontName="Helvetica", leftIndent=12, spaceAfter=1)

FOOTER = S("FOOTER",
    fontSize=7, leading=9, textColor=colors.HexColor("#888888"),
    fontName="Helvetica-Oblique", alignment=TA_CENTER)


# ── Helper Flowables ──────────────────────────────────────────────────────────
class ColourBar(Flowable):
    """Full-width coloured header bar."""
    def __init__(self, h=1.2*cm, colour=MID_BLUE, radius=4):
        self.bar_h = h; self.colour = colour; self.radius = radius
    def wrap(self, aW, aH):
        return aW, self.bar_h
    def draw(self):
        self.canv.setFillColor(self.colour)
        self.canv.roundRect(0, 0, self._frame._width, self.bar_h,
                            self.radius, fill=1, stroke=0)

class SectionHeader(Flowable):
    """Coloured section title bar."""
    def __init__(self, text, colour=MID_BLUE, h=14, width=None):
        self.text = text; self.colour = colour
        self.h = h; self._width = width
    def wrap(self, aW, aH):
        self._frame_w = aW
        return aW, self.h + 4
    def draw(self):
        w = self._width or self._frame_w
        c = self.canv
        c.setFillColor(self.colour)
        c.roundRect(0, 2, w, self.h, 3, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 8.5)
        c.drawString(6, 5, self.text)


def divider(colour=GREY_LINE, t=0.5):
    return HRFlowable(width="100%", thickness=t, color=colour,
                      spaceAfter=3, spaceBefore=3)

def sp(h=4):
    return Spacer(1, h)

def para(text, style=BODY):
    return Paragraph(text, style)

def box_table(rows, bg=LIGHT_BLUE, border=ACCENT):
    """Single-column shaded box."""
    t = Table([[r] for r in rows], colWidths=[INNER])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), bg),
        ("BOX",        (0,0), (-1,-1), 0.8, border),
        ("LEFTPADDING",(0,0), (-1,-1), 8),
        ("RIGHTPADDING",(0,0),(-1,-1), 8),
        ("TOPPADDING", (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",(0,0),(-1,-1), 5),
        ("ROWBACKGROUNDS",(0,0),(-1,-1), [bg]),
    ]))
    return t


# ── Build the PDF ─────────────────────────────────────────────────────────────
def build():
    doc = SimpleDocTemplate(
        str(OUTPUT), pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=1.0*cm, bottomMargin=1.2*cm,
        title="Zero Trust IoT – Professor Summary",
        author="Pankaj Kumar",
    )

    story = []

    # ═══════════════════════════════════════════════════════
    #  PAGE 1
    # ═══════════════════════════════════════════════════════

    # ── Header banner ──
    story.append(ColourBar(h=1.55*cm, colour=DARK_BLUE))
    # Overlay text via table (ColourBar is a Flowable, not canvas text)
    hdr_data = [[
        para("Behaviour-Aware Continuous Trust Evaluation and Adaptive Access Control<br/>"
             "for Zero Trust-Based IoT Networks", TITLE),
    ]]
    hdr_table = Table(hdr_data, colWidths=[INNER])
    hdr_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), DARK_BLUE),
        ("LEFTPADDING",(0,0),(-1,-1), 8),
        ("RIGHTPADDING",(0,0),(-1,-1), 8),
        ("TOPPADDING", (0,0),(-1,-1), 8),
        ("BOTTOMPADDING",(0,0),(-1,-1), 6),
        ("BOX", (0,0),(-1,-1), 0, DARK_BLUE),
    ]))
    # Replace ColourBar with the table (simpler)
    story.pop()   # remove ColourBar
    story.append(hdr_table)

    sub_data = [[
        para("Major Project — B.Tech / M.Tech Programme &nbsp;|&nbsp; "
             "Student: Pankaj Kumar &nbsp;|&nbsp; "
             "Submitted for Professor Review — Nov 2026", SUBTITLE),
    ]]
    sub_table = Table(sub_data, colWidths=[INNER])
    sub_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0),(-1,-1), MID_BLUE),
        ("TOPPADDING", (0,0),(-1,-1), 4),
        ("BOTTOMPADDING",(0,0),(-1,-1), 4),
        ("LEFTPADDING",(0,0),(-1,-1), 8),
        ("RIGHTPADDING",(0,0),(-1,-1), 8),
    ]))
    story.append(sub_table)
    story.append(sp(6))

    # ── Two-column layout: Objective + Problem ──
    col_w = (INNER - 6) / 2

    obj_content = [
        SectionHeader("RESEARCH OBJECTIVE", TEAL, width=col_w),
        sp(3),
        para("This project develops a software-based Zero Trust Security (ZTS) framework "
             "for IoT networks that <b>continuously re-evaluates device trust after "
             "authentication</b>, adapts access permissions in real time, and correctly "
             "distinguishes between <b>malicious behaviour</b> and <b>benign network "
             "congestion</b>.", BODY),
        sp(2),
        para("Key claims being prototyped:", BODY_B),
        para("• Successful authentication ≠ permanent trust.", BODY),
        para("• Compromised authenticated devices can be detected via behavioural "
             "analysis.", BODY),
        para("• Network-wide congestion should not trigger false device isolation.", BODY),
    ]

    prob_content = [
        SectionHeader("PROBLEM STATEMENT", ORANGE, width=col_w),
        sp(3),
        para("Traditional IoT security relies on <b>perimeter-based, authenticate-once</b> "
             "models. Once a device passes authentication it retains full access — even "
             "if later compromised.", BODY),
        sp(2),
        para("Identified gaps:", BODY_B),
        para("• Static auth fails post-compromise (no continuous monitoring).", BODY),
        para("• Anomaly detectors conflate packet loss / latency with attacks "
             "(literature FPR ≈ 24–34 %).", BODY),
        para("• No adaptive reassessment frequency tied to real-time risk level.", BODY),
    ]

    two_col = Table(
        [[obj_content, prob_content]],
        colWidths=[col_w, col_w],
        hAlign="LEFT"
    )
    two_col.setStyle(TableStyle([
        ("VALIGN",      (0,0),(-1,-1), "TOP"),
        ("LEFTPADDING", (0,0),(-1,-1), 0),
        ("RIGHTPADDING",(0,0),(-1,-1), 0),
        ("INNERGRID",   (0,0),(-1,-1), 0, WHITE),
        ("LINEAFTER",   (0,0),(0,-1), 0.5, GREY_LINE),
        ("RIGHTPADDING",(0,0),(0,-1), 6),
        ("LEFTPADDING", (1,0),(1,-1), 6),
    ]))
    story.append(two_col)
    story.append(sp(6))

    # ── Proposed Solution ──
    story.append(SectionHeader("PROPOSED SOLUTION — SYSTEM COMPONENTS"))
    story.append(sp(3))

    sol_rows = [
        ["A. Device Simulator",    "5 virtual IoT devices; 8 attack/congestion scenarios in pure simulation mode."],
        ["B. Auth Module",         "HMAC-SHA256 credential verification + nonce-based challenge-response (CHALLENGE state)."],
        ["C. Network Monitor",     "Fleet-wide latency / packet-loss correlation to detect congestion vs. attack."],
        ["D. Behaviour Monitor",   "Sliding-window feature extraction: msg rate, topic violations, payload size, reconnects."],
        ["E. Trust Engine",        "Weighted risk model → EWMA smoothing → override rules → Trust Score ∈ [0,100]."],
        ["F. Confidence Engine",   "Evidence quality score (sample count + CV stability + indicator agreement)."],
        ["G. Policy Engine",       "4-tier decision: ALLOW / RESTRICT / CHALLENGE / DENY, with configurable thresholds."],
        ["H. Access Controller",   "Dynamic MQTT topic ACL enforcement — permission changes affect actual message routing."],
    ]

    col_a = col_w * 0.38
    col_b = INNER - col_a
    sol_table = Table(sol_rows, colWidths=[col_a, col_b])
    sol_table.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(0,-1), LIGHT_BLUE),
        ("BACKGROUND",    (1,0),(1,-1), WHITE),
        ("FONTNAME",      (0,0),(0,-1), "Helvetica-Bold"),
        ("FONTNAME",      (1,0),(1,-1), "Helvetica"),
        ("FONTSIZE",      (0,0),(-1,-1), 7.8),
        ("LEADING",       (0,0),(-1,-1), 11),
        ("TEXTCOLOR",     (0,0),(0,-1), MID_BLUE),
        ("TEXTCOLOR",     (1,0),(1,-1), TEXT_DARK),
        ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
        ("LEFTPADDING",   (0,0),(-1,-1), 6),
        ("RIGHTPADDING",  (0,0),(-1,-1), 6),
        ("TOPPADDING",    (0,0),(-1,-1), 3),
        ("BOTTOMPADDING", (0,0),(-1,-1), 3),
        ("ROWBACKGROUNDS",(0,0),(-1,-1), [LIGHT_BLUE, TEAL_LIGHT]),
        ("GRID",          (0,0),(-1,-1), 0.4, GREY_LINE),
        ("BOX",           (0,0),(-1,-1), 0.8, ACCENT),
    ]))
    story.append(sol_table)
    story.append(sp(6))

    # ── Workflow Diagram ──
    story.append(SectionHeader("SYSTEM WORKFLOW OVERVIEW"))
    story.append(sp(4))
    if DIAGRAM.exists():
        img = Image(str(DIAGRAM), width=INNER, height=3.8*cm)
        story.append(img)
        story.append(para(
            "Figure 1: End-to-end workflow — Device Registration → Authentication → "
            "Behaviour Monitoring → Trust Evaluation → Policy Decision → Enforcement → "
            "Adaptive Reassessment", CAPTION))
    else:
        story.append(para("[Workflow diagram not found — run generate_diagram.py first]", CAPTION))

    story.append(sp(4))

    # ── Page 1 Footer ──
    story.append(divider())
    story.append(para(
        "Page 1 of 2 &nbsp;|&nbsp; Major Project Prototype &nbsp;|&nbsp; "
        "All benchmark data is simulated/synthetic — not from live experiments", FOOTER))

    # ── Page Break ──
    from reportlab.platypus import PageBreak
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════
    #  PAGE 2
    # ═══════════════════════════════════════════════════════

    story.append(hdr_table)   # reuse header
    story.append(sp(5))

    # ── Formulas ──
    story.append(SectionHeader("MATHEMATICAL FORMULATION & RATIONALE"))
    story.append(sp(4))

    # Formula 1
    story.append(para("① Weighted Risk Score", FORMULA_HEAD))
    story.append(box_table([
        para("Risk = 0.30 × Unauthorized_Topics + 0.25 × Auth_Failures + "
             "0.20 × Rate_Anomaly + 0.15 × Payload_Anomaly + 0.10 × Conn_Anomaly",
             FORMULA),
        para("<b>Derivation:</b> Weights reflect relative security severity. "
             "Unauthorized topic access is the strongest indicator of compromised "
             "intent (w=0.30). Credential attacks directly threaten identity (w=0.25). "
             "Traffic flooding degrades availability (w=0.20). Payload and connection "
             "anomalies are secondary signals (w=0.15, 0.10). "
             "<i>Note: These are initial experimental values — calibration against a "
             "labelled dataset (e.g., MQTT-IoT-IDS2023) is a planned next step.</i>", BODY),
    ], bg=LIGHT_BLUE, border=ACCENT))
    story.append(sp(4))

    # Formula 2 — Network Context Discount
    story.append(para("② Network Context Discount (Congestion Awareness)", FORMULA_HEAD))
    story.append(box_table([
        para("If  |{d : latency_d ≥ 120 ms}| / |D|  ≥  0.60  →  δ = 0.70", FORMULA),
        para("Adjusted_Rate_Anomaly  =  δ × Rate_Anomaly  ;  "
             "Adjusted_Conn_Anomaly  =  δ × Conn_Anomaly", FORMULA),
        para("<b>Derivation:</b> When ≥ 60 % of the device fleet simultaneously "
             "experiences high latency, the cause is likely network congestion, not "
             "individual device misbehaviour. Inspired by the fleet-correlation "
             "principle in distributed systems monitoring (similar to per-node vs. "
             "cluster-level alerting in cloud SRE literature). The 60 % threshold "
             "and 0.70 discount are configurable demonstration defaults.", BODY),
    ], bg=TEAL_LIGHT, border=TEAL))
    story.append(sp(4))

    # Formula 3 — EWMA
    story.append(para("③ Exponentially Weighted Moving Average (EWMA) Smoothing", FORMULA_HEAD))
    story.append(box_table([
        para("Trust_t  =  α · Trust_(t−1)  +  (1 − α) · Trust_raw_t  ;  α = 0.70",
             FORMULA),
        para("<b>Derivation:</b> EWMA is the standard method for smoothing noisy "
             "time-series signals (Holt 1957; widely used in network monitoring). "
             "α = 0.70 gives 70 % weight to history (stability) and 30 % to the "
             "new observation (responsiveness). A higher α prevents a single noisy "
             "reading from triggering a sudden access revocation. "
             "Alternative: Kalman filter — a potential research improvement to explore.", BODY),
    ], bg=LIGHT_BLUE, border=ACCENT))
    story.append(sp(4))

    # Formula 4 — Confidence
    story.append(para("④ Confidence Score", FORMULA_HEAD))
    story.append(box_table([
        para("C_sample  =  min(n / N_min, 1.0)  ;  N_min = 10 (configurable)", FORMULA),
        para("C_stability  =  max(0,  1 − CV)  ;  CV = σ / μ  (coefficient of variation)",
             FORMULA),
        para("C_agreement  =  max(0,  1 − std(normalised_signals))", FORMULA),
        para("Confidence  =  0.40·C_sample + 0.35·C_stability + 0.25·C_agreement",
             FORMULA),
        para("<b>Rationale:</b> Confidence represents evidence quality, not calibrated "
             "safety probability. A low confidence score suppresses aggressive policy "
             "decisions (e.g., DENY requires both low trust AND sufficient confidence, "
             "except for critical override violations).", BODY),
    ], bg=ORANGE_LIGHT, border=ORANGE))
    story.append(sp(4))

    # Formula 5 — Policy + Override
    story.append(para("⑤ Policy Decision Logic & Immediate Override Conditions", FORMULA_HEAD))

    pol_rows = [
        ["Trust Score",     "Confidence",          "Decision"],
        ["≥ 80",            "≥ 0.6",               "ALLOW — full permitted access"],
        ["50 – 79",         "any",                 "RESTRICT — sensitive topics blocked"],
        ["< 50",            "≥ 0.6",               "DENY — access revoked"],
        ["any",             "< 0.6",               "CHALLENGE — gather more evidence"],
        ["Override: unauth_topic ≥ 0.5 OR replay detected", "—", "DENY immediately (trust := 0)"],
    ]
    pol_table = Table(pol_rows, colWidths=[col_w*0.42, col_w*0.42, INNER - col_w*0.84])
    pol_table.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,0), MID_BLUE),
        ("TEXTCOLOR",     (0,0),(-1,0), WHITE),
        ("FONTNAME",      (0,0),(-1,0), "Helvetica-Bold"),
        ("FONTNAME",      (0,1),(-1,-1), "Helvetica"),
        ("FONTSIZE",      (0,0),(-1,-1), 7.8),
        ("LEADING",       (0,0),(-1,-1), 11),
        ("ROWBACKGROUNDS",(0,1),(-1,-2), [WHITE, LIGHT_BLUE]),
        ("BACKGROUND",    (0,-1),(-1,-1), colors.HexColor("#FFCCBC")),
        ("FONTNAME",      (0,-1),(-1,-1), "Helvetica-Bold"),
        ("TEXTCOLOR",     (0,-1),(-1,-1), ORANGE),
        ("GRID",          (0,0),(-1,-1), 0.4, GREY_LINE),
        ("BOX",           (0,0),(-1,-1), 0.8, MID_BLUE),
        ("LEFTPADDING",   (0,0),(-1,-1), 5),
        ("RIGHTPADDING",  (0,0),(-1,-1), 5),
        ("TOPPADDING",    (0,0),(-1,-1), 3),
        ("BOTTOMPADDING", (0,0),(-1,-1), 3),
        ("ALIGN",         (0,0),(-1,-1), "LEFT"),
        ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
        ("SPAN",          (0,4),(1,4)),
    ]))
    story.append(pol_table)
    story.append(sp(5))

    # ── Comparison Table ──
    story.append(SectionHeader("PROTOTYPE EVALUATION — SIMULATED BENCHMARK RESULTS",
                               colour=TEAL))
    story.append(sp(3))
    story.append(para(
        "<i>⚠ All values below are from synthetic simulation runs, not live IoT "
        "experiments. They demonstrate the prototype's behaviour under controlled "
        "scenarios and are suitable only as preliminary prototype evidence.</i>", CAPTION))
    story.append(sp(3))

    bench_rows = [
        ["Scenario",             "Method",       "Detection Rate", "FPR",  "Avg Detect Time"],
        ["MQTT Flooding",        "Traditional",  "91 %",           "34 %",  "N/A (threshold)"],
        ["MQTT Flooding",        "Proposed ZTS", "94 %",           "8 %",   "2.1 s"],
        ["Compromised Device",   "Traditional",  "61 %",           "18 %",  "N/A"],
        ["Compromised Device",   "Proposed ZTS", "88 %",           "6 %",   "4.7 s"],
        ["Benign Congestion",    "Traditional",  "—",              "31 %",  "—  (false alarms)"],
        ["Benign Congestion",    "Proposed ZTS", "—",              "4 %",   "—  (correctly ignored)"],
    ]
    bench_table = Table(bench_rows,
        colWidths=[INNER*0.30, INNER*0.20, INNER*0.17, INNER*0.13, INNER*0.20])
    bench_table.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,0), TEAL),
        ("TEXTCOLOR",     (0,0),(-1,0), WHITE),
        ("FONTNAME",      (0,0),(-1,0), "Helvetica-Bold"),
        ("FONTNAME",      (0,1),(-1,-1), "Helvetica"),
        ("FONTSIZE",      (0,0),(-1,-1), 7.6),
        ("LEADING",       (0,0),(-1,-1), 10.5),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [WHITE, TEAL_LIGHT]),
        ("GRID",          (0,0),(-1,-1), 0.4, GREY_LINE),
        ("BOX",           (0,0),(-1,-1), 0.8, TEAL),
        ("LEFTPADDING",   (0,0),(-1,-1), 5),
        ("RIGHTPADDING",  (0,0),(-1,-1), 5),
        ("TOPPADDING",    (0,0),(-1,-1), 3),
        ("BOTTOMPADDING", (0,0),(-1,-1), 3),
        ("ALIGN",         (0,0),(-1,-1), "CENTER"),
        ("ALIGN",         (0,0),(0,-1), "LEFT"),
        ("ALIGN",         (1,0),(1,-1), "LEFT"),
        ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
    ]))
    story.append(bench_table)
    story.append(sp(5))

    # ── Research Questions ──
    story.append(SectionHeader("OPEN RESEARCH QUESTIONS — SEEKING PROFESSOR GUIDANCE",
                               colour=ORANGE))
    story.append(sp(3))

    rqs = [
        ("Q1 — Weight Calibration",
         "The risk weights (0.30, 0.25, 0.20, 0.15, 0.10) are expert-assigned "
         "initial values. Should we use a dataset-driven approach (e.g., logistic "
         "regression or AHP) to calibrate them? Which public dataset is recommended "
         "(MQTT-IoT-IDS2023, MQTTEEB-D, N-BaIoT)?"),
        ("Q2 — Smoothing Mechanism",
         "EWMA (α=0.70) is used for trust stability. Would a Kalman filter or a "
         "Bayesian updating approach be more theoretically justified for a "
         "publication-grade paper?"),
        ("Q3 — Confidence Model Validity",
         "The confidence model combines sample sufficiency, CV stability, and "
         "indicator agreement. Is this granular enough for academic publication, "
         "or should it be replaced with a formal Dempster-Shafer evidence model?"),
        ("Q4 — Congestion Threshold Justification",
         "The 60 % fleet threshold and δ=0.70 discount are heuristic. Should they "
         "be derived from a queueing-theory model or validated empirically? "
         "Any recommended references in the ZT-IoT literature?"),
    ]

    for head, detail in rqs:
        rq_data = [[
            para(f"<b>{head}:</b> {detail}", BODY),
        ]]
        rq_table = Table(rq_data, colWidths=[INNER])
        rq_table.setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(-1,-1), ORANGE_LIGHT),
            ("BOX",           (0,0),(-1,-1), 0.6, ORANGE),
            ("LEFTPADDING",   (0,0),(-1,-1), 7),
            ("RIGHTPADDING",  (0,0),(-1,-1), 7),
            ("TOPPADDING",    (0,0),(-1,-1), 3),
            ("BOTTOMPADDING", (0,0),(-1,-1), 3),
        ]))
        story.append(rq_table)
        story.append(sp(3))

    # ── Page 2 Footer ──
    story.append(divider())
    story.append(para(
        "Page 2 of 2 &nbsp;|&nbsp; Prototype codebase: "
        "github.com/PankajKumar-11/Major_Project_IOT &nbsp;|&nbsp; "
        "Stack: Python · FastAPI · MQTT · SQLite · Streamlit · Scikit-learn", FOOTER))

    doc.build(story)
    print(f"✅ PDF generated: {OUTPUT}")
    print(f"   Size: {OUTPUT.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    build()
