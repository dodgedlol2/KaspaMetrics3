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
        st.stop()

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

# Calculate current metrics for later use
if not hashrate_df.empty:
    current_hashrate = hashrate_df['Hashrate_PH'].iloc[-1]
    last_date = hashrate_df['Date'].iloc[-1]
    thirty_days_ago = last_date - timedelta(days=30)
    df_30_days_ago = hashrate_df[hashrate_df['Date'] >= thirty_days_ago]

    if len(df_30_days_ago) > 0:
        hashrate_30_days_ago = df_30_days_ago['Hashrate_PH'].iloc[0]
        hashrate_pct_change = ((current_hashrate - hashrate_30_days_ago) / hashrate_30_days_ago) * 100
    else:
        hashrate_pct_change = 0
else:
    current_hashrate = 0
    hashrate_pct_change = 0

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* Global dark theme */
.stApp {
    background: linear-gradient(135deg, #0F0F1A 0%, #1A1A2E 100%);
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

/* HEADER SECTION WITH CONTROLS */
.header-section {
    margin-bottom: 2rem;
    padding: 1rem 0;
}

.title-container {
    display: flex;
    align-items: center;
    margin-bottom: 1rem;
}

.main-title {
    background: linear-gradient(90deg, #FFFFFF 0%, #A0A0B8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 3.5rem;
    font-weight: 800;
    margin: 0;
    padding: 0;
    font-family: 'Inter', sans-serif;
    letter-spacing: -0.03em;
    line-height: 1.1;
    text-shadow: 0 0 20px rgba(255, 255, 255, 0.15);
    filter: drop-shadow(0 0 8px rgba(255, 255, 255, 0.1));
}

.control-group {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
}

.control-label {
    color: #9CA3AF;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    text-align: center;
    margin-bottom: 0.25rem;
}

/* Enhanced metrics cards */
.metric-card {
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.9) 100%);
    border: 2px solid rgba(100, 116, 139, 0.3);
    border-radius: 16px;
    padding: 1.5rem;
    backdrop-filter: blur(15px);
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
    position: relative;
    overflow: hidden;
}

.metric-card:hover {
    border-color: #00d4ff;
    box-shadow: 0 8px 32px rgba(0, 212, 255, 0.2), 0 0 0 1px rgba(0, 212, 255, 0.3);
    transform: translateY(-2px);
}

.metric-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, #00d4ff, #0ea5e9);
    opacity: 0.7;
}

.metric-label {
    color: #94a3b8;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.5rem;
}

.metric-value {
    color: #f1f5f9;
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 0.25rem;
    line-height: 1.2;
}

.metric-delta {
    font-size: 0.875rem;
    font-weight: 600;
}

.metric-delta.positive {
    color: #10b981;
}

.metric-delta.negative {
    color: #ef4444;
}

/* Chart content section */
.chart-content {
    margin-bottom: 2rem;
}

