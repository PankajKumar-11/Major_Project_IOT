"""
Generates a SIMPLE, CLEAN pipeline diagram optimised for PDF embedding.
Wide aspect ratio, minimal text, large fonts — readable even at 6 cm height.
Output: assets/pdf_workflow.png
"""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

OUTPUT = Path("assets/pdf_workflow.png")
Path("assets").mkdir(exist_ok=True)

# ── Canvas: very wide, short ──────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(18, 5.5), dpi=220)
fig.patch.set_facecolor("white")
ax.set_facecolor("white")
ax.axis("off")
ax.set_xlim(0, 18)
ax.set_ylim(0, 5.5)

# ── Title row ─────────────────────────────────────────────────────────────────
ax.text(9, 5.25,
        "Zero Trust IoT — End-to-End System Workflow",
        ha="center", va="center", fontsize=14, fontweight="bold",
        color="#0D1B2A")

# ── Step definitions ──────────────────────────────────────────────────────────
# (label_top, label_bottom, border, fill)
steps = [
    ("①  Device",         "MQTT publish\n+ nonce + seq#",           "#1565C0", "#BBDEFB"),
    ("②  Auth Check",     "Credential verify\n+ ACL gate",          "#C62828", "#FFCDD2"),
    ("③  Behaviour\n     Monitor", "Rate · Payload\nReplay detect",  "#283593", "#C5CAE9"),
    ("④  Network\n     Context",   "Fleet latency\nCongestion flag", "#E65100", "#FFE0B2"),
    ("⑤  Trust Engine",   "Risk score\nEWMA smooth",                "#2E7D32", "#C8E6C9"),
    ("⑥  Policy\n     Decision",   "ALLOW / RESTRICT\nCHALLENGE / DENY", "#6A1B9A", "#E1BEE7"),
    ("⑦  Enforce\n     & Audit",   "Update ACL\nLog + Dashboard",   "#00695C", "#B2DFDB"),
]

N = len(steps)
BOX_W = 2.10
BOX_H = 2.80
GAP   = 0.08
START_X = (18 - N * BOX_W - (N - 1) * GAP) / 2
BOX_Y = 1.10   # bottom of boxes

box_centers = []

for i, (top_lbl, bot_lbl, border, fill) in enumerate(steps):
    bx = START_X + i * (BOX_W + GAP)
    cx = bx + BOX_W / 2
    box_centers.append(cx)

    # Shadow
    shadow = mpatches.FancyBboxPatch(
        (bx + 0.05, BOX_Y - 0.05), BOX_W, BOX_H,
        boxstyle="round,pad=0.10",
        fc="#BBBBBB", ec="none", zorder=1)
    ax.add_patch(shadow)

    # Main box
    box = mpatches.FancyBboxPatch(
        (bx, BOX_Y), BOX_W, BOX_H,
        boxstyle="round,pad=0.10",
        fc=fill, ec=border, linewidth=2.5, zorder=2)
    ax.add_patch(box)

    # Coloured top stripe
    stripe = mpatches.FancyBboxPatch(
        (bx, BOX_Y + BOX_H - 0.78), BOX_W, 0.78,
        boxstyle="round,pad=0.0",
        fc=border, ec="none", zorder=3)
    ax.add_patch(stripe)

    # Step label (top stripe)
    ax.text(cx, BOX_Y + BOX_H - 0.39, top_lbl,
            ha="center", va="center",
            fontsize=9.5, fontweight="bold", color="white", zorder=4)

    # Body text
    ax.text(cx, BOX_Y + (BOX_H - 0.78) / 2 + 0.05, bot_lbl,
            ha="center", va="center",
            fontsize=9.0, color="#1A237E", zorder=3,
            linespacing=1.5)

# ── Arrows between boxes ──────────────────────────────────────────────────────
arrow_y = BOX_Y + BOX_H / 2
for i in range(N - 1):
    x1 = START_X + i * (BOX_W + GAP) + BOX_W + 0.02
    x2 = START_X + (i + 1) * (BOX_W + GAP) - 0.02
    ax.annotate("",
        xy=(x2, arrow_y), xytext=(x1, arrow_y),
        arrowprops=dict(
            arrowstyle="->,head_width=0.30,head_length=0.22",
            color="#37474F", lw=2.0),
        zorder=5)

# ── Feedback loop arc (⑦ → ②) ────────────────────────────────────────────────
loop_y = BOX_Y - 0.42
x_start = box_centers[6]   # Step 7
x_end   = box_centers[1]   # Step 2

ax.annotate("",
    xy=(x_end, BOX_Y),
    xytext=(x_start, BOX_Y),
    arrowprops=dict(
        arrowstyle="->,head_width=0.28,head_length=0.22",
        color="#2E7D32", lw=2.0,
        connectionstyle=f"arc3,rad=0.38"),
    zorder=5)

# Feedback label
mx = (x_start + x_end) / 2
ax.text(mx, loop_y - 0.08,
        "⟲  Adaptive Feedback Loop  —  ACL permissions updated for every next message",
        ha="center", va="top", fontsize=8.5,
        color="#2E7D32", fontweight="bold", style="italic")

# ── Legend row ────────────────────────────────────────────────────────────────
legend = [
    ("#1565C0", "Device / MQTT"),
    ("#C62828", "Security Gate"),
    ("#283593", "Behaviour Analysis"),
    ("#E65100", "Network Context ★ Novel"),
    ("#2E7D32", "Trust Engine"),
    ("#6A1B9A", "ZT Policy"),
    ("#00695C", "Enforcement"),
]
lx = 0.4
ly = 0.46
for color, label in legend:
    circ = plt.Circle((lx + 0.14, ly), 0.12,
                       fc=color, ec="white", linewidth=1, zorder=5)
    ax.add_patch(circ)
    ax.text(lx + 0.34, ly, label,
            ha="left", va="center", fontsize=8.0, color="#263238")
    lx += 2.44

plt.tight_layout(pad=0.2)
plt.savefig(str(OUTPUT), dpi=220, bbox_inches="tight",
            facecolor="white", edgecolor="none")
plt.close()
print(f"SUCCESS → {OUTPUT}")
