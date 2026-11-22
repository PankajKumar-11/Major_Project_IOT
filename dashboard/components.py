"""
Reusable Plotly Charts and UI Styling for Streamlit Cybersecurity Dashboard.
Dark Cybersecurity Theme with High-Contrast Scientific Visualizations.
"""
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import List, Dict, Any

CYBER_THEME = {
    "bg_color": "#0E131F",
    "paper_color": "#131B2E",
    "text_color": "#E2E8F0",
    "grid_color": "#1E293B",
    "cyan": "#00F0FF",
    "green": "#00FFA3",
    "red": "#FF3366",
    "yellow": "#FFD166",
    "purple": "#BD93F9"
}

CYBER_CSS = """
<style>
    /* Dark Cybersecurity Global Styling */
    .stApp {
        background-color: #0B0F19;
        color: #E2E8F0;
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
    }
    
    /* Metric Cards */
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #131B2E 0%, #1A233A 100%);
        border: 1px solid #1E293B;
        border-radius: 8px;
        padding: 12px 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.4);
    }
    div[data-testid="stMetric"]:hover {
        border-color: #00F0FF;
        box-shadow: 0 0 12px rgba(0, 240, 255, 0.25);
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #F8FAFC;
        font-weight: 600;
        letter-spacing: -0.02em;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #080C14;
        border-right: 1px solid #1E293B;
    }
    
    /* Status Badges */
    .badge-allow {
        background-color: rgba(0, 255, 163, 0.15);
        color: #00FFA3;
        border: 1px solid #00FFA3;
        padding: 2px 8px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.85em;
    }
    .badge-restrict {
        background-color: rgba(255, 209, 102, 0.15);
        color: #FFD166;
        border: 1px solid #FFD166;
        padding: 2px 8px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.85em;
    }
    .badge-deny {
        background-color: rgba(255, 51, 102, 0.15);
        color: #FF3366;
        border: 1px solid #FF3366;
        padding: 2px 8px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.85em;
    }
    .badge-challenge {
        background-color: rgba(189, 147, 249, 0.15);
        color: #BD93F9;
        border: 1px solid #BD93F9;
        padding: 2px 8px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.85em;
    }
</style>
"""

def create_trust_timeline_chart(history_records: List[Dict[str, Any]], device_id: str) -> go.Figure:
    """Generates continuous trust score timeline with threshold zones."""
    if not history_records:
        fig = go.Figure()
        fig.add_annotation(text="No trust history recorded yet", showarrow=False, font=dict(color="#94A3B8"))
        fig.update_layout(paper_bgcolor=CYBER_THEME["paper_color"], plot_bgcolor=CYBER_THEME["bg_color"])
        return fig

    df = pd.DataFrame(history_records)
    df["id"] = range(1, len(df) + 1)

    fig = go.Figure()

    # Threshold horizontal reference lines and shaded zones
    fig.add_hrect(y0=80, y1=100, fillcolor="rgba(0, 255, 163, 0.08)", line_width=0, annotation_text="ALLOW ZONE (Trust >= 80)", annotation_position="top left", annotation_font_color="#00FFA3")
    fig.add_hrect(y0=50, y1=80, fillcolor="rgba(255, 209, 102, 0.08)", line_width=0, annotation_text="RESTRICT ZONE (50 - 80)", annotation_position="left", annotation_font_color="#FFD166")
    fig.add_hrect(y0=0, y1=50, fillcolor="rgba(255, 51, 102, 0.08)", line_width=0, annotation_text="DENY ZONE (Trust < 50)", annotation_position="bottom left", annotation_font_color="#FF3366")

    # Smoothed Trust Line
    fig.add_trace(go.Scatter(
        x=df["id"],
        y=df["smoothed_trust"],
        mode="lines+markers",
        name="Smoothed Trust Score",
        line=dict(color=CYBER_THEME["cyan"], width=3),
        marker=dict(size=6, color=CYBER_THEME["cyan"])
    ))

    # Raw Calculated Trust Line
    fig.add_trace(go.Scatter(
        x=df["id"],
        y=df["calculated_trust"],
        mode="lines",
        name="Instant Raw Trust",
        line=dict(color="#64748B", width=1.5, dash="dash")
    ))

    # Confidence Score Trace (scaled to 100 for overlay)
    if "confidence_score" in df.columns:
        fig.add_trace(go.Scatter(
            x=df["id"],
            y=df["confidence_score"] * 100.0,
            mode="lines",
            name="Evidence Confidence (x100)",
            line=dict(color=CYBER_THEME["purple"], width=1.5, dash="dot")
        ))

    fig.update_layout(
        title=f"Continuous Trust Evolution & Policy Thresholds — {device_id}",
        xaxis_title="Evaluation Step",
        yaxis_title="Trust Score (0 - 100)",
        yaxis=dict(range=[0, 105], gridcolor=CYBER_THEME["grid_color"]),
        xaxis=dict(gridcolor=CYBER_THEME["grid_color"]),
        paper_bgcolor=CYBER_THEME["paper_color"],
        plot_bgcolor=CYBER_THEME["bg_color"],
        font=dict(color=CYBER_THEME["text_color"]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=40, r=40, t=60, b=40)
    )
    return fig

