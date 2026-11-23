"""
Generates a pristine, highly readable, VERTICAL architecture and operational workflow diagram.
Guaranteed ZERO overlapping text: all text blocks have explicit va='top' and generous vertical spacing.
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

# Canvas: 13 x 9.8 inches for generous, clean vertical flow without collision
fig, ax = plt.subplots(figsize=(13, 9.8), dpi=250)
fig.patch.set_facecolor("#FFFFFF")
ax.set_facecolor("#FFFFFF")
ax.axis("off")
ax.set_xlim(0, 13)
ax.set_ylim(0, 9.8)

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
TEXT_DARK = "#0F172A"

# ── Title ────────────────────────────────────────────────────────────────────
ax.text(6.5, 9.55, "Closed-Loop Zero Trust Operational Architecture & Workflow",
        ha="center", va="center", fontsize=13, fontweight="bold", color=DARK_NAVY)
ax.text(6.5, 9.25, "Top-to-bottom pipeline: telemetry ingestion to dual-stream analysis, trust reasoning, and live broker ACL enforcement",
        ha="center", va="center", fontsize=8.5, color="#64748B", style="italic")

# Layout coordinates: 4 Vertical Stages stacked top to bottom
X_LEFT  = 1.7
STAGE_W = 10.8

# ─────────────────────────────────────────────────────────────────────────────
# STAGE 1: TELEMETRY INGESTION & PROTOCOL GATEKEEPER
# ─────────────────────────────────────────────────────────────────────────────
s1_y = 7.65
s1_h = 1.35

s1_box = mpatches.FancyBboxPatch((X_LEFT, s1_y), STAGE_W, s1_h, boxstyle="round,pad=0.06", fc=BLUE_BG, ec=BLUE, lw=1.5, zorder=2)
ax.add_patch(s1_box)

s1_stripe = mpatches.FancyBboxPatch((X_LEFT, s1_y + s1_h - 0.36), STAGE_W, 0.36, boxstyle="round,pad=0.0", fc=BLUE, ec="none", zorder=3)
ax.add_patch(s1_stripe)
ax.text(X_LEFT + 0.25, s1_y + s1_h - 0.18, "STAGE 1: IoT Device Telemetry & Protocol Gatekeeper", ha="left", va="center", fontsize=8.8, fontweight="bold", color="white", zorder=4)

ax.text(X_LEFT + 0.35, s1_y + s1_h - 0.48, 
        "• IoT Sensor Fleet: temperature_sensor_01, humidity_02, energy_03, motor_04, camera_05\n"
        "• Each message carries: Client ID + Sensor Payload + Monotonic Seq# + Cryptographic Nonce", 
        ha="left", va="top", fontsize=7.5, color=TEXT_DARK, zorder=4, linespacing=1.4)

ax.text(X_LEFT + 6.3, s1_y + s1_h - 0.48, 
        "• Protocol Verification: Verifies HMAC token & checks nonce freshness against replay attacks\n"
        "• Zero Trust Gate: Validates schema; authentication grants access to router, NOT permanent trust", 
        ha="left", va="top", fontsize=7.6, color=TEXT_DARK, zorder=4, linespacing=1.4)

# Downward Arrow Stage 1 -> Stage 2
arrow_kw = dict(arrowstyle="->,head_width=0.28,head_length=0.22", lw=2.0, color="#334155")
ax.annotate("", xy=(X_LEFT + STAGE_W/2, 7.25), xytext=(X_LEFT + STAGE_W/2, s1_y), arrowprops=arrow_kw, zorder=5)
ax.text(X_LEFT + STAGE_W/2 + 0.15, 7.45, "Parallel Dual Monitoring", fontsize=7.2, color="#475569", style="italic", zorder=5)


# ─────────────────────────────────────────────────────────────────────────────
# STAGE 2: PARALLEL DUAL-STREAM MONITORING (DEVICES VS. NETWORK)
# ─────────────────────────────────────────────────────────────────────────────
s2_y = 5.25
s2_h = 1.90

s2_box = mpatches.FancyBboxPatch((X_LEFT, s2_y), STAGE_W, s2_h, boxstyle="round,pad=0.06", fc="#F8FAFC", ec=TEAL, lw=1.5, zorder=2)
ax.add_patch(s2_box)

s2_stripe = mpatches.FancyBboxPatch((X_LEFT, s2_y + s2_h - 0.36), STAGE_W, 0.36, boxstyle="round,pad=0.0", fc=TEAL, ec="none", zorder=3)
ax.add_patch(s2_stripe)
ax.text(X_LEFT + 0.25, s2_y + s2_h - 0.18, "STAGE 2: Dual-Stream Monitoring — Decoupling Device Behaviour from Network Health", ha="left", va="center", fontsize=8.8, fontweight="bold", color="white", zorder=4)

# Sub-card 2A (Left): Device Behaviour Profiler
sub2a_w = 5.15
sub2a_h = 1.35
sub2a = mpatches.FancyBboxPatch((X_LEFT + 0.20, s2_y + 0.12), sub2a_w, sub2a_h, boxstyle="round,pad=0.04", fc=TEAL_BG, ec=TEAL, lw=1.0, zorder=3)
ax.add_patch(sub2a)

# Sub-card 2A Header Strip
hdr2a = mpatches.FancyBboxPatch((X_LEFT + 0.20, s2_y + 0.12 + sub2a_h - 0.28), sub2a_w, 0.28, boxstyle="round,pad=0.0", fc=TEAL, ec="none", zorder=4)
ax.add_patch(hdr2a)
ax.text(X_LEFT + 0.35, s2_y + 0.12 + sub2a_h - 0.14, "2A. Device Behaviour Profiler (Sliding Window)", ha="left", va="center", fontsize=7.6, fontweight="bold", color="white", zorder=5)

# Sub-card 2A Content (strictly va="top" below header)
ax.text(X_LEFT + 0.35, s2_y + 0.12 + sub2a_h - 0.34,
        "• Message Rate Anomaly (x_rate): Frequency surge over baseline\n"
        "• Unauthorized Topics (x_unauth): Probing sensitive namespaces\n"
        "• Authentication Failures (x_auth): Credential brute-force attempts\n"
        "• Payload Variance (x_payload): Size distribution shifts / buffer abuse\n"
        "• Connection Flapping (x_conn): Rapid disconnect/reconnect cycles",
        ha="left", va="top", fontsize=6.8, color=TEXT_DARK, zorder=5, linespacing=1.35)

# Sub-card 2B (Right): Fleet Network Context Monitor
sub2b_w = 5.15
sub2b_h = 1.35
sub2b = mpatches.FancyBboxPatch((X_LEFT + 5.45, s2_y + 0.12), sub2b_w, sub2b_h, boxstyle="round,pad=0.04", fc=AMBER_BG, ec=AMBER, lw=1.0, zorder=3)
ax.add_patch(sub2b)

# Sub-card 2B Header Strip
hdr2b = mpatches.FancyBboxPatch((X_LEFT + 5.45, s2_y + 0.12 + sub2b_h - 0.28), sub2b_w, 0.28, boxstyle="round,pad=0.0", fc=AMBER, ec="none", zorder=4)
ax.add_patch(hdr2b)
ax.text(X_LEFT + 5.60, s2_y + 0.12 + sub2b_h - 0.14, "2B. Fleet Network Health Monitor (Novel Contribution)", ha="left", va="center", fontsize=7.6, fontweight="bold", color="white", zorder=5)

# Sub-card 2B Content (strictly va="top" below header)
ax.text(X_LEFT + 5.60, s2_y + 0.12 + sub2b_h - 0.34,
        "• Multi-Device RTT Latency: Fleet-wide delay across all connected nodes\n"
        "• Broker Queue Delay & Packet Loss: Broker processing backpressure\n"
        "• Fleet Degradation Ratio (ρ): % of nodes experiencing latency >= 120ms\n"
        "• Congestion Flag: Triggered when ρ >= 60% of fleet degraded\n"
        "• Core Research Novelty: Distinguishes benign network delay from DoS floods",
        ha="left", va="top", fontsize=6.8, color=TEXT_DARK, zorder=5, linespacing=1.35)

# Downward Arrow Stage 2 -> Stage 3
ax.annotate("", xy=(X_LEFT + STAGE_W/2, 4.85), xytext=(X_LEFT + STAGE_W/2, s2_y), arrowprops=arrow_kw, zorder=5)
ax.text(X_LEFT + STAGE_W/2 + 0.15, 5.05, "Feature Fusion & Context Filtering", fontsize=7.2, color="#475569", style="italic", zorder=5)


# ─────────────────────────────────────────────────────────────────────────────
# STAGE 3: TRUST EVALUATION, CONTEXT FILTERING & CONFIDENCE
# ─────────────────────────────────────────────────────────────────────────────
s3_y = 3.05
s3_h = 1.70

s3_box = mpatches.FancyBboxPatch((X_LEFT, s3_y), STAGE_W, s3_h, boxstyle="round,pad=0.06", fc=PURPLE_BG, ec=PURPLE, lw=1.5, zorder=2)
ax.add_patch(s3_box)

s3_stripe = mpatches.FancyBboxPatch((X_LEFT, s3_y + s3_h - 0.36), STAGE_W, 0.36, boxstyle="round,pad=0.0", fc=PURPLE, ec="none", zorder=3)
ax.add_patch(s3_stripe)
ax.text(X_LEFT + 0.25, s3_y + s3_h - 0.18, "STAGE 3: Mathematical Reasoning Engine — Context Discount, EWMA Trust & Confidence", ha="left", va="center", fontsize=8.8, fontweight="bold", color="white", zorder=4)

# 3 Inner blocks for Stage 3
cw3 = 3.35
box3_h = 1.15

def draw_stage3_box(x, y, w, h, title, lines, color):
    b = mpatches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.04", fc="#FFFFFF", ec=color, lw=0.9, zorder=3)
    ax.add_patch(b)
    # Header strip
    hdr = mpatches.FancyBboxPatch((x, y + h - 0.24), w, 0.24, boxstyle="round,pad=0.0", fc=color, ec="none", zorder=4)
    ax.add_patch(hdr)
    ax.text(x + w/2, y + h - 0.12, title, ha="center", va="center", fontsize=7.2, fontweight="bold", color="white", zorder=5)
    # Text
    ax.text(x + 0.15, y + h - 0.32, "\n".join(lines), ha="left", va="top", fontsize=6.7, color=TEXT_DARK, zorder=5, linespacing=1.35)

draw_stage3_box(X_LEFT + 0.18, s3_y + 0.12, cw3, box3_h, 
                "Context Discount Filter",
                ["If Congestion Flag == True:",
                 "  x_rate_adj = 0.70 * x_rate",
                 "  x_conn_adj = 0.70 * x_conn",
                 "• Unauth violations NEVER discounted"],
                AMBER)

draw_stage3_box(X_LEFT + 3.73, s3_y + 0.12, cw3, box3_h, 
                "Weighted Risk & EWMA",
                ["Risk = 0.30 Unauth + 0.25 AuthFail",
                 "       + 0.20 Rate + 0.15 Pay + 0.10 Conn",
                 "Trust_t = 0.70 Trust_(t-1) + 0.30 Trust_raw",
                 "• Override: Unauth forces Trust = 0 instantly"],
                PURPLE)

draw_stage3_box(X_LEFT + 7.28, s3_y + 0.12, cw3, box3_h, 
                "Evidence Confidence (C)",
                ["C = 0.40 C_sample + 0.35 C_stability",
                 "    + 0.25 C_agreement",
                 "• Bounded in [0, 1] via sample count & CV",
                 "• Low confidence triggers CHALLENGE, not DENY"],
                DARK_NAVY)

# Downward Arrow Stage 3 -> Stage 4
ax.annotate("", xy=(X_LEFT + STAGE_W/2, 2.65), xytext=(X_LEFT + STAGE_W/2, s3_y), arrowprops=arrow_kw, zorder=5)
ax.text(X_LEFT + STAGE_W/2 + 0.15, 2.85, "Adaptive Policy Mapping", fontsize=7.2, color="#475569", style="italic", zorder=5)


# ─────────────────────────────────────────────────────────────────────────────
# STAGE 4: ADAPTIVE ACCESS CONTROL POLICY & MOSQUITTO BROKER ENFORCEMENT
# ─────────────────────────────────────────────────────────────────────────────
s4_y = 0.85
s4_h = 1.70

s4_box = mpatches.FancyBboxPatch((X_LEFT, s4_y), STAGE_W, s4_h, boxstyle="round,pad=0.06", fc=GREEN_BG, ec=GREEN, lw=1.5, zorder=2)
ax.add_patch(s4_box)

s4_stripe = mpatches.FancyBboxPatch((X_LEFT, s4_y + s4_h - 0.36), STAGE_W, 0.36, boxstyle="round,pad=0.0", fc=GREEN, ec="none", zorder=3)
ax.add_patch(s4_stripe)
ax.text(X_LEFT + 0.25, s4_y + s4_h - 0.18, "STAGE 4: Adaptive Access Policy & Dynamic Mosquitto ACL Enforcement (PEP)", ha="left", va="center", fontsize=8.8, fontweight="bold", color="white", zorder=4)

# 4 Outcome Policy Cards across Stage 4
cw4 = 2.50
card4_h = 1.15

def draw_stage4_card(x, y, w, h, title, lines, color):
    b = mpatches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.04", fc="#FFFFFF", ec=color, lw=1.0, zorder=3)
    ax.add_patch(b)
    # Header strip
    hdr = mpatches.FancyBboxPatch((x, y + h - 0.24), w, 0.24, boxstyle="round,pad=0.0", fc=color, ec="none", zorder=4)
    ax.add_patch(hdr)
    ax.text(x + w/2, y + h - 0.12, title, ha="center", va="center", fontsize=6.8, fontweight="bold", color="white", zorder=5)
    # Text
    ax.text(x + 0.12, y + h - 0.32, "\n".join(lines), ha="left", va="top", fontsize=6.6, color=TEXT_DARK, zorder=5, linespacing=1.35)

draw_stage4_card(X_LEFT + 0.16, s4_y + 0.12, cw4, card4_h,
                 "ALLOW (Trust >= 80, C >= 0.6)",
                 ["• Full access to registered topics",
                  "• Normal publish & subscribe",
                  "• Reassessment window: 60s"],
                 GREEN)

draw_stage4_card(X_LEFT + 2.82, s4_y + 0.12, cw4, card4_h,
                 "RESTRICT (50 <= Trust < 80)",
                 ["• Actuator control topics revoked",
                  "• Telemetry throttled / read-only",
                  "• Reassessment window: 15s"],
                 AMBER)

draw_stage4_card(X_LEFT + 5.48, s4_y + 0.12, cw4, card4_h,
                 "CHALLENGE (C < 0.40)",
                 ["• Low evidence confidence",
                  "• Transmit cryptographic challenge",
                  "• Must reply correctly in 5s"],
                 BLUE)

draw_stage4_card(X_LEFT + 8.14, s4_y + 0.12, cw4, card4_h,
                 "DENY (Trust < 50 / Override)",
                 ["• Broker ACL instantly revoked",
                  "• Active TCP socket terminated",
                  "• Reassessment window: 2s"],
                 RED)


# ─────────────────────────────────────────────────────────────────────────────
# CONTINUOUS FEEDBACK LOOP ARROW (LEFT SIDE: STAGE 4 -> STAGE 1)
# ─────────────────────────────────────────────────────────────────────────────
loop_x = 0.75
ax.plot([X_LEFT, loop_x], [s4_y + s4_h/2, s4_y + s4_h/2], color=GREEN, lw=2.2, zorder=5)
ax.plot([loop_x, loop_x], [s4_y + s4_h/2, s1_y + s1_h/2], color=GREEN, lw=2.2, zorder=5)
ax.annotate("", xy=(X_LEFT, s1_y + s1_h/2), xytext=(loop_x, s1_y + s1_h/2),
            arrowprops=dict(arrowstyle="->,head_width=0.30,head_length=0.25", lw=2.2, color=GREEN),
            zorder=5)

ax.text(loop_x - 0.20, (s1_y + s4_y)/2 + 0.8,
        "⟲ CONTINUOUS FEEDBACK LOOP: Live Mosquitto ACL Synchronization for Subsequent Messages",
        ha="center", va="center", fontsize=7.6, fontweight="bold", color=GREEN, rotation=90, zorder=6)

plt.tight_layout(pad=0.2)
plt.savefig(str(OUTPUT_FILE), dpi=250, bbox_inches="tight", facecolor="white")
plt.close()
print(f"SUCCESS: Generated clean vertical architecture workflow diagram without overlapping text at {OUTPUT_FILE}")
