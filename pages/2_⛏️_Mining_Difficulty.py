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
}
</style>
<div class='big-font'>Kaspa Network Hashrate</div>
""", unsafe_allow_html=True)

# Enhanced CSS with Beautiful Background Textures and Glow Effects
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* BEAUTIFUL ANIMATED BACKGROUND WITH MULTIPLE LAYERS */
.stApp {
    position: relative;
    background: #0A0A0F;
    color: #FFFFFF;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    overflow-x: hidden;
}

/* Main background with animated gradients */
.stApp::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: -1;
    background: 
        /* Primary gradient layer */
        radial-gradient(ellipse 800px 600px at 20% 40%, rgba(91, 108, 255, 0.15) 0%, transparent 50%),
        radial-gradient(ellipse 600px 800px at 80% 20%, rgba(99, 102, 241, 0.12) 0%, transparent 50%),
        radial-gradient(ellipse 1000px 400px at 50% 80%, rgba(139, 92, 246, 0.08) 0%, transparent 50%),
        /* Secondary glow effects */
        radial-gradient(circle 400px at 10% 90%, rgba(16, 185, 129, 0.05) 0%, transparent 70%),
        radial-gradient(circle 300px at 90% 10%, rgba(245, 158, 11, 0.04) 0%, transparent 70%),
        /* Base gradients */
        linear-gradient(135deg, #0F0F1A 0%, #1A1A2E 30%, #16213E 60%, #1A1A2E 100%);
    animation: backgroundShift 20s ease-in-out infinite;
}

/* Animated noise texture overlay */
.stApp::after {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: -1;
    background-image: 
        url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)' opacity='0.03'/%3E%3C/svg%3E");
    mix-blend-mode: overlay;
}

@keyframes backgroundShift {
    0%, 100% {
        background: 
            radial-gradient(ellipse 800px 600px at 20% 40%, rgba(91, 108, 255, 0.15) 0%, transparent 50%),
            radial-gradient(ellipse 600px 800px at 80% 20%, rgba(99, 102, 241, 0.12) 0%, transparent 50%),
            radial-gradient(ellipse 1000px 400px at 50% 80%, rgba(139, 92, 246, 0.08) 0%, transparent 50%),
            radial-gradient(circle 400px at 10% 90%, rgba(16, 185, 129, 0.05) 0%, transparent 70%),
            radial-gradient(circle 300px at 90% 10%, rgba(245, 158, 11, 0.04) 0%, transparent 70%),
            linear-gradient(135deg, #0F0F1A 0%, #1A1A2E 30%, #16213E 60%, #1A1A2E 100%);
    }
    50% {
        background: 
            radial-gradient(ellipse 600px 800px at 25% 60%, rgba(91, 108, 255, 0.18) 0%, transparent 50%),
            radial-gradient(ellipse 800px 600px at 75% 30%, rgba(99, 102, 241, 0.15) 0%, transparent 50%),
            radial-gradient(ellipse 800px 500px at 40% 70%, rgba(139, 92, 246, 0.10) 0%, transparent 50%),
            radial-gradient(circle 350px at 15% 80%, rgba(16, 185, 129, 0.06) 0%, transparent 70%),
            radial-gradient(circle 250px at 85% 20%, rgba(245, 158, 11, 0.05) 0%, transparent 70%),
            linear-gradient(135deg, #0F0F1A 0%, #1A1A2E 30%, #16213E 60%, #1A1A2E 100%);
    }
}

/* Hide default streamlit styling */
.stApp > header {
    background-color: transparent;
}

.stApp > .main .block-container {
    padding-top: 0.5rem;
    padding-bottom: 2rem;
    max-width: 1200px;
    position: relative;
}

/* GLOWING CARDS WITH ENHANCED EFFECTS */
.metrics-container {
    display: flex;
    gap: 1.5rem;
    margin-bottom: 3rem;
    flex-wrap: wrap;
}

.metric-card {
    background: linear-gradient(135deg, 
        rgba(26, 26, 46, 0.9) 0%, 
        rgba(22, 22, 41, 0.9) 100%);
    border: 1px solid rgba(91, 108, 255, 0.2);
    border-radius: 16px;
    padding: 1.5rem;
    flex: 1;
    min-width: 250px;
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(12px);
    box-shadow: 
        0 8px 32px rgba(0, 0, 0, 0.4),
        0 2px 8px rgba(91, 108, 255, 0.1),
        inset 0 1px 0 rgba(255, 255, 255, 0.05);
    transition: all 0.3s ease;
}

.metric-card:hover {
    transform: translateY(-2px);
    border-color: rgba(91, 108, 255, 0.4);
    box-shadow: 
        0 12px 48px rgba(0, 0, 0, 0.6),
        0 4px 16px rgba(91, 108, 255, 0.2),
        inset 0 1px 0 rgba(255, 255, 255, 0.1);
}

.metric-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, 
        rgba(91, 108, 255, 0.8), 
        rgba(99, 102, 241, 0.8), 
        rgba(139, 92, 246, 0.8));
    border-radius: 16px 16px 0 0;
}

.metric-card::after {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(91, 108, 255, 0.03) 0%, transparent 70%);
    animation: cardGlow 8s ease-in-out infinite;
    pointer-events: none;
}

@keyframes cardGlow {
    0%, 100% { opacity: 0.3; transform: scale(1); }
    50% { opacity: 0.1; transform: scale(1.1); }
}

.metric-value {
    font-size: 2.5rem;
    font-weight: 700;
    color: #FFFFFF;
    margin-bottom: 0.5rem;
    font-family: 'Inter', sans-serif;
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
    text-shadow: 0 1px 4px rgba(16, 185, 129, 0.3);
}

.metric-change.negative {
    color: #ef4444;
    text-shadow: 0 1px 4px rgba(239, 68, 68, 0.3);
}

/* ENHANCED CHART CONTAINER */
.chart-container {
    background: linear-gradient(135deg, 
        rgba(26, 26, 46, 0.85) 0%, 
        rgba(22, 22, 41, 0.85) 100%);
    border: 1px solid rgba(91, 108, 255, 0.15);
    border-radius: 16px;
    padding: 2rem;
    margin-bottom: 3rem;
    position: relative;
    backdrop-filter: blur(16px);
    box-shadow: 
        0 16px 64px rgba(0, 0, 0, 0.4),
        0 4px 16px rgba(91, 108, 255, 0.08),
        inset 0 1px 0 rgba(255, 255, 255, 0.03);
}

.chart-container::before {
    content: '';
    position: absolute;
    top: -1px;
    left: -1px;
    right: -1px;
    bottom: -1px;
    background: linear-gradient(45deg, 
        rgba(91, 108, 255, 0.2), 
        rgba(99, 102, 241, 0.1), 
        rgba(139, 92, 246, 0.1),
        rgba(91, 108, 255, 0.2));
    border-radius: 16px;
    z-index: -1;
    animation: borderGlow 6s ease-in-out infinite;
}

@keyframes borderGlow {
    0%, 100% { opacity: 0.5; }
    50% { opacity: 0.8; }
}

/* ENHANCED ANALYSIS SECTION */
.analysis-section {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
    margin-bottom: 3rem;
}

.analysis-card {
    background: linear-gradient(135deg, 
        rgba(26, 26, 46, 0.8) 0%, 
        rgba(22, 22, 41, 0.8) 100%);
    border: 1px solid rgba(91, 108, 255, 0.15);
    border-radius: 16px;
    padding: 2rem;
    position: relative;
    backdrop-filter: blur(12px);
    box-shadow: 
        0 8px 32px rgba(0, 0, 0, 0.3),
        0 2px 8px rgba(91, 108, 255, 0.05);
    transition: all 0.3s ease;
}

.analysis-card:hover {
    border-color: rgba(91, 108, 255, 0.25);
    box-shadow: 
        0 12px 48px rgba(0, 0, 0, 0.5),
        0 4px 16px rgba(91, 108, 255, 0.1);
}

/* BETTERSTACK-STYLE SEGMENTED CONTROLS WITH GLOW */
[data-testid="stVerticalBlock"] div[data-baseweb="segmented-control"] {
    background: linear-gradient(135deg, 
        rgba(26, 26, 46, 0.9) 0%, 
        rgba(22, 22, 41, 0.9) 100%) !important;
    border: 1px solid rgba(91, 108, 255, 0.3) !important;
    border-radius: 8px !important;
    backdrop-filter: blur(16px) !important;
    padding: 2px !important;
    box-shadow: 
        0 4px 16px rgba(0, 0, 0, 0.3),
        0 1px 4px rgba(91, 108, 255, 0.1),
        inset 0 1px 0 rgba(255, 255, 255, 0.05) !important;
    display: inline-flex !important;
}

/* Make columns fit their content */
div[data-testid="stColumn"] {
    width: fit-content !important;
    flex: unset !important;
}

div[data-testid="stColumn"] * {
    width: fit-content !important;
}

/* Individual segments with enhanced glow */
[data-testid="stVerticalBlock"] div[data-baseweb="segmented-control"] button {
    background: transparent !important;
    border: none !important;
    border-radius: 6px !important;
    color: #9CA3AF !important;
    font-weight: 500 !important;
    font-size: 13px !important;
    padding: 6px 8px !important;
    margin: 0 1px !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    font-family: 'Inter', sans-serif !important;
    min-height: 28px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    min-width: fit-content !important;
    width: auto !important;
    flex-shrink: 0 !important;
}

/* Active segment with beautiful glow */
[data-testid="stVerticalBlock"] div[data-baseweb="segmented-control"] button[aria-pressed="true"] {
    background: linear-gradient(135deg, 
        rgba(91, 108, 255, 0.25) 0%, 
        rgba(99, 102, 241, 0.15) 100%) !important;
    color: #ffffff !important;
    font-weight: 600 !important;
    box-shadow: 
        0 2px 8px rgba(91, 108, 255, 0.3),
        0 1px 3px rgba(0, 0, 0, 0.2),
        inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
    border: 1px solid rgba(91, 108, 255, 0.4) !important;
    text-shadow: 0 1px 2px rgba(91, 108, 255, 0.5);
}

/* Hover state with subtle glow */
[data-testid="stVerticalBlock"] div[data-baseweb="segmented-control"] button:hover:not([aria-pressed="true"]) {
    background: linear-gradient(135deg, 
        rgba(91, 108, 255, 0.08) 0%, 
        rgba(54, 54, 80, 0.15) 100%) !important;
    color: #e2e8f0 !important;
    box-shadow: 0 1px 4px rgba(91, 108, 255, 0.1);
}

/* Controls styling */
.chart-controls {
    margin: 0;
    padding: 0;
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
    margin: 0;
    font-family: 'Inter', sans-serif;
    text-align: center;
    white-space: nowrap;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
}

.section-title {
    color: #FFFFFF;
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 1.5rem;
    font-family: 'Inter', sans-serif;
    text-shadow: 0 2px 8px rgba(91, 108, 255, 0.3);
}

/* Custom bullet points with glow */
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
    text-shadow: 0 1px 4px rgba(91, 108, 255, 0.5);
}

/* Responsive design */
@media (max-width: 768px) {
    .chart-controls {
        flex-direction: column;
        gap: 1.5rem;
        padding: 1rem;
    }
    
    .control-group {
        width: 100%;
    }
    
    .analysis-section {
        grid-template-columns: 1fr;
    }
    
    .metrics-container {
        flex-direction: column;
    }
    
    .stApp::before {
        animation: none; /* Disable animation on mobile for performance */
    }
}

/* Override Streamlit's default styling */
.stMetric {
    background: none !important;
}

.stMetric > div {
    background: none !important;
}

/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Additional floating particle effect for extra magic */
@keyframes float {
    0%, 100% { transform: translateY(0px) rotate(0deg); }
    33% { transform: translateY(-10px) rotate(120deg); }
    66% { transform: translateY(5px) rotate(240deg); }
}

.floating-particles {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: -1;
}

.floating-particles::before,
.floating-particles::after {
    content: '';
    position: absolute;
    width: 4px;
    height: 4px;
    background: radial-gradient(circle, rgba(91, 108, 255, 0.6) 0%, transparent 70%);
    border-radius: 50%;
    animation: float 8s ease-in-out infinite;
}

.floating-particles::before {
    top: 20%;
    left: 10%;
    animation-delay: -2s;
}

.floating-particles::after {
    top: 80%;
    right: 10%;
    animation-delay: -4s;
}
</style>

<!-- Add floating particles -->
<div class="floating-particles"></div>
""", unsafe_allow_html=True)

