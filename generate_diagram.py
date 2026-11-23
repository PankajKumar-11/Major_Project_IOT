"""
Generates a clean, readable, vertical academic flowchart diagram.
One step per row, wide boxes, clear labels, big fonts.
Run:  python generate_diagram.py
Output: assets/workflow_diagram.png
"""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch

OUTPUT_DIR = Path("assets")
OUTPUT_DIR.mkdir(exist_ok=True)
OUTPUT_PATH = OUTPUT_DIR / "workflow_diagram.png"

# ── Canvas ────────────────────────────────────────────────────────────────────
FIG_W, FIG_H = 14, 20
fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=200)
fig.patch.set_facecolor("white")
ax.set_facecolor("white")
ax.axis("off")
ax.set_xlim(0, 14)
ax.set_ylim(0, 20)

# ── Design tokens ─────────────────────────────────────────────────────────────
COLORS = {
    "blue":    "#1565C0",
    "red":     "#C62828",
    "indigo":  "#283593",
    "amber":   "#E65100",
    "green":   "#2E7D32",
    "purple":  "#6A1B9A",
    "teal":    "#00695C",
    "navy":    "#0D1B2A",
    "arrow":   "#37474F",
}
LBOX = 1.2   # left x of box
RBOX = 12.8  # right x
BOX_W = RBOX - LBOX
BOX_H = 1.55  # normal box height
GAP   = 0.52  # gap between boxes

# ── Helper: rounded box + text ────────────────────────────────────────────────
def draw_box(ax, x, y, w, h, bg, border, step_num, step_title, body_lines,
             title_color=None):
    """Draw a step box. y = bottom-left corner."""
    tc = title_color or border
    # Shadow
    shadow = mpatches.FancyBboxPatch(
        (x + 0.07, y - 0.07), w, h,
        boxstyle="round,pad=0.08",
        fc="#CCCCCC", ec="none", zorder=1)
    ax.add_patch(shadow)
    # Main box
    box = mpatches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.08",
        fc=bg, ec=border, linewidth=2.2, zorder=2)
    ax.add_patch(box)
    # Step badge (left coloured circle)
    badge_x = x + 0.42
    badge_y = y + h / 2
    circ = plt.Circle((badge_x, badge_y), 0.30,
                       fc=border, ec="white", linewidth=1.5, zorder=3)
    ax.add_patch(circ)
    ax.text(badge_x, badge_y, str(step_num),
            ha="center", va="center", fontsize=11,
            fontweight="bold", color="white", zorder=4)
    # Title
    ax.text(x + 0.90, y + h * 0.72, step_title,
            ha="left", va="center", fontsize=11.5,
            fontweight="bold", color=tc, zorder=3)
    # Body lines
    if isinstance(body_lines, str):
        body_lines = [body_lines]
    line_y = y + h * 0.72 - 0.32
    for line in body_lines:
        ax.text(x + 0.90, line_y, line,
                ha="left", va="top", fontsize=9.0,
                color="#263238", zorder=3, linespacing=1.4)
        line_y -= 0.265

def draw_arrow(ax, x1, y1, x2, y2, color="#37474F", label=""):
    ax.annotate("",
        xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(
            arrowstyle="->,head_width=0.35,head_length=0.28",
            color=color, lw=2.0),
        zorder=5)
    if label:
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax.text(mx + 0.15, my, label,
                ha="left", va="center",
                fontsize=8, color=color, style="italic", zorder=5)

def draw_diamond(ax, cx, cy, w, h, bg, border, text_lines):
    """Draw a decision diamond."""
    dx, dy = w/2, h/2
    pts = [(cx, cy+dy), (cx+dx, cy), (cx, cy-dy), (cx-dx, cy)]
    diamond = mpatches.Polygon(pts, closed=True,
                               fc=bg, ec=border, linewidth=2.2, zorder=2)
    ax.add_patch(diamond)
    if isinstance(text_lines, str):
        text_lines = [text_lines]
    for i, t in enumerate(text_lines):
        offset = (len(text_lines)-1) * 0.14 - i * 0.28
        ax.text(cx, cy + offset, t,
                ha="center", va="center",
                fontsize=9.5, fontweight="bold",
                color=border, zorder=3)

# ── TITLE ─────────────────────────────────────────────────────────────────────
ax.text(7, 19.65,
        "Behaviour-Aware Zero Trust Security — System Workflow",
        ha="center", va="top", fontsize=14.5,
        fontweight="bold", color=COLORS["navy"])
ax.text(7, 19.28,
        "End-to-end flow: from IoT device message → authentication → monitoring → "
        "trust evaluation → policy decision → enforcement",
        ha="center", va="top", fontsize=9.5, color="#546E7A", style="italic")

