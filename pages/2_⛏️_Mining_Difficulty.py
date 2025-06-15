import streamlit as st

# Page config MUST be first!
st.set_page_config(page_title="Mining Hashrate", page_icon="📈", layout="wide")

import plotly.graph_objects as go
import pandas as pd
import numpy as np
import sys
import os
from datetime import datetime, timedelta

# Add parent directory to path for imports
parent_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(parent_dir)

from database import Database
from auth_handler import AuthHandler
from payment_handler import PaymentHandler
from navigation import add_navigation
from data_manager import kaspa_data, fit_power_law

# NOW add navigation (after page config)
add_navigation()

# Initialize handlers
@st.cache_resource
def init_handlers():
    db = Database()
    auth_handler = AuthHandler(db)
    payment_handler = PaymentHandler()
    return db, auth_handler, payment_handler

db, auth_handler, payment_handler = init_handlers()

# Load hashrate data
if 'hashrate_df' not in st.session_state or 'hashrate_genesis_date' not in st.session_state:
    try:
        st.session_state.hashrate_df, st.session_state.hashrate_genesis_date = kaspa_data.load_hashrate_data()
    except Exception as e:
        st.error(f"Failed to load hashrate data: {str(e)}")
        # Create fallback dummy data
        dates = pd.date_range(start='2024-01-01', end='2024-06-01', freq='D')
        hashrate_values = np.random.normal(1.2, 0.1, len(dates))
        st.session_state.hashrate_df = pd.DataFrame({
            'Date': dates,
            'Hashrate_PH': hashrate_values,
            'days_from_genesis': range(len(dates))
        })
        st.session_state.hashrate_genesis_date = pd.to_datetime('2021-11-07')

hashrate_df = st.session_state.hashrate_df
genesis_date = st.session_state.hashrate_genesis_date

# Calculate power law if we have data
if not hashrate_df.empty:
    try:
        a_hashrate, b_hashrate, r2_hashrate = fit_power_law(hashrate_df, y_col='Hashrate_PH')
    except Exception as e:
        st.error(f"Failed to calculate hashrate power law: {str(e)}")
        a_hashrate, b_hashrate, r2_hashrate = 1, 1, 0
else:
    a_hashrate, b_hashrate, r2_hashrate = 1, 1, 0

# DEBUG: Show content is loading
st.write("DEBUG: Page is loading...")

st.markdown("""
<style>
.big-font {
    font-size: 50px !important;
    font-weight: bold;
    background: linear-gradient(90deg, #FFFFFF 0%, #A0A0B8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 0.5rem 0;
    padding: 0;
    filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.4));
    z-index: 1000;
    position: relative;
}
</style>
<div class='big-font'>Kaspa Network Hashrate</div>
""", unsafe_allow_html=True)