# BETTERSTACK-STYLE CHART CONTROLS WITH SEGMENTED CONTROLS
st.markdown('<div class="chart-controls">', unsafe_allow_html=True)

# Create the layout with proper spacing
col1, col2, col3, spacer, col4 = st.columns([0.8, 0.8, 0.8, 4, 1.2])

with col1:
    st.markdown('<div class="control-group"><div class="control-label">Hashrate Scale</div>', unsafe_allow_html=True)
    y_scale = st.segmented_control(
        label="",
        options=["Linear", "Log"],
        default="Log",
        label_visibility="collapsed",
        key="hashrate_y_scale_segment"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="control-group"><div class="control-label">Time Scale</div>', unsafe_allow_html=True)
    x_scale_type = st.segmented_control(
        label="",
        options=["Linear", "Log"],
        default="Linear",
        label_visibility="collapsed",
        key="hashrate_x_scale_segment"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="control-group"><div class="control-label">Power Law</div>', unsafe_allow_html=True)
    show_power_law = st.segmented_control(
        label="",
        options=["Hide", "Show"],
        default="Show",
        label_visibility="collapsed",
        key="hashrate_power_law_segment"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with spacer:
    st.empty()  # Creates the space between left and right groups

with col4:
    st.markdown('<div class="control-group"><div class="control-label">Time Period</div>', unsafe_allow_html=True)
    time_range = st.segmented_control(
        label="",
        options=["1M", "3M", "6M", "1Y", "All"],
        default="All",
        label_visibility="collapsed",
        key="hashrate_time_range_segment"
    )
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

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

# Enhanced chart with power law functionality but keeping your purple theme
fig = go.Figure()

if not filtered_df.empty:
    if x_scale_type == "Log":
        x_values = filtered_df['days_from_genesis']
        x_title = "Days Since Genesis (Log Scale)"
    else:
        x_values = filtered_df['Date']
        x_title = "Date"

    # Add hashrate trace with enhanced glow effects
    fig.add_trace(go.Scatter(
        x=x_values,
        y=filtered_df['Hashrate_PH'],
        mode='lines',
        name='Hashrate (PH/s)',
        line=dict(
            color='#5B6CFF', 
            width=3,
            # Adding glow effect via multiple overlapping lines would be complex in Plotly
            # We'll rely on the CSS backdrop effects instead
        ),
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

        # Support and resistance bands
        fig.add_trace(go.Scatter(
            x=fit_x,
            y=y_fit * 0.4,
            mode='lines',
            name='Support (-60%)',
            line=dict(color='rgba(255, 255, 255, 0.7)', width=1.5, dash='dot'),
            showlegend=True,
            hoverinfo='skip'
        ))
        
        fig.add_trace(go.Scatter(
            x=fit_x,
            y=y_fit * 2.2,
            mode='lines',
            name='Resistance (+120%)',
            line=dict(color='rgba(255, 255, 255, 0.7)', width=1.5, dash='dot'),
            fill='tonexty',
            fillcolor='rgba(100, 100, 100, 0.05)',
            showlegend=True,
            hoverinfo='skip'
        ))

# Enhanced chart layout with beautiful styling - INCREASED HEIGHT
fig.update_layout(
    xaxis_title=x_title if not filtered_df.empty else "Date",
    yaxis_title="Hashrate (PH/s)",
    height=650,  # Increased from 450 to 650
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#9CA3AF', family='Inter'),
    xaxis=dict(
        gridcolor='rgba(91, 108, 255, 0.1)',
        gridwidth=1,
        color='#9CA3AF',
        type="log" if x_scale_type == "Log" else None,
        showgrid=True,
        zeroline=False
    ),
    yaxis=dict(
        gridcolor='rgba(91, 108, 255, 0.1)',
        gridwidth=1,
        color='#9CA3AF',
        type="log" if y_scale == "Log" else "linear",
        showgrid=True,
        zeroline=False
    ),
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="left",
        x=0,
        bgcolor='rgba(0,0,0,0)',
        bordercolor='rgba(0,0,0,0)',
        borderwidth=0,
        font=dict(size=11, color='#9CA3AF')
    ),
    margin=dict(l=50, r=20, t=20, b=50),
    modebar=dict(
        orientation="v",
        bgcolor="rgba(26, 26, 46, 0.8)",
        color="#9CA3AF",
        activecolor="#5B6CFF"
    ),
    hoverlabel=dict(
        bgcolor='rgba(15, 20, 25, 0.95)',
        bordercolor='rgba(91, 108, 255, 0.5)',
        font=dict(color='#e2e8f0', size=11),
        align='left'
    )
)

# Wrap chart in container div for enhanced styling
st.markdown('<div class="chart-container">', unsafe_allow_html=True)

st.plotly_chart(fig, use_container_width=True, config={
    'displayModeBar': True,
    'displaylogo': False,
    'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
    'modeBarButtonsToAdd': ['hoverclosest', 'hovercompare'],
    'toImageButtonOptions': {
        'format': 'png',
        'filename': f'kaspa_hashrate_analysis_{datetime.now().strftime("%Y%m%d_%H%M")}',
        'height': 650,
        'width': 1400,
        'scale': 2
    }
})

st.markdown('</div>', unsafe_allow_html=True)

# Calculate real metrics from data
if not hashrate_df.empty:
    current_hashrate = hashrate_df['Hashrate_PH'].iloc[-1]
    
    # 7-day average
    seven_days_ago = hashrate_df['Date'].iloc[-1] - timedelta(days=7)
    df_7_days = hashrate_df[hashrate_df['Date'] >= seven_days_ago]
    avg_7d = df_7_days['Hashrate_PH'].mean() if len(df_7_days) > 0 else current_hashrate
    
    # 30-day average  
    thirty_days_ago = hashrate_df['Date'].iloc[-1] - timedelta(days=30)
    df_30_days = hashrate_df[hashrate_df['Date'] >= thirty_days_ago]
    avg_30d = df_30_days['Hashrate_PH'].mean() if len(df_30_days) > 0 else current_hashrate
    
    # Calculate percentage changes
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

# Enhanced metrics cards with beautiful glow effects
st.markdown(f"""
<div class="metrics-container">
    <div class="metric-card">
        <div class="metric-label">Current Hashrate</div>
        <div class="metric-value">{current_hashrate:.2f} PH/s</div>
        <div class="metric-change {'positive' if change_7d >= 0 else 'negative'}">+{change_7d:.1f}%</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">7d Average</div>
        <div class="metric-value">{avg_7d:.2f} PH/s</div>
        <div class="metric-change">+0.8%</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">30d Average</div>
        <div class="metric-value">{avg_30d:.2f} PH/s</div>
        <div class="metric-change {'positive' if change_30d >= 0 else 'negative'}">+{change_30d:.1f}%</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Enhanced analysis section with beautiful styling
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
""", unsafe_allow_html=True)

# Mini chart for recent trends using real data
if not hashrate_df.empty:
    recent_30_days = hashrate_df.tail(30)
    recent_dates = recent_30_days['Date']
    recent_data = recent_30_days['Hashrate_PH']
else:
    # Fallback dummy data
    recent_dates = pd.date_range(start='2024-01-01', end='2024-01-30', freq='D')
    recent_data = np.random.normal(1.2, 0.1, len(recent_dates))

mini_fig = go.Figure()
mini_fig.add_trace(go.Scatter(
    x=recent_dates,
    y=recent_data,
    mode='lines+markers',
    name='30-Day Trend',
    line=dict(color='#6366F1', width=3),
    marker=dict(color='#5B6CFF', size=4),
    fill='tonexty',
    fillcolor='rgba(99, 102, 241, 0.15)'
))

mini_fig.update_layout(
    height=250,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#9CA3AF', family='Inter', size=12),
    xaxis=dict(
        gridcolor='rgba(91, 108, 255, 0.1)',
        gridwidth=1,
        color='#9CA3AF',
        showticklabels=True,
        showgrid=True,
        zeroline=False
    ),
    yaxis=dict(
        gridcolor='rgba(91, 108, 255, 0.1)',
        gridwidth=1,
        color='#9CA3AF',
        showgrid=True,
        zeroline=False
    ),
    showlegend=False,
    margin=dict(l=0, r=0, t=20, b=0)
)

st.plotly_chart(mini_fig, use_container_width=True)

st.markdown("""
    </div>
</div>
""", unsafe_allow_html=True)

# At the end of each page:
from footer import add_footer
add_footer()