# ── STEP DEFINITIONS ──────────────────────────────────────────────────────────
# (step_num, title, body_lines, border_color, bg_color)
steps = [
    # y will be computed bottom-up; we lay them top→bottom
    (1, "IoT Device Publishes Message",
     ["Device sends MQTT message: payload + sequence number + nonce",
      "Device ID must match a registered credential in the database"],
     COLORS["blue"], "#E3F2FD"),

    (2, "Broker Gatekeeper — Real-time ACL Check",
     ["Is this device currently ALLOWED or DENIED?",
      "Is the topic in the device's permitted topic list?",
      "If DENIED or wrong topic → block message immediately, log alert"],
     COLORS["red"], "#FFEBEE"),

    (3, "Device Behaviour Monitor (Sliding Window)",
     ["Collects features over last N seconds per device:",
      "• Message rate  • Payload size variance  • Reconnection count",
      "• Failed auth attempts  • Unauthorized topic access count",
      "• Duplicate nonce / replay sequence detection"],
     COLORS["indigo"], "#E8EAF6"),

    (4, "Network Monitor — Fleet-wide Health Check",
     ["Measures latency, packet loss, broker delay across ALL devices simultaneously",
      "If ≥ 60% of devices show high latency → Network Congestion Flag raised",
      "→ Rate and connection anomaly scores discounted by 30% (δ = 0.70)",
      "Purpose: avoid falsely blaming honest devices for slow network"],
     COLORS["amber"], "#FFF3E0"),

    (5, "Trust & Confidence Calculation",
     ["Risk  =  0.30×Unauth_Topics + 0.25×Auth_Failures + 0.20×Rate_Anomaly",
      "         + 0.15×Payload_Anomaly + 0.10×Conn_Anomaly",
      "Trust_raw  =  100 × (1 − Risk)",
      "Trust_t    =  0.70 × Trust_(t−1) + 0.30 × Trust_raw   [EWMA smoothing]",
      "Confidence =  sample sufficiency + stability (CV) + indicator agreement",
      "Override:  unauth ≥ 0.5 OR replay detected → Trust := 0  immediately"],
     COLORS["green"], "#E8F5E9"),
]

# Layout: start drawing from top (y=18.8), going down
TOP_Y  = 18.80
cur_y  = TOP_Y
BOX_H2 = BOX_H  # may vary per step

step_bottoms = []   # track bottom y of each step box for arrows

for i, (num, title, body, border, bg) in enumerate(steps):
    # Taller box for steps with more body lines
    h = max(BOX_H, 0.28 * len(body) + 0.80)
    bottom = cur_y - h
    draw_box(ax, LBOX, bottom, BOX_W, h, bg, border, num, title, body)
    step_bottoms.append((LBOX + BOX_W/2, bottom, bottom + h))  # cx, bottom, top
    # Arrow from previous step
    if i > 0:
        px, pb, pt = step_bottoms[i-1]
        cx, cb, ct = step_bottoms[i]
        draw_arrow(ax, px, pb, cx, ct)
    cur_y = bottom - GAP

# ── POLICY DECISION DIAMOND ───────────────────────────────────────────────────
diamond_cx = 7.0
diamond_top = cur_y
diamond_cy  = cur_y - 1.05
draw_arrow(ax, 7.0, step_bottoms[-1][1], 7.0, diamond_cy + 1.05)

draw_diamond(ax, diamond_cx, diamond_cy, 5.6, 2.1,
             "#F3E5F5", COLORS["purple"],
             ["STEP 6: Policy Decision", "What is the Trust Score?"])
cur_y = diamond_cy - 1.1

# ── 4 OUTCOME BOXES side by side ──────────────────────────────────────────────
outcome_y = cur_y - 2.15
out_w = 2.65
out_h = 2.00
spacing = 0.22
total_w = 4 * out_w + 3 * spacing
start_x = (14 - total_w) / 2

outcomes = [
    ("ALLOW",     "Trust ≥ 80\nConfidence ≥ 0.6",
     "Full access to\nall permitted topics.\nRe-evaluate in 30 s.",
     COLORS["green"], "#E8F5E9"),
    ("RESTRICT",  "Trust 50–79",
     "Block sensitive topics\n(e.g. motor commands).\nRe-evaluate in 10 s.",
     COLORS["amber"], "#FFF3E0"),
    ("CHALLENGE", "Confidence < 0.4",
     "Issue crypto nonce\nchallenge. Wait for\ndevice to respond.",
     COLORS["indigo"], "#E8EAF6"),
    ("DENY",      "Trust < 50\nor Override",
     "Revoke all access.\nQuarantine device.\nRe-evaluate in 2 s.",
     COLORS["red"], "#FFEBEE"),
]