def create_risk_radar_chart(breakdown: Dict[str, Any]) -> go.Figure:
    """Radar chart showing 5 risk anomaly dimensions."""
    categories = [
        "Rate Anomaly",
        "Unauthorized Topic",
        "Auth Failures",
        "Payload Anomaly",
        "Connection Anomaly"
    ]
    values = [
        breakdown.get("effective_rate_anomaly", breakdown.get("rate_anomaly", 0.0)),
        breakdown.get("unauth_anomaly", 0.0),
        breakdown.get("auth_fail_anomaly", 0.0),
        breakdown.get("payload_anomaly", 0.0),
        breakdown.get("effective_conn_anomaly", breakdown.get("conn_anomaly", 0.0))
    ]
    # Close radar loop
    categories.append(categories[0])
    values.append(values[0])

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill="toself",
        fillcolor="rgba(0, 240, 255, 0.25)",
        line=dict(color=CYBER_THEME["cyan"], width=2),
        name="Risk Anomaly Profile"
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1.0], gridcolor=CYBER_THEME["grid_color"], color="#94A3B8"),
            angularaxis=dict(gridcolor=CYBER_THEME["grid_color"], color=CYBER_THEME["text_color"]),
            bgcolor=CYBER_THEME["bg_color"]
        ),
        paper_bgcolor=CYBER_THEME["paper_color"],
        font=dict(color=CYBER_THEME["text_color"]),
        title="Multidimensional Risk Breakdown [0.0 - 1.0]",
        margin=dict(l=40, r=40, t=50, b=40)
    )
    return fig

def create_network_timeline(metrics: List[Dict[str, Any]]) -> go.Figure:
    """Dual-axis timeline of Latency (ms) and Throughput (msg/s)."""
    if not metrics:
        fig = go.Figure()
        fig.add_annotation(text="No network telemetry yet", showarrow=False, font=dict(color="#94A3B8"))
        fig.update_layout(paper_bgcolor=CYBER_THEME["paper_color"], plot_bgcolor=CYBER_THEME["bg_color"])
        return fig

    df = pd.DataFrame(metrics)
    df["step"] = range(1, len(df) + 1)

    fig = go.Figure()

    # Latency line
    fig.add_trace(go.Scatter(
        x=df["step"],
        y=df["avg_latency_ms"],
        name="Average Latency (ms)",
        line=dict(color=CYBER_THEME["yellow"], width=2.5),
        mode="lines+markers"
    ))

    # Highlight Congestion threshold
    fig.add_hline(y=120.0, line_dash="dash", line_color=CYBER_THEME["red"], annotation_text="Congestion Threshold (120ms)", annotation_font_color=CYBER_THEME["red"])

    fig.update_layout(
        title="Network Telemetry & Congestion Detection Timeline",
        xaxis_title="Time Sample",
        yaxis_title="Latency (ms)",
        paper_bgcolor=CYBER_THEME["paper_color"],
        plot_bgcolor=CYBER_THEME["bg_color"],
        font=dict(color=CYBER_THEME["text_color"]),
        xaxis=dict(gridcolor=CYBER_THEME["grid_color"]),
        yaxis=dict(gridcolor=CYBER_THEME["grid_color"]),
        margin=dict(l=40, r=40, t=50, b=40)
    )
    return fig

def create_benchmark_comparison_bar(df_comp: pd.DataFrame) -> go.Figure:
    """Grouped bar chart comparing S1, S2, S3, and S4 across metrics."""
    metrics_to_plot = ["precision", "recall", "f1_score", "false_positive_rate"]
    display_names = ["Precision", "Recall", "F1 Score", "False Positive Rate (FPR)"]

    fig = go.Figure()

    colors = [CYBER_THEME["cyan"], CYBER_THEME["green"], CYBER_THEME["yellow"], CYBER_THEME["red"]]

    for i, col in enumerate(metrics_to_plot):
        fig.add_trace(go.Bar(
            name=display_names[i],
            x=df_comp["model_id"] + " (" + df_comp["model_name"] + ")",
            y=df_comp[col],
            marker_color=colors[i]
        ))

    fig.update_layout(
        barmode="group",
        title="Comparative Framework Evaluation: S1 vs S2 vs S3 vs S4",
        yaxis_title="Score [0.0 - 1.0]",
        yaxis=dict(range=[0, 1.05], gridcolor=CYBER_THEME["grid_color"]),
        xaxis=dict(gridcolor=CYBER_THEME["grid_color"]),
        paper_bgcolor=CYBER_THEME["paper_color"],
        plot_bgcolor=CYBER_THEME["bg_color"],
        font=dict(color=CYBER_THEME["text_color"]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=40, r=40, t=60, b=40)
    )
    return fig

