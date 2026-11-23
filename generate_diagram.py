"""
Generates a publication-grade, high-resolution workflow diagram image for
the Zero Trust IoT Security Framework using Matplotlib.
Saved to assets/workflow_diagram.png for embedding into README.md and PDF.
"""
import os
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches

OUTPUT_DIR = Path("assets")
OUTPUT_DIR.mkdir(exist_ok=True)
OUTPUT_PATH = OUTPUT_DIR / "workflow_diagram.png"

def generate_diagram():
    # High resolution 16:9 canvas
    fig, ax = plt.subplots(figsize=(14, 8), dpi=300)
    ax.set_facecolor('#0B0F19')
    fig.patch.set_facecolor('#0B0F19')

    # Color Palette (Dark Cybersecurity Theme)
    c_blue = '#0284C7'
    c_cyan = '#00F0FF'
    c_green = '#10B981'
    c_yellow = '#F59E0B'
    c_purple = '#8B5CF6'
    c_red = '#EF4444'
    c_box = '#131B2E'
    c_border = '#1E293B'
    c_text = '#F8FAFC'
    c_subtext = '#94A3B8'

    # Title Banner
    ax.text(7.0, 7.6, "END-TO-END ZERO TRUST OPERATIONAL WORKFLOW", 
            fontsize=16, fontweight='bold', color='#FFFFFF', ha='center', va='center')
    ax.text(7.0, 7.25, "Continuous Behaviour Evaluation • Fleet Network Context Awareness • Adaptive Policy Enforcement", 
            fontsize=10, color=c_cyan, ha='center', va='center')

    # Stage Box Dimensions
    w_box = 2.4
    h_box = 1.35
    y_top = 5.3
    y_bot = 2.3

    # STAGE 1: Telemetry Ingestion
    box1 = patches.FancyBboxPatch((0.4, y_top), w_box, h_box, boxstyle="round,pad=0.08", 
                                  edgecolor=c_cyan, facecolor=c_box, linewidth=1.5)
    ax.add_patch(box1)
    ax.text(0.4 + w_box/2, y_top + h_box - 0.22, "1. TELEMETRY INGESTION", fontsize=9, fontweight='bold', color=c_cyan, ha='center')
    ax.text(0.4 + w_box/2, y_top + 0.55, "• 5 Virtual IoT Devices\n• Timestamps & Nonces\n• Sequence Numbers\n• Payload Telemetry", 
            fontsize=7.5, color=c_text, ha='center', va='center')

    # STAGE 2: Real-Time Broker Enforcement
    box2 = patches.FancyBboxPatch((3.7, y_top), w_box, h_box, boxstyle="round,pad=0.08", 
                                  edgecolor=c_blue, facecolor=c_box, linewidth=1.5)
    ax.add_patch(box2)
    ax.text(3.7 + w_box/2, y_top + h_box - 0.22, "2. BROKER ACL FILTER", fontsize=9, fontweight='bold', color=c_blue, ha='center')
    ax.text(3.7 + w_box/2, y_top + 0.55, "• Inspect Policy State\n• Enforce Topic Whitelist\n• Block DENIED Devices\n• Log Unauthorized Attempts", 
            fontsize=7.5, color=c_text, ha='center', va='center')

    # STAGE 3: Dual-Stream Feature Extraction
    box3 = patches.FancyBboxPatch((7.0, y_top), w_box, h_box, boxstyle="round,pad=0.08", 
                                  edgecolor=c_purple, facecolor=c_box, linewidth=1.5)
    ax.add_patch(box3)
    ax.text(7.0 + w_box/2, y_top + h_box - 0.22, "3. FEATURE EXTRACTION", fontsize=9, fontweight='bold', color=c_purple, ha='center')
    ax.text(7.0 + w_box/2, y_top + 0.55, "• Sliding-Window Rate (Hz)\n• Payload Size Deviation\n• Replay/Duplicate Nonce\n• Multi-Device Latency Ping", 
            fontsize=7.5, color=c_text, ha='center', va='center')

    # STAGE 4: Context & Confidence Engine
    box4 = patches.FancyBboxPatch((10.3, y_top), w_box, h_box, boxstyle="round,pad=0.08", 
                                  edgecolor=c_yellow, facecolor=c_box, linewidth=1.5)
    ax.add_patch(box4)
    ax.text(10.3 + w_box/2, y_top + h_box - 0.22, "4. CONTEXT & CONFIDENCE", fontsize=9, fontweight='bold', color=c_yellow, ha='center')
    ax.text(10.3 + w_box/2, y_top + 0.55, "• Fleet Congestion Detection\n• 70% Rate Penalty Discount\n• Uncalibrated Confidence C\n• Hard Violations Preserved", 
            fontsize=7.5, color=c_text, ha='center', va='center')

    # STAGE 5: Trust Evaluation Engine
    box5 = patches.FancyBboxPatch((10.3, y_bot), w_box, h_box, boxstyle="round,pad=0.08", 
                                  edgecolor=c_green, facecolor=c_box, linewidth=1.5)
    ax.add_patch(box5)
    ax.text(10.3 + w_box/2, y_bot + h_box - 0.22, "5. TRUST ENGINE", fontsize=9, fontweight='bold', color=c_green, ha='center')
    ax.text(10.3 + w_box/2, y_bot + 0.55, "• 5-Factor Weighted Risk\n• Raw Trust = 100*(1-Risk)\n• Smoothing (alpha = 0.70)\n• Critical Security Overrides", 
            fontsize=7.5, color=c_text, ha='center', va='center')

    # STAGE 6: Zero Trust Policy Decision
    box6 = patches.FancyBboxPatch((5.4, y_bot - 0.1), 3.8, h_box + 0.2, boxstyle="round,pad=0.08", 
                                  edgecolor='#38BDF8', facecolor=c_box, linewidth=2.0)
    ax.add_patch(box6)
    ax.text(5.4 + 3.8/2, y_bot + h_box - 0.05, "6. ZERO TRUST POLICY DECISION ENGINE", fontsize=9.5, fontweight='bold', color='#38BDF8', ha='center')
    
    # Policy Decision Sub-Badges
    badge_y = y_bot + 0.35
    ax.text(5.9, badge_y + 0.45, "ALLOW (Trust >= 80)", fontsize=7.5, fontweight='bold', color=c_green, ha='center',
            bbox=dict(boxstyle="square,pad=0.2", fc='#064E3B', ec=c_green, lw=1))
    ax.text(8.7, badge_y + 0.45, "RESTRICT (50 - 79)", fontsize=7.5, fontweight='bold', color=c_yellow, ha='center',
            bbox=dict(boxstyle="square,pad=0.2", fc='#78350F', ec=c_yellow, lw=1))
    ax.text(5.9, badge_y, "CHALLENGE (Low Conf)", fontsize=7.5, fontweight='bold', color=c_purple, ha='center',
            bbox=dict(boxstyle="square,pad=0.2", fc='#4C1D95', ec=c_purple, lw=1))
    ax.text(8.7, badge_y, "DENY (< 50 or Violation)", fontsize=7.5, fontweight='bold', color=c_red, ha='center',
            bbox=dict(boxstyle="square,pad=0.2", fc='#7F1D1D', ec=c_red, lw=1))

    # STAGE 7: Dynamic Enforcement & Feedback Loop
    box7 = patches.FancyBboxPatch((0.4, y_bot), 3.8, h_box, boxstyle="round,pad=0.08", 
                                  edgecolor=c_cyan, facecolor=c_box, linewidth=1.5)
    ax.add_patch(box7)
    ax.text(0.4 + 3.8/2, y_bot + h_box - 0.22, "7. ADAPTIVE ENFORCEMENT & AUDIT", fontsize=9, fontweight='bold', color=c_cyan, ha='center')
    ax.text(0.4 + 3.8/2, y_bot + 0.55, "• Dynamic Mosquitto ACL Generation\n• Modulate Assessment Interval (2s / 10s / 30s)\n• SQLite Audit Event Log & Streamlit SOC\n• Feedback Loop: Updates Next Cycle Permissions", 
            fontsize=7.5, color=c_text, ha='center', va='center')

    # Draw Arrows Connecting Stages
    arrow_props = dict(arrowstyle="->,head_width=0.35,head_length=0.45", lw=1.8, color='#38BDF8')
    
    # 1 -> 2
    ax.annotate("", xy=(3.7, y_top + h_box/2), xytext=(2.8, y_top + h_box/2), arrowprops=arrow_props)
    # 2 -> 3
    ax.annotate("", xy=(7.0, y_top + h_box/2), xytext=(6.1, y_top + h_box/2), arrowprops=arrow_props)
    # 3 -> 4
    ax.annotate("", xy=(10.3, y_top + h_box/2), xytext=(9.4, y_top + h_box/2), arrowprops=arrow_props)
    # 4 -> 5 (Vertical down)
    ax.annotate("", xy=(11.5, y_bot + h_box), xytext=(11.5, y_top), arrowprops=arrow_props)
    # 5 -> 6 (Horizontal left)
    ax.annotate("", xy=(9.2, y_bot + h_box/2), xytext=(10.3, y_bot + h_box/2), arrowprops=arrow_props)
    # 6 -> 7 (Horizontal left)
    ax.annotate("", xy=(4.2, y_bot + h_box/2), xytext=(5.4, y_bot + h_box/2), arrowprops=arrow_props)
    # 7 -> 2 (Feedback loop arrow: vertical up to broker)
    feedback_arrow = dict(arrowstyle="->,head_width=0.35,head_length=0.45", lw=1.8, color='#00FFA3', linestyle='--')
    ax.annotate("", xy=(4.9, y_top), xytext=(2.3, y_bot + h_box),
                arrowprops=dict(arrowstyle="->,head_width=0.35,head_length=0.45", lw=1.8, color='#00FFA3',
                                connectionstyle="angle,angleA=0,angleB=90,rad=10"))
    ax.text(3.3, 4.0, "DYNAMIC ACL FEEDBACK (Loop)", fontsize=7.5, fontweight='bold', color='#00FFA3', rotation=90, va='center')

    # Bottom Legend / Footer
    ax.text(7.0, 0.45, "Zero Trust Principle: Never Trust, Always Verify • Even Authenticated Devices Undergo Continuous Behavioural Scrutiny", 
            fontsize=8.5, fontstyle='italic', color=c_subtext, ha='center', va='center')

    ax.set_xlim(0, 13.5)
    ax.set_ylim(0, 8.2)
    ax.axis('off')

    plt.tight_layout()
    plt.savefig(OUTPUT_PATH, dpi=300, bbox_inches='tight', facecolor='#0B0F19')
    plt.close()
    print(f"SUCCESS: Generated workflow diagram image at {OUTPUT_PATH}")

if __name__ == "__main__":
    generate_diagram()
