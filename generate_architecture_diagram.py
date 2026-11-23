"""
Generates a spacious, highly readable, VERTICAL architecture and operational workflow diagram.
Layers flow from TOP to BOTTOM with full horizontal width for crystal-clear readability.
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

# Canvas: 13 x 9 inches for a spacious, clean vertical flow
fig, ax = plt.subplots(figsize=(13, 9.2), dpi=250)
fig.patch.set_facecolor("#FFFFFF")
ax.set_facecolor("#FFFFFF")
ax.axis("off")
ax.set_xlim(0, 13)
ax.set_ylim(0, 9.2)

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
TEXT_DARK = "#1E293B"

# ── Title ────────────────────────────────────────────────────────────────────
ax.text(6.5, 8.95, "Closed-Loop Zero Trust Operational Architecture & Workflow",
        ha="center", va="center", fontsize=12.5, fontweight="bold", color=DARK_NAVY)
ax.text(6.5, 8.68, "Top-to-bottom pipeline: from telemetry ingestion to dual-stream analysis, trust reasoning, and live broker ACL enforcement",
        ha="center", va="center", fontsize=8.2, color="#64748B", style="italic")

# Layout coordinates: 4 Vertical Stages stacked top to bottom
# Left margin is 1.6 to allow space for the feedback loop arrow on the left!
X_LEFT  = 1.7
STAGE_W = 10.8

# ─────────────────────────────────────────────────────────────────────────────
# STAGE 1: TELEMETRY INGESTION & PROTOCOL GATEKEEPER
# ─────────────────────────────────────────────────────────────────────────────
s1_y = 7.15
s1_h = 1.30

# Container
s1_box = mpatches.FancyBboxPatch((X_LEFT, s1_y), STAGE_W, s1_h, boxstyle="round,pad=0.06", fc=BLUE_BG, ec=BLUE, lw=1.5, zorder=2)
ax.add_patch(s1_box)

# Header stripe
s1_stripe = mpatches.FancyBboxPatch((X_LEFT, s1_y + s1_h - 0.36), STAGE_W, 0.36, boxstyle="round,pad=0.0", fc=BLUE, ec="none", zorder=3)
ax.add_patch(s1_stripe)
ax.text(X_LEFT + 0.25, s1_y + s1_h - 0.18, "STAGE 1: IoT Device Telemetry & Protocol Gatekeeper", ha="left", va="center", fontsize=8.5, fontweight="bold", color="white", zorder=4)

# Content (Two side-by-side elements inside Stage 1)
ax.text(X_LEFT + 0.35, s1_y + 0.65, 
        "• IoT Sensor Fleet (Sensors, Motors, Cameras) publishes MQTT telemetry\n"
        "• Each packet carries: Client ID + Payload + Monotonic Seq# + Cryptographic Nonce", 
        ha="left", va="center", fontsize=7.6, color=TEXT_DARK, zorder=4, linespacing=1.35)

ax.text(X_LEFT + 6.6, s1_y + 0.65, 
        "• Protocol Verification: Checks HMAC token & validates nonce freshness\n"
        "• Zero Trust Gate: Passes packet to router; authentication ≠ permanent trust", 
        ha="left", va="center", fontsize=7.6, color=TEXT_DARK, zorder=4, linespacing=1.35)

# Downward Arrow Stage 1 -> Stage 2
arrow_kw = dict(arrowstyle="->,head_width=0.28,head_length=0.22", lw=2.0, color="#334155")
ax.annotate("", xy=(X_LEFT + STAGE_W/2, 6.75), xytext=(X_LEFT + STAGE_W/2, s1_y), arrowprops=arrow_kw, zorder=5)
ax.text(X_LEFT + STAGE_W/2 + 0.15, 6.95, "Parallel Dual Monitoring", fontsize=7.2, color="#475569", style="italic", zorder=5)


# ─────────────────────────────────────────────────────────────────────────────
# STAGE 2: PARALLEL DUAL-STREAM MONITORING (DEVICES VS. NETWORK)
# ─────────────────────────────────────────────────────────────────────────────
s2_y = 4.95
s2_h = 1.80

s2_box = mpatches.FancyBboxPatch((X_LEFT, s2_y), STAGE_W, s2_h, boxstyle="round,pad=0.06", fc="#F8FAFC", ec=TEAL, lw=1.5, zorder=2)
ax.add_patch(s2_box)

s2_stripe = mpatches.FancyBboxPatch((X_LEFT, s2_y + s2_h - 0.36), STAGE_W, 0.36, boxstyle="round,pad=0.0", fc=TEAL, ec="none", zorder=3)
ax.add_patch(s2_stripe)
ax.text(X_LEFT + 0.25, s2_y + s2_h - 0.18, "STAGE 2: Dual-Stream Monitoring — Decoupling Device Behaviour from Network Health", ha="left", va="center", fontsize=8.5, fontweight="bold", color="white", zorder=4)

# Sub-card 2A (Left): Device Behaviour Profiler
sub2a_w = 5.15
sub2a_h = 1.25
sub2a = mpatches.FancyBboxPatch((X_LEFT + 0.20, s2_y + 0.12), sub2a_w, sub2a_h, boxstyle="round,pad=0.04", fc=TEAL_BG, ec=TEAL, lw=1.0, zorder=3)
ax.add_patch(sub2a)
ax.text(X_LEFT + 0.35, s2_y + 0.12 + sub2a_h - 0.20, "2A. Device Behaviour Profiler (Sliding Window)", fontsize=7.8, fontweight="bold", color=TEAL, zorder=4)
ax.text(X_LEFT + 0.35, s2_y + 0.12 + 0.50,
        "• Message Rate Anomaly (x_rate): Frequency spikes above baseline\n"
        "• Unauthorized Topics (x_unauth): Probing sensitive namespaces\n"
        "• Authentication Failures (x_auth): Credential brute-force attempts\n"
        "• Payload Variance (x_payload): Size distribution shifts / buffer abuse\n"
        "• Connection Flapping (x_conn): Rapid disconnect/reconnect cycles",
        fontsize=6.8, color=TEXT_DARK, zorder=4, linespacing=1.3)

# Sub-card 2B (Right): Fleet Network Context Monitor
sub2b_w = 5.15
sub2b_h = 1.25
sub2b = mpatches.FancyBboxPatch((X_LEFT + 5.45, s2_y + 0.12), sub2b_w, sub2b_h, boxstyle="round,pad=0.04", fc=AMBER_BG, ec=AMBER, lw=1.0, zorder=3)
ax.add_patch(sub2b)
ax.text(X_LEFT + 5.60, s2_y + 0.12 + sub2b_h - 0.20, "2B. Fleet Network Health Monitor (Novel Contribution)", fontsize=7.8, fontweight="bold", color=AMBER, zorder=4)
ax.text(X_LEFT + 5.60, s2_y + 0.12 + 0.50,
        "• Multi-Device RTT Latency: Tracks delivery delay across entire fleet\n"
        "• Broker Queue Delay & Packet Loss: Senses broker load & backpressure\n"
        "• Fleet Degradation Ratio (ρ): % of nodes experiencing high latency\n"
        "• Congestion Flag Trigger: If ρ >= 60% with Latency >= 120ms\n"
        "• Crucial Novelty: Distinguishes benign network delay from DoS floods",
        fontsize=6.8, color=TEXT_DARK, zorder=4, linespacing=1.3)

# Downward Arrow Stage 2 -> Stage 3
ax.annotate("", xy=(X_LEFT + STAGE_W/2, 4.55), xytext=(X_LEFT + STAGE_W/2, s2_y), arrowprops=arrow_kw, zorder=5)
ax.text(X_LEFT + STAGE_W/2 + 0.15, 4.75, "Feature Fusion & Filtering", fontsize=7.2, color="#475569", style="italic", zorder=5)


# ─────────────────────────────────────────────────────────────────────────────
# STAGE 3: TRUST EVALUATION, CONTEXT FILTERING & CONFIDENCE
# ─────────────────────────────────────────────────────────────────────────────
s3_y = 2.90
s3_h = 1.65

s3_box = mpatches.FancyBboxPatch((X_LEFT, s3_y), STAGE_W, s3_h, boxstyle="round,pad=0.06", fc=PURPLE_BG, ec=PURPLE, lw=1.5, zorder=2)
ax.add_patch(s3_box)

s3_stripe = mpatches.FancyBboxPatch((X_LEFT, s3_y + s3_h - 0.36), STAGE_W, 0.36, boxstyle="round,pad=0.0", fc=PURPLE, ec="none", zorder=3)
ax.add_patch(s3_stripe)
ax.text(X_LEFT + 0.25, s3_y + s3_h - 0.18, "STAGE 3: Mathematical Reasoning Engine — Context Discount, EWMA Trust & Confidence", ha="left", va="center", fontsize=8.5, fontweight="bold", color="white", zorder=4)

# 3 Inner blocks for Stage 3
cw3 = 3.35
# 3A: Context Discount
b3a = mpatches.FancyBboxPatch((X_LEFT + 0.18, s3_y + 0.12), cw3, 1.05, boxstyle="round,pad=0.04", fc="#FFFFFF", ec=AMBER, lw=0.9, zorder=3)
ax.add_patch(b3a)
ax.text(X_LEFT + 0.28, s3_y + 0.95, "Context Discount Filter", fontsize=7.2, fontweight="bold", color=AMBER, zorder=4)
ax.text(X_LEFT + 0.28, s3_y + 0.50,
        "If Congestion Flag == True:\n"
        "  x_rate_adj = 0.70 * x_rate\n"
        "  x_conn_adj = 0.70 * x_conn\n"
        "• Unauth violations never discounted",
        fontsize=6.7, color=TEXT_DARK, zorder=4, linespacing=1.25)

# 3B: Weighted Risk & EWMA
b3b = mpatches.FancyBboxPatch((X_LEFT + 3.73, s3_y + 0.12), cw3, 1.05, boxstyle="round,pad=0.04", fc="#FFFFFF", ec=PURPLE, lw=0.9, zorder=3)
ax.add_patch(b3b)
ax.text(X_LEFT + 3.83, s3_y + 0.95, "Weighted Risk & EWMA", fontsize=7.2, fontweight="bold", color=PURPLE, zorder=4)
ax.text(X_LEFT + 3.83, s3_y + 0.50,
        "Risk = 0.30 Unauth + 0.25 AuthFail\n"
        "       + 0.20 Rate + 0.15 Pay + 0.10 Conn\n"
        "Trust_t = 0.70 Trust_(t-1) + 0.30 Trust_raw\n"
        "• Critical Override: Unauth forces Trust=0",
        fontsize=6.7, color=TEXT_DARK, zorder=4, linespacing=1.25)

# 3C: Confidence Engine
b3c = mpatches.FancyBboxPatch((X_LEFT + 7.28, s3_y + 0.12), cw3, 1.05, boxstyle="round,pad=0.04", fc="#FFFFFF", ec=DARK_NAVY, lw=0.9, zorder=3)
ax.add_patch(b3c)
ax.text(X_LEFT + 7.38, s3_y + 0.95, "Evidence Confidence (C)", fontsize=7.2, fontweight="bold", color=DARK_NAVY, zorder=4)
ax.text(X_LEFT + 7.38, s3_y + 0.50,
        "C = 0.40 C_sample + 0.35 C_stability\n"
        "    + 0.25 C_agreement\n"
        "• Bounded in [0, 1] by sample count & variance\n"
        "• Suppresses DENY on sparse data",
        fontsize=6.7, color=TEXT_DARK, zorder=4, linespacing=1.25)

# Downward Arrow Stage 3 -> Stage 4
ax.annotate("", xy=(X_LEFT + STAGE_W/2, 2.50), xytext=(X_LEFT + STAGE_W/2, s3_y), arrowprops=arrow_kw, zorder=5)
ax.text(X_LEFT + STAGE_W/2 + 0.15, 2.70, "Adaptive Policy Mapping", fontsize=7.2, color="#475569", style="italic", zorder=5)


# ─────────────────────────────────────────────────────────────────────────────
# STAGE 4: ADAPTIVE ACCESS CONTROL POLICY & MOSQUITTO BROKER ENFORCEMENT
# ─────────────────────────────────────────────────────────────────────────────
s4_y = 0.85
s4_h = 1.65

s4_box = mpatches.FancyBboxPatch((X_LEFT, s4_y), STAGE_W, s4_h, boxstyle="round,pad=0.06", fc=GREEN_BG, ec=GREEN, lw=1.5, zorder=2)
ax.add_patch(s4_box)

s4_stripe = mpatches.FancyBboxPatch((X_LEFT, s4_y + s4_h - 0.36), STAGE_W, 0.36, boxstyle="round,pad=0.0", fc=GREEN, ec="none", zorder=3)
ax.add_patch(s4_stripe)
ax.text(X_LEFT + 0.25, s4_y + s4_h - 0.18, "STAGE 4: Adaptive Access Policy & Dynamic Mosquitto ACL Enforcement (PEP)", ha="left", va="center", fontsize=8.5, fontweight="bold", color="white", zorder=4)

# 4 Outcome Policy Cards across Stage 4
cw4 = 2.50
# Card 1: ALLOW
p1 = mpatches.FancyBboxPatch((X_LEFT + 0.16, s4_y + 0.12), cw4, 1.05, boxstyle="round,pad=0.04", fc="#FFFFFF", ec=GREEN, lw=1.0, zorder=3)
ax.add_patch(p1)
ax.text(X_LEFT + 0.26, s4_y + 0.95, "ALLOW (Trust >= 80, C >= 0.6)", fontsize=7.0, fontweight="bold", color=GREEN, zorder=4)
ax.text(X_LEFT + 0.26, s4_y + 0.50,
        "• Full access to registered topics\n"
        "• Normal publish & subscribe\n"
        "• Reassessment window: 30s",
        fontsize=6.6, color=TEXT_DARK, zorder=4, linespacing=1.25)

# Card 2: RESTRICT
p2 = mpatches.FancyBboxPatch((X_LEFT + 2.82, s4_y + 0.12), cw4, 1.05, boxstyle="round,pad=0.04", fc="#FFFFFF", ec=AMBER, lw=1.0, zorder=3)
ax.add_patch(p2)
ax.text(X_LEFT + 2.92, s4_y + 0.95, "RESTRICT (50 <= Trust < 80)", fontsize=7.0, fontweight="bold", color=AMBER, zorder=4)
ax.text(X_LEFT + 2.92, s4_y + 0.50,
        "• Actuator control topics stripped\n"
        "• Telemetry throttled / read-only\n"
        "• Reassessment window: 10s",
        fontsize=6.6, color=TEXT_DARK, zorder=4, linespacing=1.25)

# Card 3: CHALLENGE
p3 = mpatches.FancyBboxPatch((X_LEFT + 5.48, s4_y + 0.12), cw4, 1.05, boxstyle="round,pad=0.04", fc="#FFFFFF", ec=BLUE, lw=1.0, zorder=3)
ax.add_patch(p3)
ax.text(X_LEFT + 5.58, s4_y + 0.95, "CHALLENGE (C < 0.40)", fontsize=7.0, fontweight="bold", color=BLUE, zorder=4)
ax.text(X_LEFT + 5.58, s4_y + 0.50,
        "• Low evidence confidence\n"
        "• Transmit fresh cryptographic nonce\n"
        "• Device must reply in 5 seconds",
        fontsize=6.6, color=TEXT_DARK, zorder=4, linespacing=1.25)

# Card 4: DENY
p4 = mpatches.FancyBboxPatch((X_LEFT + 8.14, s4_y + 0.12), cw4, 1.05, boxstyle="round,pad=0.04", fc="#FFFFFF", ec=RED, lw=1.0, zorder=3)
ax.add_patch(p4)
ax.text(X_LEFT + 8.24, s4_y + 0.95, "DENY (Trust < 50 / Override)", fontsize=7.0, fontweight="bold", color=RED, zorder=4)
ax.text(X_LEFT + 8.24, s4_y + 0.50,
        "• Broker ACL instantly revoked\n"
        "• Active TCP socket terminated\n"
        "• Reassessment window: 2s",
        fontsize=6.6, color=TEXT_DARK, zorder=4, linespacing=1.25)


# ─────────────────────────────────────────────────────────────────────────────
# CONTINUOUS FEEDBACK LOOP ARROW (LEFT SIDE: STAGE 4 -> STAGE 1)
# ─────────────────────────────────────────────────────────────────────────────
# Clean vertical conduit on the left: x = 0.8
loop_x = 0.75
ax.plot([X_LEFT, loop_x], [s4_y + s4_h/2, s4_y + s4_h/2], color=GREEN, lw=2.2, zorder=5)
ax.plot([loop_x, loop_x], [s4_y + s4_h/2, s1_y + s1_h/2], color=GREEN, lw=2.2, zorder=5)
ax.annotate("", xy=(X_LEFT, s1_y + s1_h/2), xytext=(loop_x, s1_y + s1_h/2),
            arrowprops=dict(arrowstyle="->,head_width=0.30,head_length=0.25", lw=2.2, color=GREEN),
            zorder=5)

# Vertical label along the feedback arrow
ax.text(loop_x - 0.20, (s1_y + s4_y)/2 + 0.8,
        "⟲ CONTINUOUS FEEDBACK LOOP: Live Mosquitto ACL Synchronization for Subsequent Messages",
        ha="center", va="center", fontsize=7.6, fontweight="bold", color=GREEN, rotation=90, zorder=6)

plt.tight_layout(pad=0.2)
plt.savefig(str(OUTPUT_FILE), dpi=250, bbox_inches="tight", facecolor="white")
plt.close()
print(f"SUCCESS: Generated clean vertical architecture workflow diagram at {OUTPUT_FILE}")
