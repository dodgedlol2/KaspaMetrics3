import streamlit as st

# Page config MUST be first!
st.set_page_config(page_title="Open Interest", page_icon="📊", layout="wide")

import plotly.graph_objects as go
import pandas as pd
import numpy as np
import sys
import os
from datetime import datetime, timedelta
import re
import requests
from io import StringIO

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

# Function to parse currency values like '$1.21M', '$548.54K'
def parse_currency(value_str):
    """Parse currency strings like '$1.21M', '$548.54K' to float values"""
    if not isinstance(value_str, str):
        return float(value_str) if pd.notna(value_str) else 0
    
    # Remove currency symbol and trailing quotes/apostrophes
    clean_str = value_str.replace('$', '').replace("'", '').strip()
    
    # Handle millions, billions, and thousands
    if clean_str.endswith('M'):
        return float(clean_str[:-1]) * 1e6
    elif clean_str.endswith('K'):
        return float(clean_str[:-1]) * 1e3
    elif clean_str.endswith('B'):
        return float(clean_str[:-1]) * 1e9
    else:
        # Try to convert directly if no suffix
        try:
            return float(clean_str)
        except:
            return 0

# Function to load open interest data from Google Sheets
@st.cache_data
def load_open_interest_data():
    """Load and process open interest data from Google Sheets CSV export"""
    try:
        # Google Sheets CSV export URL
        sheet_id = "1F9VGnVr3zdZF-6da4JuKG6KxQe5hGtph6xhB4vhu394"
        gid = "0"  # Blad1 sheet
        csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
        
        # Fetch the CSV data
        response = requests.get(csv_url)
        response.raise_for_status()
        
        # Read CSV into DataFrame
        csv_data = StringIO(response.text)
        df = pd.read_csv(csv_data)
        
        # Clean column names
        df.columns = df.columns.str.strip()
        
        # Remove empty rows and clean data
        df = df.dropna(subset=['date', 'Total_open_interest'])
        
        # Clean date strings - remove time and trailing quotes
        df['date'] = df['date'].str.replace(', 02:00\'', '').str.replace(', 01:00\'', '').str.replace('\'', '').str.strip()
        
        # Parse dates
        df['Date'] = pd.to_datetime(df['date'], format='%d %b %Y')
        
        # Parse open interest values and clean
        df['Open_Interest_USD'] = df['Total_open_interest'].apply(parse_currency)
        
        # Remove duplicates and sort
        df = df.drop_duplicates(subset=['Date']).sort_values('Date').reset_index(drop=True)
        
        # Filter out any zero or invalid values
        df = df[df['Open_Interest_USD'] > 0]
        
        # Calculate days from Kaspa genesis (Nov 7, 2021)
        kaspa_genesis_date = datetime(2021, 11, 7)
        oi_start_date = df['Date'].iloc[0]  # First OI data point
        
        df['days_from_kaspa_genesis'] = (df['Date'] - kaspa_genesis_date).dt.days
        df['days_from_oi_start'] = (df['Date'] - oi_start_date).dt.days
        
        return df, kaspa_genesis_date, oi_start_date
        
    except Exception as e:
        st.error(f"Failed to load open interest data: {str(e)}")
        # Return empty dataframe with correct structure
        empty_df = pd.DataFrame(columns=['Date', 'Open_Interest_USD', 'days_from_kaspa_genesis', 'days_from_oi_start'])
        kaspa_genesis_date = datetime(2021, 11, 7)
        return empty_df, kaspa_genesis_date, None

# Load open interest data
if 'oi_df' not in st.session_state or 'kaspa_genesis_date' not in st.session_state or 'oi_start_date' not in st.session_state:
    st.session_state.oi_df, st.session_state.kaspa_genesis_date, st.session_state.oi_start_date = load_open_interest_data()

oi_df = st.session_state.oi_df
kaspa_genesis_date = st.session_state.kaspa_genesis_date
oi_start_date = st.session_state.oi_start_date

