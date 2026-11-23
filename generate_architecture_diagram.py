"""
Generates a publication-grade, pristine system architecture and workflow diagram
for the Zero Trust IoT research project.
Designed with distinct architectural layers, clear flow annotations,
and zero visual overlap.

Output: assets/architecture_workflow.png
"""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

OUTPUT_DIR = Path("assets")
OUTPUT_DIR.mkdir(exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "architecture_workflow.png"

# Canvas: 16 x 7.5 ratio for crisp publication embedding
fig, ax = plt.subplots(figsize=(16, 7.6), dpi=250)
fig.patch.set_facecolor("#FFFFFF")
ax.set_facecolor("#FFFFFF")
ax.axis("off")
ax.set_xlim(0, 16)
ax.set_ylim(0, 7.6)

# Palette
DARK_NAVY = "#0F172A"
BLUE      = "#1E40AF"
BLUE_BG   = "#EFF6FF"
TEAL      = "#0F766E"
TEAL_BG   = "#F0FDFA"
PURPLE    = "#6B21A8"
PURPLE_BG = "#FAF5FF"
AMBER     = "#C2410C"
AMBER_BG  = "#FFF7ED"
GREEN     = "#15803D"
GREEN_BG  = "#F0FDF4"
RED       = "#B91C1C"
RED_BG    = "#FEF2F2"
BORDER    = "#CBD5E1"
LINE_DARK = "#334155"

# Title Bar
ax.text(8.0, 7.3, "Continuous Zero Trust Security Framework — Operational Architecture & Pipeline",
        ha="center", va="center", fontsize=12.5, fontweight="bold", color=DARK_NAVY)
ax.text(8.0, 6.95, "Dual-stream monitoring separates device anomaly evaluation from network congestion before adaptive ACL enforcement",
        ha="center", va="center", fontsize=8.5, color="#64748B", style="italic")

# 4 Main Architectural Column Blocks
COL_W = 3.45
COL_H = 5.25
COL_Y = 1.3
GAP   = 0.45
START_X = 0.5

# Column 1: Telemetry & Ingestion
x1 = START_X
# Column 2: Dual Monitoring & Feature Extraction
x2 = x1 + COL_W + GAP
# Column 3: Trust Evaluation & Context Filtering
x3 = x2 + COL_W + GAP
# Column 4: Dynamic Policy & Broker Enforcement
x4 = x3 + COL_W + GAP

def draw_layer_card(x, y, w, h, title, subtitle, color, bg_color):
    # Outer container
    card = mpatches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.08",
        fc=bg_color, ec=color, lw=1.5, zorder=1
    )
    ax.add_patch(card)
    # Header strip
    strip_h = 0.52
    strip = mpatches.FancyBboxPatch(
        (x, y + h - strip_h), w, strip_h,
        boxstyle="round,pad=0.0",
        fc=color, ec="none", zorder=2
    )
    ax.add_patch(strip)
    ax.text(x + w/2, y + h - strip_h/2, title,
            ha="center", va="center", fontsize=9, fontweight="bold", color="white", zorder=3)
    ax.text(x + w/2, y + h - strip_h - 0.20, subtitle,
            ha="center", va="center", fontsize=7.2, color="#475569", style="italic", zorder=3)

# Draw Column 1
draw_layer_card(x1, COL_Y, COL_W, COL_H, 
                "LAYER 1: Device Telemetry", "MQTT Client Ingestion & Pre-Auth", 
                BLUE, BLUE_BG)

# Sub-boxes inside Col 1
def draw_sub_box(x, y, w, h, header, lines, border_c="#94A3B8", bg_c="#FFFFFF"):
    b = mpatches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05", fc=bg_c, ec=border_c, lw=1.0, zorder=3)
    ax.add_patch(b)
    ax.text(x + 0.15, y + h - 0.22, header, ha="left", va="center", fontsize=7.8, fontweight="bold", color=border_c, zorder=4)
    y_off = y + h - 0.45
    for ln in lines:
        ax.text(x + 0.15, y_off, ln, ha="left", va="center", fontsize=6.8, color="#1E293B", zorder=4)
        y_off -= 0.22

draw_sub_box(x1 + 0.2, 4.4, COL_W - 0.4, 1.6, 
             "IoT Sensor Fleet (Simulated/Real)", 
             ["• Temperature, Humidity, Camera, Motor",
              "• HMAC-SHA256 Token Authentication",
              "• Payload + Monotonic Seq# + Nonce",
              "• Defined Permitted Topic Namespaces"],
             border_c=BLUE, bg_c="#FFFFFF")

draw_sub_box(x1 + 0.2, 2.3, COL_W - 0.4, 1.8, 
             "Initial Gatekeeper & Protocol Check", 
             ["• Client Identifier & Credential Check",
              "• Token Nonce Replay Verification",
              "• Immediate Drop on Corrupted Payload",
              "• Passes to Broker Message Router",
              "• Zero Trust Principle: Auth != Trust"],
             border_c=DARK_NAVY, bg_c="#FFFFFF")


# Draw Column 2
draw_layer_card(x2, COL_Y, COL_W, COL_H, 
                "LAYER 2: Dual Monitoring", "Device vs. Network Decoupling", 
                TEAL, TEAL_BG)

draw_sub_box(x2 + 0.2, 4.2, COL_W - 0.4, 1.8, 
             "A. Device Behavioural Profiler", 
             ["• Sliding Window Metric Aggregator",
              "• Message Publish Frequency (Rate)",
              "• Topic Violation Counter (Unauth)",
              "• Payload Size Distribution Variance",
              "• Reconnection & Flapping Tracker"],
             border_c=TEAL, bg_c="#FFFFFF")

