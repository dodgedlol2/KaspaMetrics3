import streamlit as st

# Page config MUST be first!
st.set_page_config(page_title="Spot Price", page_icon="💰", layout="wide")

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

# Load price data
if 'price_df' not in st.session_state or 'price_genesis_date' not in st.session_state:
    try:
        st.session_state.price_df, st.session_state.price_genesis_date = kaspa_data.load_price_data()
    except Exception as e:
        st.error(f"Failed to load price data: {str(e)}")
        # Create fallback dummy data
        dates = pd.date_range(start='2024-01-01', end='2024-06-01', freq='D')
        price_values = np.random.uniform(0.10, 0.25, len(dates))
        st.session_state.price_df = pd.DataFrame({
            'Date': dates,
            'Price': price_values,
            'days_from_genesis': range(len(dates))
        })
        st.session_state.price_genesis_date = pd.to_datetime('2021-11-07')

price_df = st.session_state.price_df
genesis_date = st.session_state.price_genesis_date

# Calculate power law if we have data
if not price_df.empty:
    try:
        a_price, b_price, r2_price = fit_power_law(price_df, y_col='Price')
    except Exception as e:
        st.error(f"Failed to calculate price power law: {str(e)}")
        a_price, b_price, r2_price = 1, 1, 0
else:
    a_price, b_price, r2_price = 1, 1, 0

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
<div class='big-font'>Kaspa Spot Price</div>
""", unsafe_allow_html=True)

# Custom CSS for BetterStack-inspired dark theme with segmented controls
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* Global dark theme with subtle textured background */
.stApp {
    background: 
        linear-gradient(135deg, #0F0F1A 0%, #0D0D1A 100%),
        radial-gradient(circle at 20% 20%, rgba(91, 108, 255, 0.03) 0%, transparent 50%),
        radial-gradient(circle at 80% 80%, rgba(99, 102, 241, 0.02) 0%, transparent 50%);
    color: #FFFFFF;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
}

/* Hide default streamlit styling */
.stApp > header {
    background-color: transparent;
}

.stApp > .main .block-container {
    padding-top: 0.5rem;
    padding-bottom: 2rem;
    max-width: 1200px;
}

/* BETTERSTACK-STYLE SEGMENTED CONTROLS */
/* Target all segmented controls */
[data-testid="stVerticalBlock"] div[data-baseweb="segmented-control"] {
    background: rgba(26, 26, 46, 0.6) !important;
    border: 1px solid rgba(54, 54, 80, 0.4) !important;
    border-radius: 8px !important;
    backdrop-filter: blur(12px) !important;
    padding: 2px !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
    display: inline-flex !important;
}

/* PROVEN SOLUTION: Make columns fit their content */
div[data-testid="stColumn"] {
    width: fit-content !important;
    flex: unset !important;
}

div[data-testid="stColumn"] * {
    width: fit-content !important;
}

/* Individual segments - inactive state */
[data-testid="stVerticalBlock"] div[data-baseweb="segmented-control"] button {
    background: transparent !important;
    border: none !important;
    border-radius: 6px !important;
    color: #9CA3AF !important;
    font-weight: 500 !important;
    font-size: 13px !important;
    padding: 6px 8px !important;
    margin: 0 1px !important;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    font-family: 'Inter', sans-serif !important;
    min-height: 28px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    min-width: fit-content !important;
    width: auto !important;
    flex-shrink: 0 !important;
}

/* Active segment - BetterStack style */
[data-testid="stVerticalBlock"] div[data-baseweb="segmented-control"] button[aria-pressed="true"] {
    background: rgba(91, 108, 255, 0.15) !important;
    color: #ffffff !important;
    font-weight: 600 !important;
    box-shadow: 
        0 1px 3px rgba(0, 0, 0, 0.1),
        inset 0 1px 0 rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(91, 108, 255, 0.3) !important;
}

/* Hover state for inactive segments */
[data-testid="stVerticalBlock"] div[data-baseweb="segmented-control"] button:hover:not([aria-pressed="true"]) {
    background: rgba(54, 54, 80, 0.3) !important;
    color: #e2e8f0 !important;
}

/* Controls container */
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
}

/* Enhanced metrics cards with gritty texture and animations */
.metrics-container {
    display: flex;
    gap: 1.5rem;
    margin-bottom: 3rem;
    flex-wrap: wrap;
}

.metric-card {
    background: 
        /* Main gradient */
        linear-gradient(135deg, #1A1A2E 0%, #161629 50%, #0F0F1A 100%),
        /* Gritty noise texture */
        radial-gradient(circle at 30% 30%, rgba(91, 108, 255, 0.08) 0%, transparent 50%),
        radial-gradient(circle at 70% 70%, rgba(147, 51, 234, 0.06) 0%, transparent 50%),
        /* Fine grain */
        repeating-linear-gradient(
            45deg,
            rgba(255, 255, 255, 0.015) 0px,
            rgba(255, 255, 255, 0.015) 1px,
            transparent 1px,
            transparent 12px
        ),
        repeating-linear-gradient(
            -45deg,
            rgba(91, 108, 255, 0.02) 0px,
            rgba(91, 108, 255, 0.02) 1px,
            transparent 1px,
            transparent 16px
        );
    border: 1px solid #363650;
    border-radius: 16px;
    padding: 1.5rem;
    flex: 1;
    min-width: 250px;
    position: relative;
    overflow: hidden;
    cursor: pointer;
    transition: all 0.6s cubic-bezier(0.23, 1, 0.32, 1);
    transform: translateY(0);
    box-shadow: 
        0 4px 16px rgba(0, 0, 0, 0.3),
        inset 0 1px 0 rgba(255, 255, 255, 0.05);
}

/* Hover animations */
.metric-card:hover {
    transform: translateY(-6px) scale(1.015);
    border-color: rgba(91, 108, 255, 0.4);
    box-shadow: 
        0 12px 32px rgba(0, 0, 0, 0.4),
        0 4px 16px rgba(91, 108, 255, 0.2),
        inset 0 1px 0 rgba(255, 255, 255, 0.1);
    background: 
        /* Enhanced hover gradient */
        linear-gradient(135deg, #1F1F3A 0%, #1A1A35 50%, #12121F 100%),
        /* Brighter glow on hover */
        radial-gradient(circle at 30% 30%, rgba(91, 108, 255, 0.12) 0%, transparent 50%),
        radial-gradient(circle at 70% 70%, rgba(147, 51, 234, 0.1) 0%, transparent 50%),
        /* Same grain patterns */
        repeating-linear-gradient(
            45deg,
            rgba(255, 255, 255, 0.02) 0px,
            rgba(255, 255, 255, 0.02) 1px,
            transparent 1px,
            transparent 12px
        ),
        repeating-linear-gradient(
            -45deg,
            rgba(91, 108, 255, 0.03) 0px,
            rgba(91, 108, 255, 0.03) 1px,
            transparent 1px,
            transparent 16px
        );
}

/* Enhanced top gradient border */
.metric-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, #5B6CFF 0%, #6366F1 50%, #8B5CF6 100%);
    transition: all 0.5s ease;
}

.metric-card:hover::before {
    height: 4px;
    background: linear-gradient(90deg, #5B6CFF 0%, #6366F1 30%, #8B5CF6 60%, #A855F7 100%);
    box-shadow: 0 0 12px rgba(91, 108, 255, 0.6);
}

/* Animated shimmer effect */
.metric-card::after {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(
        90deg,
        transparent,
        rgba(255, 255, 255, 0.03),
        transparent
    );
    transition: left 0.8s ease;
    pointer-events: none;
}

.metric-card:hover::after {
    left: 100%;
}

.metric-value {
    font-size: 2.5rem;
    font-weight: 700;
    color: #FFFFFF;
    margin-bottom: 0.5rem;
    font-family: 'Inter', sans-serif;
    position: relative;
    z-index: 2;
    transition: all 0.4s ease;
    text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.metric-card:hover .metric-value {
    color: #F8FAFC;
    text-shadow: 
        0 2px 8px rgba(0, 0, 0, 0.4),
        0 0 20px rgba(91, 108, 255, 0.3);
}

.metric-label {
    color: #9CA3AF;
    font-size: 0.9rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.5rem;
    position: relative;
    z-index: 2;
    transition: all 0.3s ease;
}

.metric-card:hover .metric-label {
    color: #CBD5E1;
}

.metric-change {
    color: #10B981;
    font-size: 0.9rem;
    font-weight: 600;
    position: relative;
    z-index: 2;
    transition: all 0.3s ease;
    text-shadow: 0 1px 4px rgba(0, 0, 0, 0.3);
}

.metric-card:hover .metric-change {
    color: #34D399;
    text-shadow: 
        0 1px 4px rgba(0, 0, 0, 0.4),
        0 0 12px rgba(16, 185, 129, 0.3);
}

.metric-change.negative {
    color: #ef4444;
}

.metric-card:hover .metric-change.negative {
    color: #F87171;
    text-shadow: 
        0 1px 4px rgba(0, 0, 0, 0.4),
        0 0 12px rgba(239, 68, 68, 0.3);
}

/* Chart container */
.chart-container {
    background: linear-gradient(135deg, #1A1A2E 0%, #161629 100%);
    border: 1px solid #363650;
    border-radius: 16px;
    padding: 2rem;
    margin-bottom: 3rem;
}

/* Analysis section */
.analysis-section {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
    margin-bottom: 3rem;
}

.analysis-card {
    background: linear-gradient(135deg, #1A1A2E 0%, #161629 100%);
    border: 1px solid #363650;
    border-radius: 16px;
    padding: 2rem;
}

.section-title {
    color: #FFFFFF;
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 1.5rem;
    font-family: 'Inter', sans-serif;
}

/* Custom bullet points */
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
</style>
""", unsafe_allow_html=True)