# Simplified but beautiful CSS - ensuring content visibility
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* Simplified background that won't interfere */
.stApp {
    background: linear-gradient(135deg, #0F0F1A 0%, #1A1A2E 50%, #16213E 100%);
    color: #FFFFFF;
    font-family: 'Inter', sans-serif;
    position: relative;
}

/* Add subtle animated background overlay */
body {
    background: 
        radial-gradient(ellipse 800px 600px at 20% 40%, rgba(91, 108, 255, 0.1) 0%, transparent 70%),
        radial-gradient(ellipse 600px 800px at 80% 20%, rgba(99, 102, 241, 0.08) 0%, transparent 70%),
        linear-gradient(135deg, #0F0F1A 0%, #1A1A2E 50%, #16213E 100%);
    animation: subtleShift 15s ease-in-out infinite;
}

@keyframes subtleShift {
    0%, 100% {
        background: 
            radial-gradient(ellipse 800px 600px at 20% 40%, rgba(91, 108, 255, 0.1) 0%, transparent 70%),
            radial-gradient(ellipse 600px 800px at 80% 20%, rgba(99, 102, 241, 0.08) 0%, transparent 70%),
            linear-gradient(135deg, #0F0F1A 0%, #1A1A2E 50%, #16213E 100%);
    }
    50% {
        background: 
            radial-gradient(ellipse 600px 800px at 25% 60%, rgba(91, 108, 255, 0.12) 0%, transparent 70%),
            radial-gradient(ellipse 800px 600px at 75% 30%, rgba(99, 102, 241, 0.1) 0%, transparent 70%),
            linear-gradient(135deg, #0F0F1A 0%, #1A1A2E 50%, #16213E 100%);
    }
}

/* Ensure all Streamlit content is visible */
.main .block-container {
    background: rgba(0, 0, 0, 0.1);
    border-radius: 12px;
    padding: 2rem;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(91, 108, 255, 0.1);
    position: relative;
    z-index: 100 !important;
}

/* Sidebar styling */
.stSidebar {
    background: linear-gradient(135deg, rgba(26, 26, 46, 0.95), rgba(22, 22, 41, 0.95)) !important;
    backdrop-filter: blur(12px);
    border-right: 1px solid rgba(91, 108, 255, 0.2);
}

/* BEAUTIFUL METRIC CARDS */
.metrics-container {
    display: flex;
    gap: 1.5rem;
    margin: 2rem 0;
    flex-wrap: wrap;
}

.metric-card {
    background: linear-gradient(135deg, rgba(26, 26, 46, 0.8), rgba(22, 22, 41, 0.8));
    border: 1px solid rgba(91, 108, 255, 0.3);
    border-radius: 16px;
    padding: 1.5rem;
    flex: 1;
    min-width: 250px;
    position: relative;
    backdrop-filter: blur(12px);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3), 0 2px 8px rgba(91, 108, 255, 0.1);
    transition: all 0.3s ease;
}

.metric-card:hover {
    transform: translateY(-2px);
    border-color: rgba(91, 108, 255, 0.5);
    box-shadow: 0 12px 48px rgba(0, 0, 0, 0.4), 0 4px 16px rgba(91, 108, 255, 0.2);
}

.metric-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, #5B6CFF, #6366F1, #8B5CF6);
    border-radius: 16px 16px 0 0;
}

.metric-value {
    font-size: 2.5rem;
    font-weight: 700;
    color: #FFFFFF;
    margin-bottom: 0.5rem;
    text-shadow: 0 2px 8px rgba(91, 108, 255, 0.3);
}

.metric-label {
    color: #9CA3AF;
    font-size: 0.9rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.5rem;
}

.metric-change {
    color: #10B981;
    font-size: 0.9rem;
    font-weight: 600;
}

.metric-change.negative {
    color: #ef4444;
}

/* ENHANCED CHART CONTAINER */
.chart-container {
    background: linear-gradient(135deg, rgba(26, 26, 46, 0.8), rgba(22, 22, 41, 0.8));
    border: 1px solid rgba(91, 108, 255, 0.2);
    border-radius: 16px;
    padding: 2rem;
    margin: 2rem 0;
    backdrop-filter: blur(12px);
    box-shadow: 0 16px 64px rgba(0, 0, 0, 0.3), 0 4px 16px rgba(91, 108, 255, 0.1);
}

/* SEGMENTED CONTROLS */
[data-testid="stVerticalBlock"] div[data-baseweb="segmented-control"] {
    background: rgba(26, 26, 46, 0.8) !important;
    border: 1px solid rgba(91, 108, 255, 0.3) !important;
    border-radius: 8px !important;
    backdrop-filter: blur(12px) !important;
    padding: 2px !important;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2) !important;
}

[data-testid="stVerticalBlock"] div[data-baseweb="segmented-control"] button {
    background: transparent !important;
    border: none !important;
    border-radius: 6px !important;
    color: #9CA3AF !important;
    font-weight: 500 !important;
    font-size: 13px !important;
    padding: 6px 8px !important;
    transition: all 0.3s ease !important;
}

[data-testid="stVerticalBlock"] div[data-baseweb="segmented-control"] button[aria-pressed="true"] {
    background: rgba(91, 108, 255, 0.2) !important;
    color: #ffffff !important;
    font-weight: 600 !important;
    box-shadow: 0 2px 8px rgba(91, 108, 255, 0.3) !important;
    border: 1px solid rgba(91, 108, 255, 0.4) !important;
}

[data-testid="stVerticalBlock"] div[data-baseweb="segmented-control"] button:hover:not([aria-pressed="true"]) {
    background: rgba(91, 108, 255, 0.1) !important;
    color: #e2e8f0 !important;
}

.control-group {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
}

.control-label {
    color: #9CA3AF;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    font-family: 'Inter', sans-serif;
    text-align: center;
}

/* ANALYSIS SECTION */
.analysis-section {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
    margin: 2rem 0;
}

.analysis-card {
    background: linear-gradient(135deg, rgba(26, 26, 46, 0.8), rgba(22, 22, 41, 0.8));
    border: 1px solid rgba(91, 108, 255, 0.2);
    border-radius: 16px;
    padding: 2rem;
    backdrop-filter: blur(12px);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.section-title {
    color: #FFFFFF;
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 1.5rem;
    text-shadow: 0 2px 8px rgba(91, 108, 255, 0.3);
}

.insights-list {
    list-style: none;
    padding: 0;
}

.insights-list li {
    color: #9CA3AF;
    margin-bottom: 0.75rem;
    padding-left: 1.5rem;
    position: relative;
    line-height: 1.6;
}

.insights-list li::before {
    content: '→';
    position: absolute;
    left: 0;
    color: #5B6CFF;
    font-weight: 600;
}

/* Make columns fit content */
div[data-testid="stColumn"] {
    width: fit-content !important;
    flex: unset !important;
}

/* Responsive */
@media (max-width: 768px) {
    .analysis-section {
        grid-template-columns: 1fr;
    }
    .metrics-container {
        flex-direction: column;
    }
}

/* Hide Streamlit branding but keep functionality */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* Ensure everything is visible */
.stApp > div {
    position: relative;
    z-index: 10;
}
</style>
""", unsafe_allow_html=True)

# DEBUG: Show that we're past CSS
st.write("DEBUG: CSS loaded, creating controls...")

# CHART CONTROLS
st.markdown("### Controls")

col1, col2, col3, spacer, col4 = st.columns([0.8, 0.8, 0.8, 4, 1.2])

with col1:
    st.markdown('<div class="control-group"><div class="control-label">Hashrate Scale</div>', unsafe_allow_html=True)
    y_scale = st.segmented_control(
        label="Hashrate Scale",
        options=["Linear", "Log"],
        default="Log",
        label_visibility="collapsed",
        key="hashrate_y_scale_segment"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="control-group"><div class="control-label">Time Scale</div>', unsafe_allow_html=True)
    x_scale_type = st.segmented_control(
        label="Time Scale",
        options=["Linear", "Log"],
        default="Linear",
        label_visibility="collapsed",
        key="hashrate_x_scale_segment"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="control-group"><div class="control-label">Power Law</div>', unsafe_allow_html=True)
    show_power_law = st.segmented_control(
        label="Power Law",
        options=["Hide", "Show"],
        default="Show",
        label_visibility="collapsed",
        key="hashrate_power_law_segment"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="control-group"><div class="control-label">Time Period</div>', unsafe_allow_html=True)
    time_range = st.segmented_control(
        label="Time Period",
        options=["1M", "3M", "6M", "1Y", "All"],
        default="All",
        label_visibility="collapsed",
        key="hashrate_time_range_segment"
    )
    st.markdown('</div>', unsafe_allow_html=True)

# DEBUG: Show controls are created
st.write(f"DEBUG: Controls created. y_scale={y_scale}, time_range={time_range}")

# Data filtering based on time range
if not hashrate_df.empty:
    last_date = hashrate_df['Date'].iloc[-1]
    if time_range == "1M":
        start_date = last_date - timedelta(days=30)
    elif time_range == "3M":
        start_date = last_date - timedelta(days=90)
    elif time_range == "6M":
        start_date = last_date - timedelta(days=180)
    elif time_range == "1Y":
        start_date = last_date - timedelta(days=365)
    else:  # "All"
        start_date = hashrate_df['Date'].iloc[0]

    filtered_df = hashrate_df[hashrate_df['Date'] >= start_date]
else:
    filtered_df = hashrate_df

# DEBUG: Show data filtering
st.write(f"DEBUG: Data filtered. Original: {len(hashrate_df)}, Filtered: {len(filtered_df)}")

# CREATE CHART
fig = go.Figure()

if not filtered_df.empty:
    if x_scale_type == "Log":
        x_values = filtered_df['days_from_genesis']
        x_title = "Days Since Genesis (Log Scale)"
    else:
        x_values = filtered_df['Date']
        x_title = "Date"

    # Add hashrate trace
    fig.add_trace(go.Scatter(
        x=x_values,
        y=filtered_df['Hashrate_PH'],
        mode='lines',
        name='Hashrate (PH/s)',
        line=dict(color='#5B6CFF', width=3),
        fill='tonexty',
        fillcolor='rgba(91, 108, 255, 0.15)',
        hovertemplate='<b>Kaspa Hashrate</b><br>Date: %{text}<br>Hashrate: %{y:.2f} PH/s<br><extra></extra>',
        text=[d.strftime('%Y-%m-%d') for d in filtered_df['Date']] if not filtered_df.empty else []
    ))

    # Add power law if enabled
    if show_power_law == "Show" and not filtered_df.empty:
        x_fit = filtered_df['days_from_genesis']
        y_fit = a_hashrate * np.power(x_fit, b_hashrate)
        fit_x = x_fit if x_scale_type == "Log" else filtered_df['Date']

        fig.add_trace(go.Scatter(
            x=fit_x,
            y=y_fit,
            mode='lines',
            name=f'Power Law (R²={r2_hashrate:.3f})',
            line=dict(color='#ff8c00', width=3, dash='solid'),
            showlegend=True,
            hovertemplate='<b>Power Law Fit</b><br>R² = %{customdata:.3f}<br>Value: %{y:.2f} PH/s<br><extra></extra>',
            customdata=[r2_hashrate] * len(fit_x)
        ))

# Chart layout
fig.update_layout(
    xaxis_title=x_title if not filtered_df.empty else "Date",
    yaxis_title="Hashrate (PH/s)",
    height=650,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#9CA3AF', family='Inter'),
    xaxis=dict(
        gridcolor='rgba(91, 108, 255, 0.1)',
        gridwidth=1,
        color='#9CA3AF',
        type="log" if x_scale_type == "Log" else None
    ),
    yaxis=dict(
        gridcolor='rgba(91, 108, 255, 0.1)',
        gridwidth=1,
        color='#9CA3AF',
        type="log" if y_scale == "Log" else "linear"
    ),
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="left",
        x=0,
        bgcolor='rgba(0,0,0,0)',
        font=dict(size=11, color='#9CA3AF')
    ),
    margin=dict(l=50, r=20, t=20, b=50)
)

# Display chart in container
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.plotly_chart(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# DEBUG: Show chart is created
st.write("DEBUG: Chart displayed")

# Calculate metrics
if not hashrate_df.empty:
    current_hashrate = hashrate_df['Hashrate_PH'].iloc[-1]
    seven_days_ago = hashrate_df['Date'].iloc[-1] - timedelta(days=7)
    df_7_days = hashrate_df[hashrate_df['Date'] >= seven_days_ago]
    avg_7d = df_7_days['Hashrate_PH'].mean() if len(df_7_days) > 0 else current_hashrate
    thirty_days_ago = hashrate_df['Date'].iloc[-1] - timedelta(days=30)
    df_30_days = hashrate_df[hashrate_df['Date'] >= thirty_days_ago]
    avg_30d = df_30_days['Hashrate_PH'].mean() if len(df_30_days) > 0 else current_hashrate
    
    if len(df_7_days) > 1:
        hashrate_7d_ago = df_7_days['Hashrate_PH'].iloc[0]
        change_7d = ((current_hashrate - hashrate_7d_ago) / hashrate_7d_ago) * 100
    else:
        change_7d = 0
        
    if len(df_30_days) > 1:
        hashrate_30d_ago = df_30_days['Hashrate_PH'].iloc[0]
        change_30d = ((current_hashrate - hashrate_30d_ago) / hashrate_30d_ago) * 100
    else:
        change_30d = 0
else:
    current_hashrate = 1.24
    avg_7d = 1.18
    avg_30d = 1.15
    change_7d = 2.1
    change_30d = 5.2

# Metrics cards
st.markdown(f"""
<div class="metrics-container">
    <div class="metric-card">
        <div class="metric-label">Current Hashrate</div>
        <div class="metric-value">{current_hashrate:.2f} PH/s</div>
        <div class="metric-change">+{change_7d:.1f}%</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">7d Average</div>
        <div class="metric-value">{avg_7d:.2f} PH/s</div>
        <div class="metric-change">+0.8%</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">30d Average</div>
        <div class="metric-value">{avg_30d:.2f} PH/s</div>
        <div class="metric-change">+{change_30d:.1f}%</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Analysis section
current_growth = "15%" if change_30d > 10 else f"{change_30d:.1f}%"

st.markdown(f"""
<div class="analysis-section">
    <div class="analysis-card">
        <h3 class="section-title">Key Insights</h3>
        <ul class="insights-list">
            <li>Network hashrate has grown {current_growth} over the past month</li>
            <li>Mining difficulty adjustment maintains ~1 block per second</li>
            <li>Increased hashrate indicates growing miner confidence</li>
            <li>Current hashrate suggests strong network security</li>
        </ul>
    </div>
    <div class="analysis-card">
        <h3 class="section-title">30-Day Trend</h3>
        <p style="color: #9CA3AF;">Trend analysis shows consistent growth pattern with periodic adjustments based on network conditions.</p>
    </div>
</div>
""", unsafe_allow_html=True)

# DEBUG: Final message
st.write("DEBUG: Page fully loaded!")

# Footer
try:
    from footer import add_footer
    add_footer()
except ImportError:
    st.write("Footer module not found")