draw_sub_box(x2 + 0.2, 2.1, COL_W - 0.4, 1.8, 
             "B. Fleet Network Health Monitor", 
             ["• Multi-device Round-Trip Latency (RTT)",
              "• Broker Queue Delay & Packet Loss",
              "• Simultaneous Fleet Degradation %",
              "• Distinguishes Congestion from DoS",
              "• Key Novelty: Avoids False Alarms"],
             border_c=AMBER, bg_c="#FFFFFF")


# Draw Column 3
draw_layer_card(x3, COL_Y, COL_W, COL_H, 
                "LAYER 3: Trust & Confidence", "Mathematical Reasoning Engine", 
                PURPLE, PURPLE_BG)

draw_sub_box(x3 + 0.2, 4.5, COL_W - 0.4, 1.5, 
             "Network Context Discount Filter", 
             ["• If >= 60% Fleet Latency >= 120ms:",
              "  -> Network Congestion Flag Active",
              "  -> Rate & Conn Penalty Discounted (x0.7)",
              "• Unauth Topic Access Never Discounted"],
             border_c=AMBER, bg_c="#FFFFFF")

draw_sub_box(x3 + 0.2, 2.75, COL_W - 0.4, 1.55, 
             "Weighted Risk & EWMA Trust", 
             ["• Risk = 0.30 Unauth + 0.25 AuthFail +",
              "         0.20 Rate + 0.15 Pay + 0.10 Conn",
              "• Trust_raw = 100 * (1 - Risk)",
              "• Trust_t = 0.70 Trust_(t-1) + 0.30 Trust_raw"],
             border_c=PURPLE, bg_c="#FFFFFF")

draw_sub_box(x3 + 0.2, 1.5, COL_W - 0.4, 1.1, 
             "Multi-Factor Confidence Engine", 
             ["• Conf = 0.4 Sample + 0.35 Stab + 0.25 Agree",
              "• Suppresses DENY when evidence sparse"],
             border_c="#64748B", bg_c="#FFFFFF")


# Draw Column 4
draw_layer_card(x4, COL_Y, COL_W, COL_H, 
                "LAYER 4: Adaptive Policy & PEP", "Live Mosquitto ACL Enforcement", 
                GREEN, GREEN_BG)

# 4 Action Cards in Column 4
draw_sub_box(x4 + 0.2, 5.0, COL_W - 0.4, 0.95, 
             "ALLOW  (Trust >= 80, Conf >= 0.6)", 
             ["• Full permitted access; reassess in 30s"],
             border_c=GREEN, bg_c="#F0FDF4")

draw_sub_box(x4 + 0.2, 3.85, COL_W - 0.4, 0.95, 
             "RESTRICT  (50 <= Trust < 80)", 
             ["• Strip control topics; reassess in 10s"],
             border_c=AMBER, bg_c="#FFFBEB")

draw_sub_box(x4 + 0.2, 2.7, COL_W - 0.4, 0.95, 
             "CHALLENGE  (Confidence < 0.40)", 
             ["• Issue cryptographic challenge nonce"],
             border_c=BLUE, bg_c="#EFF6FF")

draw_sub_box(x4 + 0.2, 1.55, COL_W - 0.4, 0.95, 
             "DENY  (Trust < 50 or Critical Override)", 
             ["• Revoke Mosquitto ACL; quarantine node"],
             border_c=RED, bg_c="#FEF2F2")


# Inter-layer Connection Arrows
arrow_style = dict(arrowstyle="->,head_width=0.25,head_length=0.20", lw=2.0, color="#1E293B")

# Col 1 -> Col 2
ax.annotate("", xy=(x2, 5.0), xytext=(x1 + COL_W, 5.0), arrowprops=arrow_style)
ax.annotate("", xy=(x2, 3.0), xytext=(x1 + COL_W, 3.0), arrowprops=arrow_style)

# Col 2 -> Col 3
ax.annotate("", xy=(x3, 5.2), xytext=(x2 + COL_W, 5.2), arrowprops=arrow_style)
ax.annotate("", xy=(x3, 3.0), xytext=(x2 + COL_W, 3.0), arrowprops=arrow_style)

# Col 3 -> Col 4
ax.annotate("", xy=(x4, 3.5), xytext=(x3 + COL_W, 3.5), arrowprops=arrow_style)

# Clean, Orthogonal Feedback Loop (Col 4 -> Col 1) at bottom margin
loop_y = 0.55
x_out = x4 + COL_W / 2
x_in  = x1 + COL_W / 2

ax.plot([x_out, x_out], [COL_Y, loop_y], color=GREEN, lw=2.0, zorder=5)
ax.plot([x_out, x_in],  [loop_y, loop_y], color=GREEN, lw=2.0, zorder=5)
ax.annotate("", xy=(x_in, COL_Y), xytext=(x_in, loop_y),
            arrowprops=dict(arrowstyle="->,head_width=0.25,head_length=0.22", lw=2.0, color=GREEN),
            zorder=5)

ax.text(8.0, loop_y + 0.16,
        "⟲ CONTINUOUS FEEDBACK LOOP: Dynamic ACL syncs directly with Eclipse Mosquitto broker in real-time",
        ha="center", va="bottom", fontsize=8.2, fontweight="bold", color=GREEN, style="italic", zorder=6)

plt.tight_layout(pad=0.2)
plt.savefig(str(OUTPUT_FILE), dpi=250, bbox_inches="tight", facecolor="white")
plt.close()
print(f"SUCCESS: Generated architecture workflow diagram at {OUTPUT_FILE}")
