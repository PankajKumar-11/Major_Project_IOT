"""
Generates a crisp, ultra-clean pipeline diagram optimized for the single-page PDF.
No lines overlapping text. Clear orthogonal feedback loop underneath.
Output: assets/pdf_workflow.png
"""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

OUTPUT = Path("assets/pdf_workflow.png")
Path("assets").mkdir(exist_ok=True)

# 18 x 5 aspect ratio canvas
fig, ax = plt.subplots(figsize=(18, 4.8), dpi=220)
fig.patch.set_facecolor("white")
ax.set_facecolor("white")
ax.axis("off")
ax.set_xlim(0, 18)
ax.set_ylim(0, 4.8)

# Title
ax.text(9, 4.5, "Zero Trust IoT Architecture — Operational Flow Pipeline", 
        ha="center", va="center", fontsize=13, fontweight="bold", color="#0D1B2A")

# Steps definition
steps = [
    ("Step 1: Ingestion",  "MQTT Publish\nSensor Telemetry\nFresh Nonce",       "#1565C0", "#E3F2FD"),
    ("Step 2: Gatekeeper", "Broker ACL Gate\nIdentity Check\nPre-Auth Filter",  "#C62828", "#FFEBEE"),
    ("Step 3: Behaviour",  "Sliding Window\nRate & Payload Jitter\nReplay Detect", "#283593", "#E8EAF6"),
    ("Step 4: Net Context","Fleet Correlation\nCongestion Filter\n[Novel: FPR Drop]", "#E65100", "#FFF3E0"),
    ("Step 5: Trust Eng.", "Weighted Risk Model\nEWMA Smoothing\nOverride Rules", "#2E7D32", "#E8F5E9"),
    ("Step 6: ZT Policy",  "ALLOW / RESTRICT\nCHALLENGE / DENY\nAdaptive Interval", "#6A1B9A", "#F3E5F5"),
    ("Step 7: Enforce",    "Dynamic ACL Sync\nBroker Enforcement\nAudit Trail Logging", "#00695C", "#E0F2F1"),
]

N = len(steps)
BOX_W = 2.15
BOX_H = 2.40
GAP = 0.18
TOTAL_W = N * BOX_W + (N - 1) * GAP
START_X = (18 - TOTAL_W) / 2
BOX_Y = 1.35  # elevated to give plenty of clean space underneath for feedback loop

box_centers = []

for i, (title, desc, border_col, bg_col) in enumerate(steps):
    bx = START_X + i * (BOX_W + GAP)
    cx = bx + BOX_W / 2
    box_centers.append(cx)

    # Shadow
    shadow = mpatches.FancyBboxPatch(
        (bx + 0.04, BOX_Y - 0.04), BOX_W, BOX_H,
        boxstyle="round,pad=0.06",
        fc="#D0D7DE", ec="none", zorder=1)
    ax.add_patch(shadow)

    # Box
    box = mpatches.FancyBboxPatch(
        (bx, BOX_Y), BOX_W, BOX_H,
        boxstyle="round,pad=0.06",
        fc=bg_col, ec=border_col, linewidth=2.0, zorder=2)
    ax.add_patch(box)

    # Header banner
    stripe_h = 0.55
    stripe = mpatches.FancyBboxPatch(
        (bx, BOX_Y + BOX_H - stripe_h), BOX_W, stripe_h,
        boxstyle="round,pad=0.0",
        fc=border_col, ec="none", zorder=3)
    ax.add_patch(stripe)

    # Header text
    ax.text(cx, BOX_Y + BOX_H - stripe_h/2, title,
            ha="center", va="center", fontsize=8.5, fontweight="bold",
            color="white", zorder=4)

    # Body text
    ax.text(cx, BOX_Y + (BOX_H - stripe_h)/2 + 0.02, desc,
            ha="center", va="center", fontsize=7.8, color="#1E293B",
            zorder=4, linespacing=1.35)

# Forward arrows between boxes
arrow_y = BOX_Y + BOX_H / 2
for i in range(N - 1):
    x1 = START_X + i * (BOX_W + GAP) + BOX_W
    x2 = START_X + (i + 1) * (BOX_W + GAP)
    ax.annotate("",
        xy=(x2 - 0.02, arrow_y), xytext=(x1 + 0.02, arrow_y),
        arrowprops=dict(
            arrowstyle="->,head_width=0.25,head_length=0.22",
            color="#334155", lw=1.8),
        zorder=5)

# ── Clean Feedback Loop UNDERNEATH the boxes (No overlap!) ────────────────────
# Orthogonal path: Step 7 bottom -> down -> left -> up to Step 2 bottom
x_from = box_centers[6]
x_to   = box_centers[1]
y_bottom = BOX_Y
y_track  = 0.45

# Draw clean orthogonal path
ax.plot([x_from, x_from], [y_bottom, y_track], color="#059669", lw=1.8, zorder=5)
ax.plot([x_from, x_to],   [y_track, y_track], color="#059669", lw=1.8, zorder=5)
ax.annotate("",
    xy=(x_to, y_bottom), xytext=(x_to, y_track),
    arrowprops=dict(
        arrowstyle="->,head_width=0.25,head_length=0.22",
        color="#059669", lw=1.8),
    zorder=5)

# Label on the feedback line
ax.text((x_from + x_to)/2, y_track + 0.16,
        "⟲ Continuous Feedback Loop: Real-time ACL Permission Updates Enforced on Broker",
        ha="center", va="bottom", fontsize=8.2, fontweight="bold",
        color="#047857", style="italic", zorder=6)

plt.tight_layout(pad=0.2)
plt.savefig(str(OUTPUT), dpi=220, bbox_inches="tight", facecolor="white")
plt.close()
print(f"SUCCESS: Generated clean pipeline diagram at {OUTPUT}")