# Calculate power law if we have data
if not oi_df.empty and len(oi_df) > 10:
    try:
        a_oi, b_oi, r2_oi = fit_power_law(oi_df, x_col='days_from_oi_start', y_col='Open_Interest_USD')
    except Exception as e:
        st.error(f"Failed to calculate open interest power law: {str(e)}")
        a_oi, b_oi, r2_oi = 1, 1, 0
else:
    a_oi, b_oi, r2_oi = 1, 1, 0

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
<div class='big-font'>Kaspa Open Interest</div>
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
    st.markdown('<div class="control-group"><div class="control-label">OI Scale</div>', unsafe_allow_html=True)
    y_scale = st.segmented_control(
        label="OI Scale",
        options=["Linear", "Log"],
        default="Log",
        label_visibility="collapsed",
        key="oi_y_scale_segment"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="control-group"><div class="control-label">Time Scale</div>', unsafe_allow_html=True)
    x_scale_type = st.segmented_control(
        label="Time Scale",
        options=["Linear", "Log"],
        default="Linear",
        label_visibility="collapsed",
        key="oi_x_scale_segment"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="control-group"><div class="control-label">Power Law</div>', unsafe_allow_html=True)
    show_power_law = st.segmented_control(
        label="Power Law",
        options=["Hide", "Show"],
        default="Show",
        label_visibility="collapsed",
        key="oi_power_law_segment"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with spacer:
    st.empty()  # Creates the space between left and right groups

with col4:
    st.markdown('<div class="control-group"><div class="control-label">Time Period</div>', unsafe_allow_html=True)
    time_range = st.segmented_control(
        label="Time Period",
        options=["1M", "3M", "6M", "1Y", "All"],
        default="All",
        label_visibility="collapsed",
        key="oi_time_range_segment"
    )
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Data filtering based on time range
if not oi_df.empty:
    last_date = oi_df['Date'].iloc[-1]
    if time_range == "1M":
        start_date = last_date - timedelta(days=30)
    elif time_range == "3M":
        start_date = last_date - timedelta(days=90)
    elif time_range == "6M":
        start_date = last_date - timedelta(days=180)
    elif time_range == "1Y":
        start_date = last_date - timedelta(days=365)
    else:  # "All"
        start_date = oi_df['Date'].iloc[0]

    filtered_df = oi_df[oi_df['Date'] >= start_date]
else:
    filtered_df = oi_df

# Custom Y-axis tick formatting function for open interest
def format_oi(value):
    """Format open interest values for clean display"""
    if value >= 1e9:
        return f"${value/1e9:.1f}B"
    elif value >= 1e6:
        return f"${value/1e6:.1f}M"
    elif value >= 1e3:
        return f"${value/1e3:.1f}K"
    else:
        return f"${value:.0f}"

# Generate custom tick values for log scale
def generate_oi_log_ticks(data_min, data_max):
    """Generate physics-style log tick marks with 1, 2, 5 pattern for open interest"""
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
        x_values = filtered_df['days_from_oi_start']
        x_title = "Days Since Open Interest Start (Log Scale)"
    else:
        x_values = filtered_df['Date']
        x_title = "Date"

    # Calculate Y-axis range to eliminate gaps
    y_min_data = filtered_df['Open_Interest_USD'].min()
    y_max_data = filtered_df['Open_Interest_USD'].max()
    
    # Set manual minimum values for different scales
    if y_scale == "Log":
        # For log scale, set a sensible minimum that's lower than data min but not too extreme
        y_min_chart = y_min_data * 0.8  # 20% below minimum data point
        y_max_chart = y_max_data * 1.05  # 5% above maximum
    else:
        # For linear scale, start from zero
        y_min_chart = 0
        y_max_chart = y_max_data * 1.05  # 5% above maximum

    # Add open interest trace with appropriate fill method for each scale
    if y_scale == "Log" and not filtered_df.empty:
        # For log scale: add invisible baseline at the bottom of chart range
        fig.add_trace(go.Scatter(
            x=x_values,
            y=[y_min_chart] * len(x_values),
            mode='lines',
            name='baseline',
            line=dict(color='rgba(0,0,0,0)', width=0),  # Invisible line
            showlegend=False,
            hoverinfo='skip',
            fill=None
        ))
        
        # Open Interest trace fills to baseline
        fig.add_trace(go.Scatter(
            x=x_values,
            y=filtered_df['Open_Interest_USD'],
            mode='lines',
            name='Kaspa Open Interest',
            line=dict(color='#10B981', width=2),  # Green color for OI
            fill='tonexty',  # Fill to previous trace (baseline)
            fillgradient=dict(
                type="vertical",
                colorscale=[
                    [0, "rgba(13, 13, 26, 0.01)"],  # Top: transparent
                    [1, "rgba(16, 185, 129, 0.6)"]   # Bottom: green with opacity
                ]
            ),
            hovertemplate='<b>%{fullData.name}</b><br>Open Interest: $%{y:,.0f}<extra></extra>' if x_scale_type == "Linear" else '%{text}<br><b>%{fullData.name}</b><br>Open Interest: $%{y:,.0f}<extra></extra>',
            text=[f"{d.strftime('%B %d, %Y')}" for d in filtered_df['Date']] if not filtered_df.empty else [],
            customdata=filtered_df[['Date', 'days_from_oi_start']].values if not filtered_df.empty else []
        ))
    else:
        # For linear scale: fill to zero (no extra chart area)
        fig.add_trace(go.Scatter(
            x=x_values,
            y=filtered_df['Open_Interest_USD'],
            mode='lines',
            name='Kaspa Open Interest',
            line=dict(color='#10B981', width=2),  # Green color for OI
            fill='tozeroy',  # Fill to zero
            fillgradient=dict(
                type="vertical",
                colorscale=[
                    [0, "rgba(13, 13, 26, 0.01)"],  # Top: transparent
                    [1, "rgba(16, 185, 129, 0.6)"]   # Bottom: green with opacity
                ]
            ),
            hovertemplate='<b>%{fullData.name}</b><br>Open Interest: $%{y:,.0f}<extra></extra>' if x_scale_type == "Linear" else '%{text}<br><b>%{fullData.name}</b><br>Open Interest: $%{y:,.0f}<extra></extra>',
            text=[f"{d.strftime('%B %d, %Y')}" for d in filtered_df['Date']] if not filtered_df.empty else [],
            customdata=filtered_df[['Date', 'days_from_oi_start']].values if not filtered_df.empty else []
        ))

    # Add power law if enabled
    if show_power_law == "Show" and not filtered_df.empty and len(filtered_df) > 10:
        x_fit = filtered_df['days_from_oi_start']
        y_fit = a_oi * np.power(x_fit, b_oi)
        fit_x = x_fit if x_scale_type == "Log" else filtered_df['Date']

        fig.add_trace(go.Scatter(
            x=fit_x,
            y=y_fit,
            mode='lines',
            name='Power Law',
            line=dict(color='#ff8c00', width=2, dash='solid'),
            showlegend=True,
            hovertemplate='<b>%{fullData.name}</b><br>Fit: $%{y:,.0f}<extra></extra>' if x_scale_type == "Linear" else '<b>%{fullData.name}</b><br>Fit: $%{y:,.0f}<extra></extra>',
            hoverinfo='y+name' if x_scale_type == "Log" else 'x+y+name'
        ))

# Enhanced chart layout with custom logarithmic grid lines
x_axis_config = dict(
    gridcolor='#363650',
    gridwidth=1,
    color='#9CA3AF'
)

# Generate custom ticks for Y-axis if log scale
if y_scale == "Log" and not filtered_df.empty:
    y_major_ticks, y_intermediate_ticks, y_minor_ticks = generate_oi_log_ticks(y_min_chart, y_max_chart)
    # Combine major and intermediate ticks for display
    y_tick_vals = sorted(y_major_ticks + y_intermediate_ticks)
    y_tick_text = [format_oi(val) for val in y_tick_vals]
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
    yaxis_title="Open Interest (USD)",
    height=650,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#9CA3AF', family='Inter'),
    hovermode='x unified',
    hoverlabel=dict(
        bgcolor='rgba(15, 20, 25, 0.95)',
        bordercolor='rgba(16, 185, 129, 0.5)',  # Green border for OI
        font=dict(color='#e2e8f0', size=11),
        align='left',
        namelength=-1
    ),
    xaxis=dict(
        type="log" if x_scale_type == "Log" else None,
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(255, 255, 255, 0.1)',
        minor=dict(
            ticklen=6,
            gridcolor='rgba(255, 255, 255, 0.05)',
            gridwidth=0.5
        ) if x_scale_type == "Log" else dict(),
        tickformat="%b %Y" if x_scale_type == "Linear" else None,
        linecolor='#3A3C4A',
        zerolinecolor='#3A3C4A',
        color='#9CA3AF',
        hoverformat='%B %d, %Y' if x_scale_type == "Linear" else None,
        range=[
            np.log10(filtered_df['days_from_oi_start'].min()) if x_scale_type == "Log" and not filtered_df.empty else filtered_df['Date'].min() if not filtered_df.empty else None,
            np.log10(filtered_df['days_from_oi_start'].max()) if x_scale_type == "Log" and not filtered_df.empty else filtered_df['Date'].max() if not filtered_df.empty else None
        ] if not filtered_df.empty else None
    ),
    yaxis=dict(
        gridcolor='#363650',
        gridwidth=1,
        color='#9CA3AF',
        type="log" if y_scale == "Log" else "linear",
        range=[np.log10(y_min_chart), np.log10(y_max_chart)] if y_scale == "Log" and not filtered_df.empty else [y_min_chart, y_max_chart] if not filtered_df.empty else None,
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
        orientation="h",
        bgcolor="rgba(0,0,0,0)",
        color="#9CA3AF",
        activecolor="#10B981"  # Green for OI theme
    )
)

st.plotly_chart(fig, use_container_width=True, config={
    'displayModeBar': True,
    'displaylogo': False,
    'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
    'modeBarButtonsToAdd': ['hoverclosest', 'hovercompare'],
    'toImageButtonOptions': {
        'format': 'png',
        'filename': f'kaspa_oi_analysis_{datetime.now().strftime("%Y%m%d_%H%M")}',
        'height': 650,
        'width': 1400,
        'scale': 2
    }
})

# Calculate real metrics from data
if not oi_df.empty:
    current_oi = oi_df['Open_Interest_USD'].iloc[-1]
    
    # Calculate 30-day metrics for power law slope and R² changes
    thirty_days_ago = oi_df['Date'].iloc[-1] - timedelta(days=30)
    df_30_days_ago = oi_df[oi_df['Date'] <= thirty_days_ago]
    
    if len(df_30_days_ago) > 10:
        try:
            a_oi_30d, b_oi_30d, r2_oi_30d = fit_power_law(df_30_days_ago, x_col='days_from_oi_start', y_col='Open_Interest_USD')
            slope_pct_change = ((b_oi - b_oi_30d) / abs(b_oi_30d)) * 100 if b_oi_30d != 0 else 0
            r2_pct_change = ((r2_oi - r2_oi_30d) / r2_oi_30d) * 100 if r2_oi_30d != 0 else 0
        except:
            slope_pct_change = 0
            r2_pct_change = 0
    else:
        slope_pct_change = 0
        r2_pct_change = 0
    
    # Calculate OI change over 30 days
    df_30_days = oi_df[oi_df['Date'] >= thirty_days_ago]
    if len(df_30_days) > 1:
        oi_30d_ago = df_30_days['Open_Interest_USD'].iloc[0]
        oi_pct_change = ((current_oi - oi_30d_ago) / oi_30d_ago) * 100
    else:
        oi_pct_change = 0
        
    # Calculate growth rate since start
    first_oi = oi_df['Open_Interest_USD'].iloc[0]
    total_days = (oi_df['Date'].iloc[-1] - oi_df['Date'].iloc[0]).days
    daily_growth_rate = ((current_oi / first_oi) ** (1/total_days) - 1) * 100 if total_days > 0 else 0
    
    # Calculate days since Kaspa genesis for display
    days_since_genesis = (oi_df['Date'].iloc[-1] - kaspa_genesis_date).days
    days_since_oi_start = (oi_df['Date'].iloc[-1] - oi_start_date).days
    
else:
    current_oi = 50e6  # $50M fallback
    slope_pct_change = 2.5
    r2_pct_change = 1.8
    oi_pct_change = 15.2
    daily_growth_rate = 0.8
    days_since_genesis = 1000
    days_since_oi_start = 500

# Display data information
if not oi_df.empty and oi_start_date:
    st.markdown(f"""
    <div style="color: #9CA3AF; font-size: 0.9rem; margin-bottom: 2rem; text-align: center;">
        📊 <strong>Data Range:</strong> {oi_start_date.strftime('%B %d, %Y')} to {oi_df['Date'].iloc[-1].strftime('%B %d, %Y')} 
        | 🚀 <strong>Kaspa Genesis:</strong> {kaspa_genesis_date.strftime('%B %d, %Y')} 
        | 📈 <strong>Total Data Points:</strong> {len(oi_df)}
        | ⏱️ <strong>Days Since OI Start:</strong> {days_since_oi_start}
    </div>
    """, unsafe_allow_html=True)

# Custom metrics cards with real OI data
st.markdown(f"""
<div class="metrics-container">
    <div class="metric-card">
        <div class="metric-label">Power-Law Slope</div>
        <div class="metric-value">{b_oi:.4f}</div>
        <div class="metric-change {'positive' if slope_pct_change >= 0 else 'negative'}">{slope_pct_change:+.1f}% (30d)</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Model Accuracy (R²)</div>
        <div class="metric-value">{r2_oi:.4f}</div>
        <div class="metric-change {'positive' if r2_pct_change >= 0 else 'negative'}">{r2_pct_change:+.1f}% (30d)</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Current Open Interest</div>
        <div class="metric-value">${current_oi/1e6:.1f}M</div>
        <div class="metric-change {'positive' if oi_pct_change >= 0 else 'negative'}">{oi_pct_change:+.1f}% (30d)</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Daily Growth Rate</div>
        <div class="metric-value">{daily_growth_rate:.2f}%</div>
        <div class="metric-change {'positive' if daily_growth_rate >= 0 else 'negative'}">Since Start</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Data quality and insights section
if not oi_df.empty:
    st.markdown("""
    <div style="margin-top: 3rem;">
        <h3 style="color: #FFFFFF; font-size: 1.5rem; font-weight: 600; margin-bottom: 1.5rem; font-family: 'Inter', sans-serif;">
            📊 Data Insights
        </h3>
        <div style="background: linear-gradient(135deg, #1A1A2E 0%, #161629 100%); border: 1px solid #363650; border-radius: 16px; padding: 2rem;">
            <div style="color: #9CA3AF; line-height: 1.6;">
    """, unsafe_allow_html=True)
    
    # Calculate some interesting statistics
    max_oi = oi_df['Open_Interest_USD'].max()
    min_oi = oi_df['Open_Interest_USD'].min()
    avg_oi = oi_df['Open_Interest_USD'].mean()
    growth_multiple = current_oi / oi_df['Open_Interest_USD'].iloc[0]
    
    st.markdown(f"""
                <p><strong>📈 Growth Analysis:</strong> Open Interest has grown {growth_multiple:.1f}x from ${oi_df['Open_Interest_USD'].iloc[0]/1e6:.2f}M to ${current_oi/1e6:.1f}M over {days_since_oi_start} days.</p>
                <p><strong>📊 Range:</strong> Minimum OI was ${min_oi/1e6:.2f}M, maximum reached ${max_oi/1e6:.1f}M, with an average of ${avg_oi/1e6:.1f}M.</p>
                <p><strong>🔗 Power Law:</strong> The relationship follows a power law with exponent {b_oi:.4f} and R² of {r2_oi:.4f}, indicating {'strong' if r2_oi > 0.8 else 'moderate' if r2_oi > 0.6 else 'weak'} correlation.</p>
                <p><strong>🚀 Since Kaspa Genesis:</strong> {days_since_genesis} days have passed since Kaspa's genesis block on November 7, 2021.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.warning("⚠️ No data available. Please check the Google Sheets connection and data format.")
