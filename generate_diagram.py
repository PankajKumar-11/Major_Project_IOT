"""
Generates a crystal-clear, intuitive, and highly readable academic workflow diagram.
Clean professional styling with high contrast, large readable fonts,
and clear linear flow designed for university presentation slides and thesis report.
"""
import os
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches

OUTPUT_DIR = Path("assets")
OUTPUT_DIR.mkdir(exist_ok=True)
OUTPUT_PATH = OUTPUT_DIR / "workflow_diagram.png"

def generate_diagram():
    # 16:9 canvas with crisp resolution
    fig, ax = plt.subplots(figsize=(15, 8.5), dpi=300)
    
    # Clean professional slate/white background for maximum legibility in papers & slides
    bg_color = "#F8FAFC"
    fig.patch.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)

    # Color Palette: Distinct, clean academic colors
    c_slate_dark = "#0F172A"
    c_blue = "#0284C7"
    c_indigo = "#4F46E5"
    c_emerald = "#059669"
    c_amber = "#D97706"
    c_rose = "#E11D48"
    c_gray_border = "#CBD5E1"
    c_box_bg = "#FFFFFF"

    # Header Title
    ax.text(7.5, 8.0, "How It Works: Step-by-Step Zero Trust Operational Workflow", 
            fontsize=17, fontweight='bold', color=c_slate_dark, ha='center', va='center')
    ax.text(7.5, 7.6, "A continuous loop that inspects device behavior, prevents false congestion alarms, and dynamically enforces permissions.", 
            fontsize=10.5, color="#475569", ha='center', va='center')

    # STEP 1: IoT Device Telemetry
    s1 = patches.FancyBboxPatch((0.5, 4.6), 2.8, 2.4, boxstyle="round,pad=0.1", fc=c_box_bg, ec="#0284C7", lw=2)
    ax.add_patch(s1)
    ax.text(1.9, 6.7, "STEP 1: Device Message", fontsize=11, fontweight='bold', color="#0284C7", ha='center')
    ax.text(1.9, 5.65, 
            "IoT devices publish telemetry\nto MQTT topics.\n\n"
            "Each message contains:\n"
            "• Sensor data payload\n"
            "• Incrementing Seq Number\n"
            "• Fresh Random Nonce", 
            fontsize=9, color="#334155", ha='center', va='center')

    # STEP 2: Instant Gatekeeper
    s2 = patches.FancyBboxPatch((3.8, 4.6), 3.0, 2.4, boxstyle="round,pad=0.1", fc=c_box_bg, ec="#E11D48", lw=2)
    ax.add_patch(s2)
    ax.text(5.3, 6.7, "STEP 2: Broker Gatekeeper", fontsize=11, fontweight='bold', color="#E11D48", ha='center')
    ax.text(5.3, 5.65, 
            "Is the device permitted to\npublish to this topic right now?\n\n"
            "• If DENIED: Block & Alert!\n"
            "• If Unauthorized topic: Drop!\n"
            "• If ALLOWED: Route packet\n"
            "  and pass to behavior engine.", 
            fontsize=9, color="#334155", ha='center', va='center')

    # STEP 3: Dual Analysis (Behavior & Network)
    s3 = patches.FancyBboxPatch((7.3, 4.6), 3.4, 2.4, boxstyle="round,pad=0.1", fc=c_box_bg, ec="#4F46E5", lw=2)
    ax.add_patch(s3)
    ax.text(9.0, 6.7, "STEP 3: Dual Analysis", fontsize=11, fontweight='bold', color="#4F46E5", ha='center')
    ax.text(9.0, 5.65, 
            "The system checks two separate streams:\n\n"
            "A. Device Behaviour (Sliding Window):\n"
            "   Message rate, payload size variance,\n"
            "   duplicate nonce / replay checks.\n\n"
            "B. Fleet Network Health:\n"
            "   Measures latency across ALL devices.", 
            fontsize=8.5, color="#334155", ha='center', va='center')

    # STEP 4: Network Context Filter
    s4 = patches.FancyBboxPatch((11.2, 4.6), 3.3, 2.4, boxstyle="round,pad=0.1", fc=c_box_bg, ec="#D97706", lw=2)
    ax.add_patch(s4)
    ax.text(12.85, 6.7, "STEP 4: Context Awareness", fontsize=11, fontweight='bold', color="#D97706", ha='center')
    ax.text(12.85, 5.65, 
            "Key Question: Is the network slow\nor is the device being malicious?\n\n"
            "• If >= 60% of fleet experiences high\n"
            "  latency: Flag Network Congestion!\n\n"
            "• Discount rate/delay penalties by 70%\n"
            "  to prevent false isolation of\n"
            "  innocent devices.", 
            fontsize=8.5, color="#334155", ha='center', va='center')

    # STEP 5: Trust & Confidence Calculation
    s5 = patches.FancyBboxPatch((11.2, 1.2), 3.3, 2.5, boxstyle="round,pad=0.1", fc=c_box_bg, ec="#059669", lw=2)
    ax.add_patch(s5)
    ax.text(12.85, 3.4, "STEP 5: Trust & Risk Score", fontsize=11, fontweight='bold', color="#059669", ha='center')
    ax.text(12.85, 2.3, 
            "1. Weighted Risk Score:\n"
            "   Combines rate, unauth access,\n"
            "   auth failures, & payload jitter.\n\n"
            "2. Trust Score = 100 * (1 - Risk)\n\n"
            "3. Historical Smoothing (alpha=0.70)\n\n"
            "4. Immediate Security Overrides\n"
            "   (critical violations drop trust to 0)", 
            fontsize=8.5, color="#334155", ha='center', va='center')

    # STEP 6: 4 Policy Decisions (ALLOW / RESTRICT / CHALLENGE / DENY)
    s6 = patches.FancyBboxPatch((3.8, 0.8), 6.9, 2.9, boxstyle="round,pad=0.1", fc="#FFFFFF", ec="#0F172A", lw=2.5)
    ax.add_patch(s6)
    ax.text(7.25, 3.4, "STEP 6: Dynamic Zero Trust Access Policy Decision", fontsize=11.5, fontweight='bold', color=c_slate_dark, ha='center')

    # 4 Decision Cards inside Step 6
    # Card 1: ALLOW
    c1 = patches.FancyBboxPatch((4.0, 2.1), 3.1, 1.0, boxstyle="round,pad=0.05", fc="#ECFDF5", ec="#059669", lw=1.5)
    ax.add_patch(c1)
    ax.text(5.55, 2.8, "ALLOW (Trust >= 80)", fontsize=9, fontweight='bold', color="#059669", ha='center')
    ax.text(5.55, 2.35, "Full access to allowed topics.\nRe-evaluate in 30 seconds.", fontsize=7.5, color="#065F46", ha='center')

    # Card 2: RESTRICT
    c2 = patches.FancyBboxPatch((7.4, 2.1), 3.1, 1.0, boxstyle="round,pad=0.05", fc="#FFFBEB", ec="#D97706", lw=1.5)
    ax.add_patch(c2)
    ax.text(8.95, 2.8, "RESTRICT (Trust 50 - 79)", fontsize=9, fontweight='bold', color="#D97706", ha='center')
    ax.text(8.95, 2.35, "Block sensitive commands / motors.\nRe-evaluate in 10 seconds.", fontsize=7.5, color="#92400E", ha='center')

    # Card 3: CHALLENGE
    c3 = patches.FancyBboxPatch((4.0, 1.0), 3.1, 1.0, boxstyle="round,pad=0.05", fc="#EEF2FF", ec="#4F46E5", lw=1.5)
    ax.add_patch(c3)
    ax.text(5.55, 1.7, "CHALLENGE (Low Evidence)", fontsize=9, fontweight='bold', color="#4F46E5", ha='center')
    ax.text(5.55, 1.25, "Confidence < 0.40. Issues crypto\nnonce challenge before isolating.", fontsize=7.5, color="#3730A3", ha='center')

    # Card 4: DENY
    c4 = patches.FancyBboxPatch((7.4, 1.0), 3.1, 1.0, boxstyle="round,pad=0.05", fc="#FFF1F2", ec="#E11D48", lw=1.5)
    ax.add_patch(c4)
    ax.text(8.95, 1.7, "DENY (Trust < 50 or Violation)", fontsize=9, fontweight='bold', color="#E11D48", ha='center')
    ax.text(8.95, 1.25, "Access revoked! Quarantined.\nImmediate critical override.", fontsize=7.5, color="#9F1239", ha='center')

    # STEP 7: Enforcement & Loop Feedback
    s7 = patches.FancyBboxPatch((0.5, 1.2), 2.8, 2.5, boxstyle="round,pad=0.1", fc=c_box_bg, ec="#0284C7", lw=2)
    ax.add_patch(s7)
    ax.text(1.9, 3.4, "STEP 7: Enforcement & Audit", fontsize=11, fontweight='bold', color="#0284C7", ha='center')
    ax.text(1.9, 2.3, 
            "1. Synchronizes Mosquitto ACL\n"
            "   file and broker in real time.\n\n"
            "2. Logs security event to SQLite.\n\n"
            "3. Updates SOC Dashboard.\n\n"
            "4. FEEDS BACK into Step 2\n"
            "   for next incoming message!", 
            fontsize=8.5, color="#334155", ha='center', va='center')

    # Connecting Arrows
    arrow = dict(arrowstyle="->,head_width=0.4,head_length=0.45", lw=2, color="#0284C7")
    
    # 1 -> 2
    ax.annotate("", xy=(3.8, 5.8), xytext=(3.3, 5.8), arrowprops=arrow)
    # 2 -> 3
    ax.annotate("", xy=(7.3, 5.8), xytext=(6.8, 5.8), arrowprops=arrow)
    # 3 -> 4
    ax.annotate("", xy=(11.2, 5.8), xytext=(10.7, 5.8), arrowprops=arrow)
    # 4 -> 5 (Vertical down)
    ax.annotate("", xy=(12.85, 3.7), xytext=(12.85, 4.6), arrowprops=arrow)
    # 5 -> 6 (Horizontal left into Step 6)
    ax.annotate("", xy=(10.7, 2.3), xytext=(11.2, 2.3), arrowprops=arrow)
    # 6 -> 7 (Horizontal left into Step 7)
    ax.annotate("", xy=(3.3, 2.3), xytext=(3.8, 2.3), arrowprops=arrow)
    # 7 -> 2 (Feedback loop arrow: vertical up to Gatekeeper)
    ax.annotate("", xy=(3.8, 5.3), xytext=(1.9, 3.7),
                arrowprops=dict(arrowstyle="->,head_width=0.4,head_length=0.45", lw=2.2, color="#059669",
                                connectionstyle="angle,angleA=90,angleB=180,rad=8"))
    ax.text(2.6, 4.25, "FEEDBACK LOOP\n(Updates ACL Permissions)", 
            fontsize=7.5, fontweight='bold', color="#059669", ha='center', va='center')

    ax.set_xlim(0, 15)
    ax.set_ylim(0.4, 8.4)
    ax.axis('off')

    plt.tight_layout()
    plt.savefig(OUTPUT_PATH, dpi=300, bbox_inches='tight', facecolor=bg_color)
    plt.close()
    print(f"SUCCESS: Generated clear, intuitive workflow diagram at {OUTPUT_PATH}")

if __name__ == "__main__":
    generate_diagram()