out_centers = []
for j, (label, cond, action, border, bg) in enumerate(outcomes):
    bx = start_x + j * (out_w + spacing)
    by = outcome_y
    # Shadow
    shadow = mpatches.FancyBboxPatch(
        (bx+0.06, by-0.06), out_w, out_h,
        boxstyle="round,pad=0.08", fc="#CCCCCC", ec="none", zorder=1)
    ax.add_patch(shadow)
    # Box
    box = mpatches.FancyBboxPatch(
        (bx, by), out_w, out_h,
        boxstyle="round,pad=0.08",
        fc=bg, ec=border, linewidth=2.2, zorder=2)
    ax.add_patch(box)
    # Header stripe
    stripe = mpatches.FancyBboxPatch(
        (bx, by + out_h - 0.52), out_w, 0.52,
        boxstyle="round,pad=0.0",
        fc=border, ec="none", zorder=3)
    ax.add_patch(stripe)
    ax.text(bx + out_w/2, by + out_h - 0.26, label,
            ha="center", va="center", fontsize=10.5,
            fontweight="bold", color="white", zorder=4)
    ax.text(bx + out_w/2, by + out_h - 0.70, cond,
            ha="center", va="top", fontsize=8.0,
            fontweight="bold", color=border, zorder=3)
    ax.text(bx + out_w/2, by + 0.65, action,
            ha="center", va="center", fontsize=8.2,
            color="#263238", zorder=3, linespacing=1.5)
    cx_out = bx + out_w/2
    out_centers.append(cx_out)
    # Arrow from diamond
    draw_arrow(ax, diamond_cx, diamond_cy - 1.05,
               cx_out, by + out_h,
               color=border)
    # Label on arrow
    lbls = ["ALLOW", "RESTRICT", "CHALLENGE", "DENY"]
    ax.text(cx_out, by + out_h + 0.14, lbls[j],
            ha="center", va="bottom", fontsize=7.5,
            color=border, fontweight="bold")

# ── STEP 7: Enforcement box ───────────────────────────────────────────────────
enf_y = outcome_y - 0.55 - BOX_H - 0.2
enf_h = 1.42
draw_box(ax, LBOX, enf_y, BOX_W, enf_h,
         "#E3F2FD", COLORS["teal"], 7,
         "Enforcement & Audit Trail",
         ["Update Mosquitto ACL file → permissions take effect for NEXT message immediately",
          "Log security event to SQLite database  •  Push update to SOC Dashboard",
          "Trigger next trust re-evaluation at adaptive interval (2 s / 10 s / 30 s)"],
         title_color=COLORS["teal"])

enf_cx = LBOX + BOX_W/2
enf_top = enf_y + enf_h
# Arrows from all outcome boxes down to enforcement
for cx_out in out_centers:
    ax.annotate("",
        xy=(enf_cx, enf_top),
        xytext=(cx_out, outcome_y),
        arrowprops=dict(
            arrowstyle="->,head_width=0.25,head_length=0.22",
            color=COLORS["teal"], lw=1.4,
            connectionstyle="arc3,rad=0.0"),
        zorder=5)

# ── FEEDBACK LOOP arrow ───────────────────────────────────────────────────────
# From Step 7 (enforcement) back up to Step 2 (Broker Gatekeeper)
broker_top = step_bottoms[1][2]   # top y of step 2
broker_cx  = step_bottoms[1][0]

ax.annotate("",
    xy=(LBOX - 0.35, broker_top - 0.4),
    xytext=(LBOX - 0.35, enf_y + enf_h * 0.5),
    arrowprops=dict(
        arrowstyle="->,head_width=0.35,head_length=0.28",
        color=COLORS["green"], lw=2.2,
        connectionstyle="arc3,rad=0.0"),
    zorder=5)
# Horizontal stub to box
ax.plot([LBOX - 0.35, LBOX], [broker_top - 0.40, broker_top - 0.40],
        color=COLORS["green"], lw=2.2, zorder=5)
# Left side vertical line
ax.plot([LBOX - 0.35, LBOX - 0.35], [enf_y + enf_h*0.5, broker_top - 0.40],
        color=COLORS["green"], lw=2.2, zorder=5)
# Stub from enforcement
ax.plot([LBOX - 0.35, LBOX], [enf_y + enf_h*0.5, enf_y + enf_h*0.5],
        color=COLORS["green"], lw=2.2, zorder=5)
ax.text(LBOX - 0.42, (broker_top + enf_y + enf_h*0.5)/2,
        "FEEDBACK\nLOOP",
        ha="right", va="center", fontsize=8.5,
        fontweight="bold", color=COLORS["green"],
        rotation=90)

# ── LEGEND ────────────────────────────────────────────────────────────────────
legend_y = enf_y - 0.65
legend_items = [
    (COLORS["blue"],   "Device / MQTT Layer"),
    (COLORS["indigo"], "Behaviour Analysis"),
    (COLORS["amber"],  "Network Context Awareness"),
    (COLORS["green"],  "Trust Engine / Enforcement"),
    (COLORS["purple"], "Policy Decision"),
    (COLORS["red"],    "Security Violation / DENY"),
]
ax.text(7, legend_y + 0.02, "Legend", ha="center", va="bottom",
        fontsize=9, color="#37474F", fontweight="bold")
lx = 0.9
for color, label in legend_items:
    circ = plt.Circle((lx + 0.18, legend_y - 0.22), 0.14,
                      fc=color, ec="white", linewidth=1, zorder=5)
    ax.add_patch(circ)
    ax.text(lx + 0.42, legend_y - 0.22, label,
            ha="left", va="center", fontsize=8, color="#263238")
    lx += 2.15

# ── SAVE ──────────────────────────────────────────────────────────────────────
plt.tight_layout(pad=0.3)
plt.savefig(str(OUTPUT_PATH), dpi=200, bbox_inches="tight",
            facecolor="white", edgecolor="none")
plt.close()
print(f"SUCCESS: Diagram saved → {OUTPUT_PATH}")
