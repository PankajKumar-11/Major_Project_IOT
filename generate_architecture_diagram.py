"""
Generates a MINIMAL, CRISP, HIGHLY READABLE vertical architecture diagram.
Focused strictly on the essential workflow: large fonts, spacious padding, zero clutter.
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

# Canvas: 12 x 8.6 inches - minimal, clean, spacious
fig, ax = plt.subplots(figsize=(12, 8.6), dpi=250)
fig.patch.set_facecolor("#FFFFFF")
ax.set_facecolor("#FFFFFF")
ax.axis("off")
ax.set_xlim(0, 12)
ax.set_ylim(0, 8.6)

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
BORDER    = "#CBD5E1"
TEXT_DARK = "#0F172A"

# Title Header
ax.text(6.3, 8.35, "Closed-Loop Zero Trust Operational Architecture",
        ha="center", va="center", fontsize=13, fontweight="bold", color=DARK_NAVY)
ax.text(6.3, 8.08, "Dual-stream monitoring separates device anomalies from network congestion before dynamic ACL enforcement",
        ha="center", va="center", fontsize=8.2, color="#64748B", style="italic")

# Coordinates
X_LEFT  = 1.5
STAGE_W = 10.0

# ── STAGE 1: INGESTION & GATEKEEPER ──────────────────────────────────────────
s1_y = 6.75
s1_h = 1.15

s1_box = mpatches.FancyBboxPatch((X_LEFT, s1_y), STAGE_W, s1_h, boxstyle="round,pad=0.06", fc=BLUE_BG, ec=BLUE, lw=1.5, zorder=2)
ax.add_patch(s1_box)

s1_hdr = mpatches.FancyBboxPatch((X_LEFT, s1_y + s1_h - 0.32), STAGE_W, 0.32, boxstyle="round,pad=0.0", fc=BLUE, ec="none", zorder=3)
ax.add_patch(s1_hdr)
ax.text(X_LEFT + 0.25, s1_y + s1_h - 0.16, "STAGE 1: Telemetry Ingestion & Protocol Gatekeeper", ha="left", va="center", fontsize=8.8, fontweight="bold", color="white", zorder=4)

ax.text(X_LEFT + 0.35, s1_y + s1_h - 0.44,
        "• IoT Fleet: temperature_01, humidity_02, energy_03, motor_04, camera_05\n"
        "• MQTT Payload + Monotonic Seq Number + Cryptographic Nonce",
        ha="left", va="top", fontsize=7.8, color=TEXT_DARK, zorder=4, linespacing=1.4)

ax.text(X_LEFT + 5.8, s1_y + s1_h - 0.44,
        "• Replay & Schema Check: Blocks duplicate nonces and malformed packets\n"
        "• Core Zero Trust Principle: Successful authentication != permanent trust",
        ha="left", va="top", fontsize=7.8, color=TEXT_DARK, zorder=4, linespacing=1.4)

# Arrow 1 -> 2
arrow_kw = dict(arrowstyle="->,head_width=0.25,head_length=0.20", lw=1.8, color="#334155")
ax.annotate("", xy=(X_LEFT + STAGE_W/2, 6.38), xytext=(X_LEFT + STAGE_W/2, s1_y), arrowprops=arrow_kw, zorder=5)


# ── STAGE 2: PARALLEL DUAL MONITORING ────────────────────────────────────────
s2_y = 4.65
s2_h = 1.70

s2_box = mpatches.FancyBboxPatch((X_LEFT, s2_y), STAGE_W, s2_h, boxstyle="round,pad=0.06", fc="#F8FAFC", ec=TEAL, lw=1.5, zorder=2)
ax.add_patch(s2_box)

s2_hdr = mpatches.FancyBboxPatch((X_LEFT, s2_y + s2_h - 0.32), STAGE_W, 0.32, boxstyle="round,pad=0.0", fc=TEAL, ec="none", zorder=3)
ax.add_patch(s2_hdr)
ax.text(X_LEFT + 0.25, s2_y + s2_h - 0.16, "STAGE 2: Parallel Dual Monitoring — Decoupling Device Behaviour from Network Congestion", ha="left", va="center", fontsize=8.8, fontweight="bold", color="white", zorder=4)

# Sub-card 2A (Left): Device Profiler
sub_w = 4.75
sub_h = 1.20
b2a = mpatches.FancyBboxPatch((X_LEFT + 0.16, s2_y + 0.10), sub_w, sub_h, boxstyle="round,pad=0.04", fc=TEAL_BG, ec=TEAL, lw=1.0, zorder=3)
ax.add_patch(b2a)
hdr2a = mpatches.FancyBboxPatch((X_LEFT + 0.16, s2_y + 0.10 + sub_h - 0.26), sub_w, 0.26, boxstyle="round,pad=0.0", fc=TEAL, ec="none", zorder=4)
ax.add_patch(hdr2a)
ax.text(X_LEFT + 0.30, s2_y + 0.10 + sub_h - 0.13, "2A. Device Behaviour Profiler (Sliding Window)", ha="left", va="center", fontsize=7.6, fontweight="bold", color="white", zorder=5)

ax.text(X_LEFT + 0.30, s2_y + 0.10 + sub_h - 0.36,
        "• Message Rate Anomaly (x_rate): Frequency spikes\n"
        "• Unauthorized Topics (x_unauth): Probing actuator commands\n"
        "• Auth Failures (x_auth): Credential brute-force attempts\n"
        "• Payload Variance & Reconnection Churn",
        ha="left", va="top", fontsize=7.2, color=TEXT_DARK, zorder=5, linespacing=1.35)

# Sub-card 2B (Right): Fleet Health Monitor
b2b = mpatches.FancyBboxPatch((X_LEFT + 5.09, s2_y + 0.10), sub_w, sub_h, boxstyle="round,pad=0.04", fc=AMBER_BG, ec=AMBER, lw=1.0, zorder=3)
ax.add_patch(b2b)
hdr2b = mpatches.FancyBboxPatch((X_LEFT + 5.09, s2_y + 0.10 + sub_h - 0.26), sub_w, 0.26, boxstyle="round,pad=0.0", fc=AMBER, ec="none", zorder=4)
ax.add_patch(hdr2b)
ax.text(X_LEFT + 5.23, s2_y + 0.10 + sub_h - 0.13, "2B. Fleet Network Health Monitor (Core Novelty)", ha="left", va="center", fontsize=7.6, fontweight="bold", color="white", zorder=5)

ax.text(X_LEFT + 5.23, s2_y + 0.10 + sub_h - 0.36,
        "• Fleet-Wide RTT Latency: Delivery delay across all nodes\n"
        "• Broker Queue Delay & Packet Loss Monitoring\n"
        "• Congestion Flag: Triggered if >= 60% of fleet has Latency >= 120ms\n"
        "• Prevents false alarms during benign network congestion",
        ha="left", va="top", fontsize=7.2, color=TEXT_DARK, zorder=5, linespacing=1.35)

# Arrow 2 -> 3
ax.annotate("", xy=(X_LEFT + STAGE_W/2, 4.28), xytext=(X_LEFT + STAGE_W/2, s2_y), arrowprops=arrow_kw, zorder=5)


# ── STAGE 3: MATHEMATICAL REASONING ENGINE ───────────────────────────────────
s3_y = 2.65
s3_h = 1.60

s3_box = mpatches.FancyBboxPatch((X_LEFT, s3_y), STAGE_W, s3_h, boxstyle="round,pad=0.06", fc=PURPLE_BG, ec=PURPLE, lw=1.5, zorder=2)
ax.add_patch(s3_box)

s3_hdr = mpatches.FancyBboxPatch((X_LEFT, s3_y + s3_h - 0.32), STAGE_W, 0.32, boxstyle="round,pad=0.0", fc=PURPLE, ec="none", zorder=3)
ax.add_patch(s3_hdr)
ax.text(X_LEFT + 0.25, s3_y + s3_h - 0.16, "STAGE 3: Mathematical Reasoning — Context Discount, EWMA Trust & Confidence", ha="left", va="center", fontsize=8.8, fontweight="bold", color="white", zorder=4)

cw3 = 3.12
box3_h = 1.10

def draw_s3_col(x, y, w, h, title, lines, color):
    b = mpatches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.04", fc="#FFFFFF", ec=color, lw=0.9, zorder=3)
    ax.add_patch(b)
    hdr = mpatches.FancyBboxPatch((x, y + h - 0.24), w, 0.24, boxstyle="round,pad=0.0", fc=color, ec="none", zorder=4)
    ax.add_patch(hdr)
    ax.text(x + w/2, y + h - 0.12, title, ha="center", va="center", fontsize=7.2, fontweight="bold", color="white", zorder=5)
    ax.text(x + 0.12, y + h - 0.34, "\n".join(lines), ha="left", va="top", fontsize=6.9, color=TEXT_DARK, zorder=5, linespacing=1.35)

draw_s3_col(X_LEFT + 0.14, s3_y + 0.10, cw3, box3_h,
            "Context Discount Filter",
            ["If Congestion Flag == True:",
             "  x_rate_adj = 0.70 * x_rate",
             "  x_conn_adj = 0.70 * x_conn",
             "• Unauthorized topics NEVER discounted"],
            AMBER)

draw_s3_col(X_LEFT + 3.44, s3_y + 0.10, cw3, box3_h,
            "Weighted Risk & EWMA",
            ["Risk = 0.30 Unauth + 0.25 AuthFail",
             "       + 0.20 Rate + 0.15 Pay + 0.10 Conn",
             "Trust_t = 0.70 Trust_(t-1) + 0.30 Trust_raw",
             "• Override: Unauth attempts force Trust = 0"],
            PURPLE)

draw_s3_col(X_LEFT + 6.74, s3_y + 0.10, cw3, box3_h,
            "Evidence Confidence (C)",
            ["C = 0.40 C_sample + 0.35 C_stability",
             "    + 0.25 C_agreement",
             "• Derived from sample size (n) and CV",
             "• Low confidence triggers CHALLENGE"],
            DARK_NAVY)

# Arrow 3 -> 4
ax.annotate("", xy=(X_LEFT + STAGE_W/2, 2.28), xytext=(X_LEFT + STAGE_W/2, s3_y), arrowprops=arrow_kw, zorder=5)


# ── STAGE 4: ADAPTIVE ACCESS CONTROL & ENFORCEMENT ───────────────────────────
s4_y = 0.65
s4_h = 1.60

s4_box = mpatches.FancyBboxPatch((X_LEFT, s4_y), STAGE_W, s4_h, boxstyle="round,pad=0.06", fc=GREEN_BG, ec=GREEN, lw=1.5, zorder=2)
ax.add_patch(s4_box)

s4_hdr = mpatches.FancyBboxPatch((X_LEFT, s4_y + s4_h - 0.32), STAGE_W, 0.32, boxstyle="round,pad=0.0", fc=GREEN, ec="none", zorder=3)
ax.add_patch(s4_hdr)
ax.text(X_LEFT + 0.25, s4_y + s4_h - 0.16, "STAGE 4: Adaptive Access Policy & Dynamic Mosquitto ACL Enforcement", ha="left", va="center", fontsize=8.8, fontweight="bold", color="white", zorder=4)

cw4 = 2.30
card4_h = 1.10

def draw_s4_card(x, y, w, h, title, lines, color):
    b = mpatches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.04", fc="#FFFFFF", ec=color, lw=1.0, zorder=3)
    ax.add_patch(b)
    hdr = mpatches.FancyBboxPatch((x, y + h - 0.24), w, 0.24, boxstyle="round,pad=0.0", fc=color, ec="none", zorder=4)
    ax.add_patch(hdr)
    ax.text(x + w/2, y + h - 0.12, title, ha="center", va="center", fontsize=6.8, fontweight="bold", color="white", zorder=5)
    ax.text(x + 0.10, y + h - 0.34, "\n".join(lines), ha="left", va="top", fontsize=6.7, color=TEXT_DARK, zorder=5, linespacing=1.35)

draw_s4_card(X_LEFT + 0.14, s4_y + 0.10, cw4, card4_h,
             "ALLOW (Trust >= 80)",
             ["• Full topic access",
              "• Normal telemetry publish",
              "• Reassess window: 60s"],
             GREEN)

draw_s4_card(X_LEFT + 2.58, s4_y + 0.10, cw4, card4_h,
             "RESTRICT (50 <= Trust < 80)",
             ["• Control topics revoked",
              "• Actuators stripped (read-only)",
              "• Reassess window: 15s"],
             AMBER)

draw_s4_card(X_LEFT + 5.02, s4_y + 0.10, cw4, card4_h,
             "CHALLENGE (C < 0.40)",
             ["• Low evidence confidence",
              "• Nonce verification issued",
              "• Reassessment: Immediate"],
             BLUE)

draw_s4_card(X_LEFT + 7.46, s4_y + 0.10, cw4, card4_h,
             "DENY (Trust < 50 / Override)",
             ["• Broker ACL revoked",
              "• Socket terminated & isolated",
              "• Reassess window: 2s"],
             RED)


# ── CONTINUOUS FEEDBACK LOOP ARROW (LEFT SIDE) ──────────────────────────────
loop_x = 0.65
ax.plot([X_LEFT, loop_x], [s4_y + s4_h/2, s4_y + s4_h/2], color=GREEN, lw=2.0, zorder=5)
ax.plot([loop_x, loop_x], [s4_y + s4_h/2, s1_y + s1_h/2], color=GREEN, lw=2.0, zorder=5)
ax.annotate("", xy=(X_LEFT, s1_y + s1_h/2), xytext=(loop_x, s1_y + s1_h/2),
            arrowprops=dict(arrowstyle="->,head_width=0.28,head_length=0.22", lw=2.0, color=GREEN),
            zorder=5)

ax.text(loop_x - 0.18, (s1_y + s4_y)/2 + 0.8,
        "⟲ CONTINUOUS FEEDBACK LOOP: Live Mosquitto ACL Synchronization for Subsequent Messages",
        ha="center", va="center", fontsize=7.4, fontweight="bold", color=GREEN, rotation=90, zorder=6)

plt.tight_layout(pad=0.2)
plt.savefig(str(OUTPUT_FILE), dpi=250, bbox_inches="tight", facecolor="white")
plt.close()
print(f"SUCCESS: Generated minimal, crisp architecture workflow diagram at {OUTPUT_FILE}")