# BETTERSTACK-STYLE CHART CONTROLS WITH SEGMENTED CONTROLS
st.markdown('<div class="chart-controls">', unsafe_allow_html=True)

# Create the layout with proper spacing
col1, col2, col3, spacer, col4 = st.columns([0.8, 0.8, 0.8, 4, 1.2])

with col1:
    st.markdown('<div class="control-group"><div class="control-label">Price Scale</div>', unsafe_allow_html=True)
    y_scale = st.segmented_control(
        label="",
        options=["Linear", "Log"],
        default="Log",
        label_visibility="collapsed",
        key="price_y_scale_segment"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="control-group"><div class="control-label">Time Scale</div>', unsafe_allow_html=True)
    x_scale_type = st.segmented_control(
        label="",
        options=["Linear", "Log"],
        default="Linear",
        label_visibility="collapsed",
        key="price_x_scale_segment"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="control-group"><div class="control-label">Power Law</div>', unsafe_allow_html=True)
    show_power_law = st.segmented_control(
        label="",
        options=["Hide", "Show"],
        default="Show",
        label_visibility="collapsed",
        key="price_power_law_segment"
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
        key="price_time_range_segment"
    )
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Data filtering based on time range
if not price_df.empty:
    last_date = price_df['Date'].iloc[-1]
    if time_range == "1M":
        start_date = last_date - timedelta(days=30)
    elif time_range == "3M":
        start_date = last_date - timedelta(days=90)
    elif time_range == "6M":
        start_date = last_date - timedelta(days=180)
    elif time_range == "1Y":
        start_date = last_date - timedelta(days=365)
    else:  # "All"
        start_date = price_df['Date'].iloc[0]

    filtered_df = price_df[price_df['Date'] >= start_date]
else:
    filtered_df = price_df

# Custom Y-axis tick formatting function for currency
def format_currency(value):
    """Format currency values for clean display"""
    if value >= 1:
        if value >= 1000:
            return f"${value/1000:.1f}k"
        elif value >= 100:
            return f"${value:.0f}"
        elif value >= 10:
            return f"${value:.1f}"
        else:
            return f"${value:.2f}"
    elif value >= 0.01:
        return f"${value:.3f}"
    elif value >= 0.001:
        return f"${value:.4f}"
    elif value >= 0.0001:
        return f"${value:.5f}"
    else:
        return f"${value:.1e}"

# Generate custom tick values for log scale
def generate_log_ticks(data_min, data_max):
    """Generate physics-style log tick marks with 1, 2, 5 pattern"""
    import math
    log_min = math.floor(math.log10(data_min))
    log_max = math.ceil(math.log10(data_max))
    
    major_ticks = []
    intermediate_ticks = []  # For 2 and 5
    minor_ticks = []
    
    for i in range(log_min, log_max + 1):
        base = 10**i
        
        # Major tick at 1 * 10^i
        if data_min <= base <= data_max:
            major_ticks.append(base)
        
        # Intermediate ticks at 2 and 5 * 10^i
        for factor in [2, 5]:
            intermediate_val = factor * base
            if data_min <= intermediate_val <= data_max:
                intermediate_ticks.append(intermediate_val)
        
        # Minor ticks at 3, 4, 6, 7, 8, 9 * 10^i
        for j in [3, 4, 6, 7, 8, 9]:
            minor_val = j * base
            if data_min <= minor_val <= data_max:
                minor_ticks.append(minor_val)
    
    return major_ticks, intermediate_ticks, minor_ticks

# Enhanced chart with power law functionality and custom log grid lines
fig = go.Figure()

if not filtered_df.empty:
    if x_scale_type == "Log":
        x_values = filtered_df['days_from_genesis']
        x_title = "Days Since Genesis (Log Scale)"
    else:
        x_values = filtered_df['Date']
        x_title = "Date"

    # Add price trace with purple color scheme (same as hashrate)
    fig.add_trace(go.Scatter(
        x=x_values,
        y=filtered_df['Price'],
        mode='lines',
        name='Kaspa Price (USD)',
        line=dict(color='#5B6CFF', width=3),
        fill='tonexty',
        fillcolor='rgba(91, 108, 255, 0.1)',
        hovertemplate='<b>Kaspa Price</b><br>Date: %{text}<br>Price: $%{y:.6f}<br><extra></extra>',
        text=[d.strftime('%Y-%m-%d') for d in filtered_df['Date']] if not filtered_df.empty else []
    ))

    # Add power law if enabled
    if show_power_law == "Show" and not filtered_df.empty:
        x_fit = filtered_df['days_from_genesis']
        y_fit = a_price * np.power(x_fit, b_price)
        fit_x = x_fit if x_scale_type == "Log" else filtered_df['Date']

        # Calculate standard deviation of residuals for proper confidence bands
        residuals = np.log(filtered_df['Price']) - np.log(y_fit)
        std_dev = np.std(residuals)
        
        # Standard deviation bands in log space
        y_fit_upper = y_fit * np.exp(std_dev)   # +1 std dev
        y_fit_lower = y_fit * np.exp(-std_dev)  # -1 std dev

        fig.add_trace(go.Scatter(
            x=fit_x,
            y=y_fit,
            mode='lines',
            name=f'Power Law (R²={r2_price:.3f})',
            line=dict(color='#ff8c00', width=3, dash='solid'),
            showlegend=True,
            hovertemplate='<b>Power Law Fit</b><br>R² = %{customdata:.3f}<br>Value: $%{y:.6f}<br><extra></extra>',
            customdata=[r2_price] * len(fit_x)
        ))

        fig.add_trace(go.Scatter(
            x=fit_x,
            y=y_fit_lower,
            mode='lines',
            name='-1σ Support',
            line=dict(color='rgba(255, 255, 255, 0.7)', width=1.5, dash='dot'),
            showlegend=True,
            hoverinfo='skip'
        ))
        
        fig.add_trace(go.Scatter(
            x=fit_x,
            y=y_fit_upper,
            mode='lines',
            name='+1σ Resistance',
            line=dict(color='rgba(255, 255, 255, 0.7)', width=1.5, dash='dot'),
            fill='tonexty',
            fillcolor='rgba(100, 100, 100, 0.05)',
            showlegend=True,
            hoverinfo='skip'
        ))

# Enhanced chart layout with custom logarithmic grid lines
x_axis_config = dict(
    gridcolor='#363650',
    gridwidth=1,
    color='#9CA3AF'
)

# Generate custom ticks for Y-axis if log scale
if y_scale == "Log" and not filtered_df.empty:
    y_min, y_max = filtered_df['Price'].min(), filtered_df['Price'].max()
    y_major_ticks, y_intermediate_ticks, y_minor_ticks = generate_log_ticks(y_min, y_max)
    # Combine major and intermediate ticks for display
    y_tick_vals = sorted(y_major_ticks + y_intermediate_ticks)
    y_tick_text = [format_currency(val) for val in y_tick_vals]
else:
    y_tick_vals = None
    y_tick_text = None
    y_minor_ticks = []

# Custom logarithmic grid lines when X-axis (Time Scale) is in log scale
if x_scale_type == "Log" and not filtered_df.empty:
    x_axis_config.update({
        'type': 'log',
        'showgrid': True,
        'gridwidth': 1,
        'gridcolor': 'rgba(255, 255, 255, 0.1)',
        'minor': dict(
            ticklen=6,
            gridcolor='rgba(255, 255, 255, 0.05)',
            gridwidth=0.5
        )
    })
            
elif x_scale_type == "Log":
    x_axis_config['type'] = 'log'

fig.update_layout(
    xaxis_title=x_title if not filtered_df.empty else "Date",
    yaxis_title="Price (USD)",
    height=650,  # Increased from 450 to 650
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#9CA3AF', family='Inter'),
    xaxis=dict(
        type="log" if x_scale_type == "Log" else None,
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(255, 255, 255, 0.1)',
        minor=dict(
            ticklen=6,
            gridcolor='rgba(255, 255, 255, 0.05)',
            gridwidth=0.5
        ),
        tickformat="%b %Y" if x_scale_type == "Linear" else None,
        linecolor='#3A3C4A',
        zerolinecolor='#3A3C4A',
        color='#9CA3AF'
    ),
    yaxis=dict(
        gridcolor='#363650',
        gridwidth=1,
        color='#9CA3AF',
        type="log" if y_scale == "Log" else "linear",
        # Custom currency formatting for Y-axis
        tickmode='array' if y_scale == "Log" and y_tick_vals else 'auto',
        tickvals=y_tick_vals,
        ticktext=y_tick_text,
        minor=dict(
            showgrid=True,
            gridwidth=0.5,
            gridcolor='rgba(54, 54, 80, 0.3)',
            tickmode='array',
            tickvals=y_minor_ticks if y_scale == "Log" else []
        ) if y_scale == "Log" else dict()
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
        font=dict(size=11)
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

st.plotly_chart(fig, use_container_width=True, config={
    'displayModeBar': True,
    'displaylogo': False,
    'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
    'modeBarButtonsToAdd': ['hoverclosest', 'hovercompare'],
    'toImageButtonOptions': {
        'format': 'png',
        'filename': f'kaspa_price_analysis_{datetime.now().strftime("%Y%m%d_%H%M")}',
        'height': 650,
        'width': 1400,
        'scale': 2
    }
})

# Calculate real metrics from data
if not price_df.empty:
    current_price = price_df['Price'].iloc[-1]
    
    # Calculate 30-day metrics for power law slope and R² changes
    thirty_days_ago = price_df['Date'].iloc[-1] - timedelta(days=30)
    df_30_days_ago = price_df[price_df['Date'] <= thirty_days_ago]
    
    if len(df_30_days_ago) > 10:
        try:
            a_price_30d, b_price_30d, r2_price_30d = fit_power_law(df_30_days_ago, y_col='Price')
            slope_pct_change = ((b_price - b_price_30d) / abs(b_price_30d)) * 100 if b_price_30d != 0 else 0
            r2_pct_change = ((r2_price - r2_price_30d) / r2_price_30d) * 100 if r2_price_30d != 0 else 0
        except:
            slope_pct_change = 0
            r2_pct_change = 0
    else:
        slope_pct_change = 0
        r2_pct_change = 0
    
    # Calculate price change over 30 days
    df_30_days = price_df[price_df['Date'] >= thirty_days_ago]
    if len(df_30_days) > 1:
        price_30d_ago = df_30_days['Price'].iloc[0]
        price_pct_change = ((current_price - price_30d_ago) / price_30d_ago) * 100
    else:
        price_pct_change = 0
        
    # Calculate market cap estimate (24B total supply)
    market_cap_estimate = current_price * 24e9
    
else:
    current_price = 0.15
    slope_pct_change = 2.1
    r2_pct_change = 1.5
    price_pct_change = 8.3
    market_cap_estimate = 3.6e9

# Custom metrics cards with real data - using the price-specific metrics
st.markdown(f"""
<div class="metrics-container">
    <div class="metric-card">
        <div class="metric-label">Power-Law Slope</div>
        <div class="metric-value">{b_price:.4f}</div>
        <div class="metric-change {'positive' if slope_pct_change >= 0 else 'negative'}">{slope_pct_change:+.1f}%</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Model Accuracy (R²)</div>
        <div class="metric-value">{r2_price:.4f}</div>
        <div class="metric-change {'positive' if r2_pct_change >= 0 else 'negative'}">{r2_pct_change:+.1f}%</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Current Price</div>
        <div class="metric-value">${current_price:.6f}</div>
        <div class="metric-change {'positive' if price_pct_change >= 0 else 'negative'}">{price_pct_change:+.1f}%</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Est. Market Cap</div>
        <div class="metric-value">${market_cap_estimate/1e9:.2f}B</div>
        <div class="metric-change {'positive' if price_pct_change >= 0 else 'negative'}">{price_pct_change:+.1f}%</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Analysis section with real insights
price_trend = "bullish" if price_pct_change > 5 else "bearish" if price_pct_change < -5 else "sideways"
slope_trend = "increasing" if slope_pct_change > 0 else "decreasing"

st.markdown(f"""
<div class="analysis-section">
    <div class="analysis-card">
        <h3 class="section-title">Key Insights</h3>
        <ul class="insights-list">
            <li>Price trend is {price_trend} with {abs(price_pct_change):.1f}% change over 30 days</li>
            <li>Power law slope is {slope_trend}, indicating {'accelerating' if slope_pct_change > 0 else 'decelerating'} growth</li>
            <li>Model accuracy (R²) of {r2_price:.3f} shows {'strong' if r2_price > 0.8 else 'moderate' if r2_price > 0.6 else 'weak'} correlation</li>
            <li>Current market cap estimate: ${market_cap_estimate/1e9:.2f}B USD</li>
        </ul>
    </div>
    <div class="analysis-card">
        <h3 class="section-title">30-Day Price Trend</h3>
""", unsafe_allow_html=True)

# Mini chart for recent price trends using real data
if not price_df.empty:
    recent_30_days = price_df.tail(30)
    recent_dates = recent_30_days['Date']
    recent_data = recent_30_days['Price']
else:
    # Fallback dummy data
    recent_dates = pd.date_range(start='2024-01-01', end='2024-01-30', freq='D')
    recent_data = np.random.uniform(0.10, 0.25, len(recent_dates))

mini_fig = go.Figure()
mini_fig.add_trace(go.Scatter(
    x=recent_dates,
    y=recent_data,
    mode='lines+markers',
    name='30-Day Trend',
    line=dict(color='#5B6CFF', width=3),
    marker=dict(color='#5B6CFF', size=4),
    fill='tonexty',
    fillcolor='rgba(91, 108, 255, 0.1)'
))

mini_fig.update_layout(
    height=250,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#9CA3AF', family='Inter', size=12),
    xaxis=dict(
        gridcolor='#363650',
        gridwidth=1,
        color='#9CA3AF',
        showticklabels=True
    ),
    yaxis=dict(
        gridcolor='#363650',
        gridwidth=1,
        color='#9CA3AF',
        tickformat='$.6f'  # Format as currency with 6 decimal places
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