/* Responsive design */
@media (max-width: 768px) {
    .main-title {
        font-size: 2.5rem;
    }
    
    .metric-card {
        padding: 1rem;
    }
    
    .metric-value {
        font-size: 1.5rem;
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

# Header section with title and controls on the same line
st.markdown('<div class="header-section">', unsafe_allow_html=True)

# Column structure with spacing controls:
# [Left Space] [Title] [Middle Space] [Controls: Hashrate Scale | Time Scale | Time Period | Power Law]
left_space, title_col, middle_space, ctrl_col1, ctrl_col2, ctrl_col3, ctrl_col4 = st.columns([0.1, 1, 5, 1, 1, 1, 1])

# Left invisible spacing column
with left_space:
    st.empty()  # Creates invisible space to the left of title

# Title column
with title_col:
    st.markdown('<div class="title-container"><h1 class="main-title">Kaspa Hashrate</h1></div>', unsafe_allow_html=True)

# Middle invisible spacing column
with middle_space:
    st.empty()  # Creates invisible space between title and controls

# Control columns
with ctrl_col1:
    st.markdown('<div class="control-group"><div class="control-label">Hashrate Scale</div>', unsafe_allow_html=True)
    y_scale = st.selectbox("", ["Linear", "Log"], index=1, label_visibility="collapsed", key="hashrate_y_scale_select")
    st.markdown('</div>', unsafe_allow_html=True)

# JavaScript to style the selectboxes (same as old price page)
st.markdown("""
<script>
setTimeout(function() {
    // Target using exact original selector
    const selectboxes = document.querySelectorAll('.stSelectbox > div > div');
    
    selectboxes.forEach(selectbox => {
        // Apply exact original styling
        if (!selectbox.hasAttribute('data-exact-styled')) {
            selectbox.style.background = 'linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.9) 100%)';
            selectbox.style.border = '2px solid rgba(100, 116, 139, 0.3)';
            selectbox.style.borderRadius = '12px';
            selectbox.style.backdropFilter = 'blur(15px)';
            selectbox.style.transition = 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)';
            selectbox.style.boxShadow = '0 4px 16px rgba(0, 0, 0, 0.2)';
            selectbox.style.minHeight = '26px';
            selectbox.style.width = '150px';
            selectbox.style.maxWidth = '250px';
            selectbox.style.minWidth = '100px';
            selectbox.setAttribute('data-exact-styled', 'true');
            
            // Add exact original hover effects
            selectbox.addEventListener('mouseenter', () => {
                selectbox.style.borderColor = '#00d4ff';
                selectbox.style.boxShadow = '0 8px 32px rgba(0, 212, 255, 0.2), 0 0 0 1px rgba(0, 212, 255, 0.3)';
                selectbox.style.transform = 'translateY(-2px)';
            });
            
            selectbox.addEventListener('mouseleave', () => {
                selectbox.style.borderColor = 'rgba(100, 116, 139, 0.3)';
                selectbox.style.boxShadow = '0 4px 16px rgba(0, 0, 0, 0.2)';
                selectbox.style.transform = 'translateY(0)';
            });
            
            // Style the text content exactly like original
            const textDiv = selectbox.querySelector('div');
            if (textDiv) {
                textDiv.style.color = '#f1f5f9';
                textDiv.style.fontWeight = '600';
                textDiv.style.fontSize = '13px';
                textDiv.style.padding = '8px 16px';
                textDiv.style.background = 'transparent';
            }
        }
    });
    
    // Fix dropdown menus to prevent scrollbars
    const fixDropdownScrollbars = () => {
        const outerPopovers = document.querySelectorAll('div[data-baseweb="popover"]:not(div[data-baseweb="popover"] div[data-baseweb="popover"])');
        outerPopovers.forEach(popover => {
            if (!popover.hasAttribute('data-dropdown-styled')) {
                popover.style.background = 'rgba(15, 20, 25, 0.98)';
                popover.style.backdropFilter = 'blur(25px)';
                popover.style.border = '1px solid rgba(0, 212, 255, 0.3)';
                popover.style.borderRadius = '12px';
                popover.style.boxShadow = '0 12px 40px rgba(0, 0, 0, 0.4)';
                popover.style.marginTop = '4px';
                popover.style.maxHeight = 'none';
                popover.style.height = 'auto';
                popover.style.overflow = 'visible';
                popover.style.overflowY = 'visible';
                popover.setAttribute('data-dropdown-styled', 'true');
                
                const nestedElements = popover.querySelectorAll('div, ul');
                nestedElements.forEach(element => {
                    if (element !== popover) {
                        element.style.background = 'transparent';
                        element.style.border = 'none';
                        element.style.boxShadow = 'none';
                        element.style.backdropFilter = 'none';
                        element.style.borderRadius = '0';
                        element.style.maxHeight = 'none';
                        element.style.overflow = 'visible';
                        element.style.overflowY = 'visible';
                    }
                });
            }
        });
    };
    
    fixDropdownScrollbars();
    
    const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            if (mutation.addedNodes.length > 0) {
                mutation.addedNodes.forEach(node => {
                    if (node.nodeType === 1) {
                        if (node.querySelector && (node.querySelector('[data-baseweb="popover"]') || node.querySelector('[data-baseweb="menu"]'))) {
                            setTimeout(fixDropdownScrollbars, 50);
                        }
                    }
                });
            }
        });
    });
    
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
    
}, 500);
</script>
""", unsafe_allow_html=True)

with ctrl_col2:
    st.markdown('<div class="control-group"><div class="control-label">Time Scale</div>', unsafe_allow_html=True)
    x_scale_type = st.selectbox("", ["Linear", "Log"], index=0, label_visibility="collapsed", key="hashrate_x_scale_select")
    st.markdown('</div>', unsafe_allow_html=True)

with ctrl_col3:
    st.markdown('<div class="control-group"><div class="control-label">Time Period</div>', unsafe_allow_html=True)
    time_range = st.selectbox("", ["1W", "1M", "3M", "6M", "1Y", "All"], index=5, label_visibility="collapsed", key="hashrate_time_range_select")
    st.markdown('</div>', unsafe_allow_html=True)

with ctrl_col4:
    st.markdown('<div class="control-group"><div class="control-label">Power Law</div>', unsafe_allow_html=True)
    show_power_law = st.selectbox("", ["Hide", "Show"], index=1, label_visibility="collapsed", key="hashrate_power_law_select")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Chart content section
st.markdown('<div class="chart-content"></div>', unsafe_allow_html=True)

# Data filtering based on time range
if not hashrate_df.empty:
    last_date = hashrate_df['Date'].iloc[-1]
    if time_range == "1W":
        start_date = last_date - timedelta(days=7)
    elif time_range == "1M":
        start_date = last_date - timedelta(days=30)
    elif time_range == "3M":
        start_date = last_date - timedelta(days=90)
    elif time_range == "6M":
        start_date = last_date - timedelta(days=180)
    elif time_range == "1Y":
        start_date = last_date - timedelta(days=365)
    else:
        start_date = hashrate_df['Date'].iloc[0]

    filtered_df = hashrate_df[hashrate_df['Date'] >= start_date]
else:
    filtered_df = hashrate_df

# Create the enhanced chart
fig = go.Figure()

if not filtered_df.empty:
    if x_scale_type == "Log":
        x_values = filtered_df['days_from_genesis']
        x_title = "Days Since Genesis (Log Scale)"
    else:
        x_values = filtered_df['Date']
        x_title = "Date"

    # Custom Y-axis tick formatting function
    def format_hashrate(value):
        """Format hashrate values for clean display"""
        if value >= 1000:
            return f"{value/1000:.1f}E"
        elif value >= 100:
            return f"{value:.0f}P"
        elif value >= 10:
            return f"{value:.1f}P"
        else:
            return f"{value:.2f}P"

    # Generate custom tick values for log scale Y-axis
    def generate_log_ticks(data_min, data_max):
        """Generate physics-style log tick marks with 1, 2, 5 pattern"""
        import math
        log_min = math.floor(math.log10(data_min))
        log_max = math.ceil(math.log10(data_max))
        
        major_ticks = []
        intermediate_ticks = []
        minor_ticks = []
        
        for i in range(log_min, log_max + 1):
            base = 10**i
            
            if data_min <= base <= data_max:
                major_ticks.append(base)
            
            for factor in [2, 5]:
                intermediate_val = factor * base
                if data_min <= intermediate_val <= data_max:
                    intermediate_ticks.append(intermediate_val)
            
            for j in [3, 4, 6, 7, 8, 9]:
                minor_val = j * base
                if data_min <= minor_val <= data_max:
                    minor_ticks.append(minor_val)
        
        return major_ticks, intermediate_ticks, minor_ticks

    # Add hashrate trace
    fig.add_trace(go.Scatter(
        x=x_values,
        y=filtered_df['Hashrate_PH'],
        mode='lines',
        name='Kaspa Hashrate (PH/s)',
        line=dict(color='#00d4ff', width=3, shape='spline', smoothing=0.3),
        hovertemplate='<b>%{fullData.name}</b><br>Date: %{text}<br>Hashrate: %{y:.2f} PH/s<br><extra></extra>',
        text=[d.strftime('%Y-%m-%d') for d in filtered_df['Date']],
        showlegend=True,
        fillcolor='rgba(0, 212, 255, 0.1)'
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
            name=f'Power Law Fit (R²={r2_hashrate:.3f})',
            line=dict(color='#ff8c00', width=3, dash='solid'),
            showlegend=True,
            hovertemplate='<b>Power Law Fit</b><br>R² = %{customdata:.3f}<br>Value: %{y:.2f} PH/s<br><extra></extra>',
            customdata=[r2_hashrate] * len(fit_x)
        ))

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

    # Enhanced chart layout with custom tick formatting
    if not filtered_df.empty:
        y_min, y_max = filtered_df['Hashrate_PH'].min(), filtered_df['Hashrate_PH'].max()

        # Generate custom ticks for Y-axis if log scale
        if y_scale == "Log":
            y_major_ticks, y_intermediate_ticks, y_minor_ticks = generate_log_ticks(y_min, y_max)
            y_tick_vals = sorted(y_major_ticks + y_intermediate_ticks)
            y_tick_text = [format_hashrate(val) for val in y_tick_vals]
        else:
            y_tick_vals = None
            y_tick_text = None
            y_minor_ticks = []

        # Generate custom ticks for X-axis if log scale
        if x_scale_type == "Log":
            x_min, x_max = filtered_df['days_from_genesis'].min(), filtered_df['days_from_genesis'].max()
            x_major_ticks, x_intermediate_ticks, x_minor_ticks = generate_log_ticks(x_min, x_max)
            x_tick_vals = sorted(x_major_ticks + x_intermediate_ticks)
            x_tick_text = [f"{int(val)}" for val in x_tick_vals]
        else:
            x_tick_vals = None
            x_tick_text = None
            x_minor_ticks = []
    else:
        y_tick_vals = None
        y_tick_text = None
        y_minor_ticks = []
        x_tick_vals = None
        x_tick_text = None
        x_minor_ticks = []

fig.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Inter', color='#e2e8f0'),
    hovermode='x unified',
    height=600,
    margin=dict(l=30, r=30, t=40, b=10),
    xaxis=dict(
        title=dict(text=x_title if not filtered_df.empty else "Date", font=dict(size=13, color='#cbd5e1', weight=600), standoff=35),
        type="log" if x_scale_type == "Log" else None,
        showgrid=True,
        gridwidth=1.2,
        gridcolor='rgba(255, 255, 255, 0.12)' if x_scale_type == "Log" else 'rgba(255, 255, 255, 0.08)',
        linecolor='rgba(255, 255, 255, 0.15)',
        tickfont=dict(size=11, color='#94a3b8'),
        tickmode='array' if x_scale_type == "Log" else 'auto',
        tickvals=x_tick_vals,
        ticktext=x_tick_text,
        minor=dict(
            showgrid=True,
            gridwidth=0.5,
            gridcolor='rgba(255, 255, 255, 0.04)',
            tickmode='array',
            tickvals=x_minor_ticks if x_scale_type == "Log" else []
        ) if x_scale_type == "Log" else dict()
    ),
    yaxis=dict(
        title=None,
        type="log" if y_scale == "Log" else "linear",
        showgrid=True,
        gridwidth=1.2,
        gridcolor='rgba(255, 255, 255, 0.12)' if y_scale == "Log" else 'rgba(255, 255, 255, 0.08)',
        linecolor='rgba(255, 255, 255, 0.15)',
        tickfont=dict(size=11, color='#94a3b8'),
        tickmode='array' if y_scale == "Log" else 'auto',
        tickvals=y_tick_vals,
        ticktext=y_tick_text,
        minor=dict(
            showgrid=True,
            gridwidth=0.5,
            gridcolor='rgba(255, 255, 255, 0.04)',
            tickmode='array',
            tickvals=y_minor_ticks if y_scale == "Log" else []
        ) if y_scale == "Log" else dict()
    ),
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
    hoverlabel=dict(
        bgcolor='rgba(15, 20, 25, 0.95)',
        bordercolor='rgba(0, 212, 255, 0.5)',
        font=dict(color='#e2e8f0', size=11),
        align='left'
    )
)

# Display chart
with st.container():
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

# Calculate comprehensive metrics
if not hashrate_df.empty and len(df_30_days_ago) > 0:
    hashrate_30_days_ago_data = hashrate_df[hashrate_df['Date'] <= thirty_days_ago]
    if len(hashrate_30_days_ago_data) > 10:
        try:
            a_hashrate_30d, b_hashrate_30d, r2_hashrate_30d = fit_power_law(hashrate_30_days_ago_data, y_col='Hashrate_PH')
        except:
            b_hashrate_30d = b_hashrate
            r2_hashrate_30d = r2_hashrate
    else:
        b_hashrate_30d = b_hashrate
        r2_hashrate_30d = r2_hashrate
    
    slope_pct_change = ((b_hashrate - b_hashrate_30d) / abs(b_hashrate_30d)) * 100 if b_hashrate_30d != 0 else 0
    r2_pct_change = ((r2_hashrate - r2_hashrate_30d) / r2_hashrate_30d) * 100 if r2_hashrate_30d != 0 else 0
else:
    slope_pct_change = 0
    r2_pct_change = 0

# Calculate 7-day average
if not hashrate_df.empty:
    seven_days_ago = last_date - timedelta(days=7)
    df_7_days = hashrate_df[hashrate_df['Date'] >= seven_days_ago]
    avg_7d = df_7_days['Hashrate_PH'].mean() if len(df_7_days) > 0 else current_hashrate
    
    # Calculate weekly change
    if len(df_7_days) > 1:
        hashrate_7_days_ago = df_7_days['Hashrate_PH'].iloc[0]
        weekly_pct_change = ((current_hashrate - hashrate_7_days_ago) / hashrate_7_days_ago) * 100
    else:
        weekly_pct_change = 0
else:
    avg_7d = 0
    weekly_pct_change = 0

# Enhanced Metrics Section with improved styling and hover effects
col1, col2, col3, col4 = st.columns(4)

with col1:
    metric_html = f"""
    <div class="metric-card">
        <div class="metric-label">POWER-LAW SLOPE</div>
        <div class="metric-value">{b_hashrate:.4f}</div>
        <div class="metric-delta {'positive' if slope_pct_change >= 0 else 'negative'}">{slope_pct_change:+.2f}%</div>
    </div>
    """
    st.markdown(metric_html, unsafe_allow_html=True)

with col2:
    metric_html = f"""
    <div class="metric-card">
        <div class="metric-label">MODEL ACCURACY (R²)</div>
        <div class="metric-value">{r2_hashrate:.4f}</div>
        <div class="metric-delta {'positive' if r2_pct_change >= 0 else 'negative'}">{r2_pct_change:+.2f}%</div>
    </div>
    """
    st.markdown(metric_html, unsafe_allow_html=True)

with col3:
    metric_html = f"""
    <div class="metric-card">
        <div class="metric-label">CURRENT HASHRATE</div>
        <div class="metric-value">{current_hashrate:.2f} PH/s</div>
        <div class="metric-delta {'positive' if hashrate_pct_change >= 0 else 'negative'}">{hashrate_pct_change:+.2f}%</div>
    </div>
    """
    st.markdown(metric_html, unsafe_allow_html=True)

with col4:
    metric_html = f"""
    <div class="metric-card">
        <div class="metric-label">7-DAY AVERAGE</div>
        <div class="metric-value">{avg_7d:.2f} PH/s</div>
        <div class="metric-delta {'positive' if weekly_pct_change >= 0 else 'negative'}">{weekly_pct_change:+.2f}%</div>
    </div>
    """
    st.markdown(metric_html, unsafe_allow_html=True)

# Footer
footer_html = """
<div style="text-align: center; padding: 40px 40px; margin-top: 32px; 
     background: rgba(15, 20, 25, 0.3); backdrop-filter: blur(20px);
     border-top: 1px solid rgba(255, 255, 255, 0.08);">
    <div style="max-width: 1200px; margin: 0 auto;">
        <p style="color: #64748b; font-size: 13px; margin-bottom: 16px;">
            Professional-grade cryptocurrency mining analysis • Real-time hashrate monitoring • Advanced predictive modeling
        </p>
        <div style="color: #475569; font-size: 10px; text-transform: uppercase; letter-spacing: 1px;">
            Last Updated: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC') + """ • 
            Built for institutional-grade analysis
        </div>
    </div>
</div>
"""

st.markdown(footer_html, unsafe_allow_html=True)

# At the end of each page:
from footer import add_footer
add_footer()
