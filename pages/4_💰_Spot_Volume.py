import streamlit as st

# Page config MUST be first!
st.set_page_config(page_title="Enhanced Spot Price", page_icon="💰", layout="wide")

import plotly.graph_objects as go
import pandas as pd
import numpy as np
import sys
import os
from datetime import datetime, timedelta
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

# Cache function to load Google Sheets data
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_google_sheets_data():
    """Load early price data from Google Sheets"""
    try:
        # Google Sheets CSV export URL
        sheets_url = "https://docs.google.com/spreadsheets/d/1zwQ_Ew2G_reqTYhCCIT276ph5aG-rxNT4BRLL88c38w/export?format=csv&gid=275707638"
        
        # Download the CSV data
        response = requests.get(sheets_url, timeout=10)
        response.raise_for_status()
        
        # Parse CSV data
        csv_data = StringIO(response.text)
        df = pd.read_csv(csv_data)
        
        # Clean and process the data
        df['date'] = pd.to_datetime(df['date'])
        df['estimatedprice'] = pd.to_numeric(df['estimatedprice'], errors='coerce')
        
        # Remove any invalid rows
        df = df.dropna(subset=['date', 'estimatedprice'])
        
        # Sort by date
        df = df.sort_values('date').reset_index(drop=True)
        
        st.success(f"✅ Loaded {len(df)} early price data points from Google Sheets")
        return df
        
    except Exception as e:
        st.error(f"⚠️ Failed to load Google Sheets data: {str(e)}")
        # Return empty dataframe as fallback
        return pd.DataFrame(columns=['date', 'estimatedprice', 'amountofselloffers', 'amountofbuyoffers', 'confidencelvl'])

# Cache function to combine datasets
@st.cache_data(ttl=3600)
def combine_price_datasets():
    """Combine early estimated data with exchange data"""
    try:
        # Load exchange data (your existing data)
        exchange_df, genesis_date = kaspa_data.load_price_data()
        
        # Load early estimated data
        early_df = load_google_sheets_data()
        
        if early_df.empty:
            # If no early data, return original data
            return exchange_df, genesis_date, pd.DataFrame()
        
        # Ensure all datetime objects are timezone-naive for consistency
        if early_df['date'].dt.tz is not None:
            early_df['date'] = early_df['date'].dt.tz_localize(None)
        if exchange_df['Date'].dt.tz is not None:
            exchange_df['Date'] = exchange_df['Date'].dt.tz_localize(None)
        if hasattr(genesis_date, 'tz') and genesis_date.tz is not None:
            genesis_date = genesis_date.tz_localize(None)
        
        # Calculate days from genesis for early data
        early_df['days_from_genesis'] = (early_df['date'] - genesis_date).dt.days
        
        # Find the overlap point - where exchange data starts
        exchange_start_date = exchange_df['Date'].min()
        
        # Filter early data to only include dates before exchange data starts
        early_filtered = early_df[early_df['date'] < exchange_start_date].copy()
        
        # Prepare early data to match exchange data format
        early_formatted = pd.DataFrame({
            'Date': early_filtered['date'],
            'Price': early_filtered['estimatedprice'],
            'days_from_genesis': early_filtered['days_from_genesis'],
            'data_source': 'estimated',
            'confidence': early_filtered['confidencelvl'] if 'confidencelvl' in early_filtered.columns else 'unknown'
        })
        
        # Add data source column to exchange data
        exchange_formatted = exchange_df.copy()
        exchange_formatted['data_source'] = 'exchange'
        exchange_formatted['confidence'] = 'high'
        
        # Combine the datasets
        combined_df = pd.concat([early_formatted, exchange_formatted], ignore_index=True)
        combined_df = combined_df.sort_values('Date').reset_index(drop=True)
        
        # Recalculate days from genesis for the combined dataset
        combined_df['days_from_genesis'] = (combined_df['Date'] - genesis_date).dt.days
        
        st.success(f"✅ Combined dataset: {len(early_formatted)} early + {len(exchange_formatted)} exchange = {len(combined_df)} total points")
        
        return combined_df, genesis_date, early_formatted
        
    except Exception as e:
        st.error(f"Failed to combine datasets: {str(e)}")
        # Fallback to original data
        original_df, genesis_date = kaspa_data.load_price_data()
        return original_df, genesis_date, pd.DataFrame()

# Load combined price data
if 'combined_price_df' not in st.session_state or 'early_data_df' not in st.session_state:
    st.session_state.combined_price_df, st.session_state.price_genesis_date, st.session_state.early_data_df = combine_price_datasets()

combined_price_df = st.session_state.combined_price_df
early_data_df = st.session_state.early_data_df
genesis_date = st.session_state.price_genesis_date

# Calculate power law if we have data
if not combined_price_df.empty:
    try:
        a_price, b_price, r2_price = fit_power_law(combined_price_df, y_col='Price')
    except Exception as e:
        st.error(f"Failed to calculate price power law: {str(e)}")
        a_price, b_price, r2_price = 1, 1, 0
else:
    a_price, b_price, r2_price = 1, 1, 0

# ====================== ATH CALCULATION AND LOGIC ======================
def calculate_ath_data(price_df):
    """Calculate All-Time High data"""
    if price_df.empty:
        return None, None, None
    
    ath_idx = price_df['Price'].idxmax()
    ath_price = price_df.loc[ath_idx, 'Price']
    ath_date = price_df.loc[ath_idx, 'Date']
    ath_days = price_df.loc[ath_idx, 'days_from_genesis']
    
    return ath_price, ath_date, ath_days

def add_ath_to_chart(fig, filtered_df, ath_price, ath_date, ath_days, x_scale_type):
    """Add ATH point as scatter trace to the chart"""
    if ath_price is None:
        return fig
    
    if x_scale_type == "Log":
        # Find the ATH point within the filtered dataframe
        ath_in_filtered = filtered_df[filtered_df['days_from_genesis'] == ath_days]
        
        # Add ATH point as scatter trace
        if not ath_in_filtered.empty:
            fig.add_trace(go.Scatter(
                x=[ath_days],
                y=[ath_price],
                mode='markers+text',
                name='ATH',
                marker=dict(
                    color='rgba(255, 255, 255, 0.9)',
                    size=8,
                    line=dict(color='rgba(91, 108, 255, 0.8)', width=2)
                ),
                text=[f'ATH ${ath_price:.4f}'],
                textposition='top center',
                textfont=dict(
                    size=11,
                    color='white',
                    family='Inter'
                ),
                showlegend=True,
                hovertemplate='<b>All-Time High</b><br>Price: $%{y:.4f}<extra></extra>'
            ))
    else:
        # For linear time scale, use dates
        ath_in_filtered = filtered_df[filtered_df['Date'] == ath_date]
        
        # Add ATH point as scatter trace
        if not ath_in_filtered.empty:
            fig.add_trace(go.Scatter(
                x=[ath_date],
                y=[ath_price],
                mode='markers+text',
                name='ATH',
                marker=dict(
                    color='rgba(255, 255, 255, 0.9)',
                    size=8,
                    line=dict(color='rgba(91, 108, 255, 0.8)', width=2)
                ),
                text=[f'ATH ${ath_price:.4f}'],
                textposition='top center',
                textfont=dict(
                    size=11,
                    color='white',
                    family='Inter'
                ),
                showlegend=True,
                hovertemplate='<b>All-Time High</b><br>Price: $%{y:.4f}<extra></extra>'
            ))
    
    return fig

# ====================== 1YL CALCULATION AND LOGIC ======================
def calculate_1yl_data(price_df):
    """Calculate One Year Low data"""
    if price_df.empty:
        return None, None, None
    
    # One year low (last 365 days)
    one_year_ago = price_df['Date'].iloc[-1] - timedelta(days=365)
    recent_year_df = price_df[price_df['Date'] >= one_year_ago]
    
    if not recent_year_df.empty:
        oyl_idx = recent_year_df['Price'].idxmin()
        oyl_price = recent_year_df.loc[oyl_idx, 'Price']
        oyl_date = recent_year_df.loc[oyl_idx, 'Date']
        oyl_days = recent_year_df.loc[oyl_idx, 'days_from_genesis']
    else:
        # Fallback to global minimum
        oyl_idx = price_df['Price'].idxmin()
        oyl_price = price_df.loc[oyl_idx, 'Price']
        oyl_date = price_df.loc[oyl_idx, 'Date']
        oyl_days = price_df.loc[oyl_idx, 'days_from_genesis']
    
    return oyl_price, oyl_date, oyl_days

def add_1yl_to_chart(fig, filtered_df, oyl_price, oyl_date, oyl_days, x_scale_type):
    """Add 1YL point as scatter trace to the chart"""
    if oyl_price is None:
        return fig
    
    if x_scale_type == "Log":
        # Find the 1YL point within the filtered dataframe
        oyl_in_filtered = filtered_df[filtered_df['days_from_genesis'] == oyl_days]
        
        # Add 1YL point as scatter trace
        if not oyl_in_filtered.empty:
            fig.add_trace(go.Scatter(
                x=[oyl_days],
                y=[oyl_price],
                mode='markers+text',
                name='1YL',
                marker=dict(
                    color='rgba(255, 255, 255, 0.9)',
                    size=8,
                    line=dict(color='rgba(239, 68, 68, 0.8)', width=2)
                ),
                text=[f'1YL ${oyl_price:.4f}'],
                textposition='bottom center',
                textfont=dict(
                    size=11,
                    color='white',
                    family='Inter'
                ),
                showlegend=True,
                hovertemplate='<b>One Year Low</b><br>Price: $%{y:.4f}<extra></extra>'
            ))
    else:
        # For linear time scale, use dates
        oyl_in_filtered = filtered_df[filtered_df['Date'] == oyl_date]
        
        # Add 1YL point as scatter trace
        if not oyl_in_filtered.empty:
            fig.add_trace(go.Scatter(
                x=[oyl_date],
                y=[oyl_price],
                mode='markers+text',
                name='1YL',
                marker=dict(
                    color='rgba(255, 255, 255, 0.9)',
                    size=8,
                    line=dict(color='rgba(239, 68, 68, 0.8)', width=2)
                ),
                text=[f'1YL ${oyl_price:.4f}'],
                textposition='bottom center',
                textfont=dict(
                    size=11,
                    color='white',
                    family='Inter'
                ),
                showlegend=True,
                hovertemplate='<b>One Year Low</b><br>Price: $%{y:.4f}<extra></extra>'
            ))
    
    return fig

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

.subtitle-enhanced {
    font-size: 18px;
    color: #9CA3AF;
    margin-bottom: 2rem;
    background: linear-gradient(90deg, #ff8c00 0%, #5B6CFF 50%, #8B5CF6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 600;
}
</style>
<div class='big-font'>Enhanced Kaspa Price History</div>
<div class='subtitle-enhanced'>🔗 Combined Discord Estimates + Exchange Data | Complete Historical View</div>
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
    min-width: 200px;
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
    font-size: 0.85rem;
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

/* Data quality indicators */
.data-quality-high {
    color: #10B981;
}

.data-quality-medium {
    color: #F59E0B;
}

.data-quality-low {
    color: #EF4444;
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

# Override Streamlit's default styling */
.stMetric {
    background: none !important;
}

.stMetric > div {
    background: none !important;
}

/* Custom modebar positioning - lower by 10px and left by 10px */
.js-plotly-plot .plotly .modebar {
    top: 10px !important;
    right: 10px !important;
}

/* Make hover line thinner and more subtle */
.js-plotly-plot .plotly .hoverline {
    stroke-width: 1px !important;
    opacity: 0.6 !important;
}

.js-plotly-plot .plotly .spikeline {
    stroke-width: 1px !important;
    opacity: 0.6 !important;
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
col1, col2, col3, col4, spacer, col5 = st.columns([0.8, 0.8, 0.8, 1.0, 3, 1.2])

with col1:
    st.markdown('<div class="control-group"><div class="control-label">Price Scale</div>', unsafe_allow_html=True)
    y_scale = st.segmented_control(
        label="Price Scale",
        options=["Linear", "Log"],
        default="Log",
        label_visibility="collapsed",
        key="enhanced_price_y_scale_segment"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="control-group"><div class="control-label">Time Scale</div>', unsafe_allow_html=True)
    x_scale_type = st.segmented_control(
        label="Time Scale",
        options=["Linear", "Log"],
        default="Linear",
        label_visibility="collapsed",
        key="enhanced_price_x_scale_segment"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="control-group"><div class="control-label">Power Law</div>', unsafe_allow_html=True)
    show_power_law = st.segmented_control(
        label="Power Law",
        options=["Hide", "Show"],
        default="Show",
        label_visibility="collapsed",
        key="enhanced_price_power_law_segment"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="control-group"><div class="control-label">Data Sources</div>', unsafe_allow_html=True)
    show_data_sources = st.segmented_control(
        label="Data Sources",
        options=["Combined", "Separate"],
        default="Separate",
        label_visibility="collapsed",
        key="enhanced_data_sources_segment"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with spacer:
    st.empty()  # Creates the space between left and right groups

with col5:
    st.markdown('<div class="control-group"><div class="control-label">Time Period</div>', unsafe_allow_html=True)
    time_range = st.segmented_control(
        label="Time Period",
        options=["1M", "3M", "6M", "1Y", "All"],
        default="All",
        label_visibility="collapsed",
        key="enhanced_price_time_range_segment"
    )
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Data filtering based on time range
if not combined_price_df.empty:
    last_date = combined_price_df['Date'].iloc[-1]
    if time_range == "1M":
        start_date = last_date - timedelta(days=30)
    elif time_range == "3M":
        start_date = last_date - timedelta(days=90)
    elif time_range == "6M":
        start_date = last_date - timedelta(days=180)
    elif time_range == "1Y":
        start_date = last_date - timedelta(days=365)
    else:  # "All"
        start_date = combined_price_df['Date'].iloc[0]

    filtered_df = combined_price_df[combined_price_df['Date'] >= start_date]
else:
    filtered_df = combined_price_df

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

# Calculate ATH and 1YL data using separated functions
ath_price, ath_date, ath_days = calculate_ath_data(combined_price_df)
oyl_price, oyl_date, oyl_days = calculate_1yl_data(combined_price_df)

# Enhanced chart with power law functionality and data source separation
fig = go.Figure()

if not filtered_df.empty:
    if x_scale_type == "Log":
        x_values = filtered_df['days_from_genesis']
        x_title = "Days Since Genesis (Log Scale)"
        # For annotations
        ath_x = ath_days
        oyl_x = oyl_days
    else:
        x_values = filtered_df['Date']
        x_title = "Date"
        # For annotations
        ath_x = ath_date
        oyl_x = oyl_date

    # Calculate Y-axis range to eliminate gaps and accommodate ATH/1YL labels
    y_min_data = filtered_df['Price'].min()
    y_max_data = filtered_df['Price'].max()
    
    # Check if ATH/1YL points are in the current view to add extra padding for text
    ath_in_view = ath_price is not None and ath_days >= filtered_df['days_from_genesis'].min() and ath_days <= filtered_df['days_from_genesis'].max() if x_scale_type == "Log" else ath_price is not None and ath_date >= filtered_df['Date'].min() and ath_date <= filtered_df['Date'].max()
    oyl_in_view = oyl_price is not None and oyl_days >= filtered_df['days_from_genesis'].min() and oyl_days <= filtered_df['days_from_genesis'].max() if x_scale_type == "Log" else oyl_price is not None and oyl_date >= filtered_df['Date'].min() and oyl_date <= filtered_df['Date'].max()
    
    # Set manual minimum values for different scales
    if y_scale == "Log":
        # For log scale, set a sensible minimum that's lower than data min but not too extreme
        y_min_chart = y_min_data * 0.8  # 20% below minimum data point
        # Add extra padding at top if ATH is visible (for text label)
        y_max_chart = y_max_data * (1.50 if ath_in_view else 1.05)  # Extra padding for ATH text
    else:
        # For linear scale, start from zero or slightly below data minimum
        y_min_chart = 0
        # Add extra padding at top if ATH is visible (for text label) 
        y_max_chart = y_max_data * (1.15 if ath_in_view else 1.05)  # Extra padding for ATH text

    # Separate data sources or combine based on user choice
    if show_data_sources == "Separate" and 'data_source' in filtered_df.columns:
        # Show estimated and exchange data separately
        estimated_data = filtered_df[filtered_df['data_source'] == 'estimated']
        exchange_data = filtered_df[filtered_df['data_source'] == 'exchange']
        
        # Add baseline for log scale
        if y_scale == "Log" and not filtered_df.empty:
            fig.add_trace(go.Scatter(
                x=x_values,
                y=[y_min_chart] * len(x_values),
                mode='lines',
                name='baseline',
                line=dict(color='rgba(0,0,0,0)', width=0),
                showlegend=False,
                hoverinfo='skip',
                fill=None
            ))
        
        # Add estimated data (early Discord data) with different styling
        if not estimated_data.empty:
            est_x = estimated_data['days_from_genesis'] if x_scale_type == "Log" else estimated_data['Date']
            
            # Add confidence-based opacity
            confidence_colors = {
                'high': 'rgba(255, 140, 0, 0.8)',
                'medium': 'rgba(255, 140, 0, 0.6)', 
                'low': 'rgba(255, 140, 0, 0.4)'
            }
            
            # Group by confidence level for different opacities
            for confidence in ['high', 'medium', 'low']:
                conf_data = estimated_data[estimated_data['confidence'] == confidence] if 'confidence' in estimated_data.columns else pd.DataFrame()
                if not conf_data.empty:
                    conf_x = conf_data['days_from_genesis'] if x_scale_type == "Log" else conf_data['Date']
                    fig.add_trace(go.Scatter(
                        x=conf_x,
                        y=conf_data['Price'],
                        mode='lines+markers',
                        name=f'Discord Estimates ({confidence})',
                        line=dict(
                            color=confidence_colors.get(confidence, 'rgba(255, 140, 0, 0.6)'), 
                            width=2,
                            dash='dot' if confidence == 'low' else 'solid'
                        ),
                        marker=dict(
                            color=confidence_colors.get(confidence, 'rgba(255, 140, 0, 0.6)'),
                            size=4 if confidence == 'high' else 3
                        ),
                        hovertemplate=f'<b>Discord Estimate ({confidence})</b><br>Price: $%{{y:.6f}}<br>Date: %{{text}}<extra></extra>',
                        text=[d.strftime('%B %d, %Y') for d in conf_data['Date']],
                        showlegend=True
                    ))
        
        # Add exchange data with filled area
        if not exchange_data.empty:
            exch_x = exchange_data['days_from_genesis'] if x_scale_type == "Log" else exchange_data['Date']
            
            fill_mode = 'tonexty' if y_scale == "Log" else 'tozeroy'
            fig.add_trace(go.Scatter(
                x=exch_x,
                y=exchange_data['Price'],
                mode='lines',
                name='Exchange Data',
                line=dict(color='#5B6CFF', width=2),
                fill=fill_mode,
                fillgradient=dict(
                    type="vertical",
                    colorscale=[
                        [0, "rgba(13, 13, 26, 0.01)"],  # Top: transparent
                        [1, "rgba(91, 108, 255, 0.6)"]   # Bottom: full opacity
                    ]
                ),
                hovertemplate='<b>Exchange Data</b><br>Price: $%{y:.6f}<br>Date: %{text}<extra></extra>',
                text=[d.strftime('%B %d, %Y') for d in exchange_data['Date']],
                showlegend=True
            ))
    
    else:
        # Combined view - single trace for all data
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
            
            # Price trace fills to baseline
            fig.add_trace(go.Scatter(
                x=x_values,
                y=filtered_df['Price'],
                mode='lines',
                name='Kaspa Price (Combined)',
                line=dict(color='#5B6CFF', width=2),
                fill='tonexty',  # Fill to previous trace (baseline)
                fillgradient=dict(
                    type="vertical",
                    colorscale=[
                        [0, "rgba(13, 13, 26, 0.01)"],  # Top: transparent
                        [1, "rgba(91, 108, 255, 0.6)"]   # Bottom: full opacity
                    ]
                ),
                hovertemplate='<b>Kaspa Price</b><br>Price: $%{y:.6f}<br>Date: %{text}<extra></extra>',
                text=[d.strftime('%B %d, %Y') for d in filtered_df['Date']],
                showlegend=True
            ))
        else:
            # For linear scale: fill to zero (no extra chart area)
            fig.add_trace(go.Scatter(
                x=x_values,
                y=filtered_df['Price'],
                mode='lines',
                name='Kaspa Price (Combined)',
                line=dict(color='#5B6CFF', width=2),
                fill='tozeroy',  # Fill to zero
                fillgradient=dict(
                    type="vertical",
                    colorscale=[
                        [0, "rgba(13, 13, 26, 0.01)"],  # Top: transparent
                        [1, "rgba(91, 108, 255, 0.6)"]   # Bottom: full opacity
                    ]
                ),
                hovertemplate='<b>Kaspa Price</b><br>Price: $%{y:.6f}<br>Date: %{text}<extra></extra>',
                text=[d.strftime('%B %d, %Y') for d in filtered_df['Date']],
                showlegend=True
            ))

    # Add power law if enabled
    if show_power_law == "Show" and not filtered_df.empty:
        x_fit = filtered_df['days_from_genesis']
        y_fit = a_price * np.power(x_fit, b_price)
        fit_x = x_fit if x_scale_type == "Log" else filtered_df['Date']

        fig.add_trace(go.Scatter(
            x=fit_x,
            y=y_fit,
            mode='lines',
            name='Power Law Fit',
            line=dict(color='#ff8c00', width=2, dash='solid'),
            showlegend=True,
            hovertemplate='<b>Power Law Fit</b><br>Fit: $%{y:.6f}<extra></extra>',
        ))

    # Add ATH using separated function
    fig = add_ath_to_chart(fig, filtered_df, ath_price, ath_date, ath_days, x_scale_type)
    
    # Add 1YL using separated function
    fig = add_1yl_to_chart(fig, filtered_df, oyl_price, oyl_date, oyl_days, x_scale_type)

# Enhanced chart layout with custom logarithmic grid lines
x_axis_config = dict(
    gridcolor='#363650',
    gridwidth=1,
    color='#9CA3AF'
)

# Generate custom ticks for Y-axis if log scale
if y_scale == "Log" and not filtered_df.empty:
    y_major_ticks, y_intermediate_ticks, y_minor_ticks = generate_log_ticks(y_min_chart, y_max_chart)
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

# Empty annotations array since we're using scatter traces
annotations = []

fig.update_layout(
    xaxis_title=x_title if not filtered_df.empty else "Date",
    yaxis_title="Price (USD)",
    height=650,  # Increased from 450 to 650
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#9CA3AF', family='Inter'),
    hovermode='x unified',  # Always show unified hover for all traces at the same x-value
    hoverlabel=dict(
        bgcolor='rgba(15, 20, 25, 0.95)',
        bordercolor='rgba(91, 108, 255, 0.5)',
        font=dict(color='#e2e8f0', size=11),
        align='left',
        namelength=-1  # Show full trace names
    ),
    # Add ATH and 1YL annotations
    annotations=annotations,
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
        color='#9CA3AF',
        # Custom hover format for linear time scale
        hoverformat='%B %d, %Y' if x_scale_type == "Linear" else None,
        # Explicitly set x-axis range to prevent auto-expansion for text labels
        range=[
            np.log10(filtered_df['days_from_genesis'].min()) if x_scale_type == "Log" and not filtered_df.empty else filtered_df['Date'].min() if not filtered_df.empty else None,
            np.log10(filtered_df['days_from_genesis'].max()) if x_scale_type == "Log" and not filtered_df.empty else filtered_df['Date'].max() if not filtered_df.empty else None
        ] if not filtered_df.empty else None
    ),
    yaxis=dict(
        gridcolor='#363650',
        gridwidth=1,
        color='#9CA3AF',
        type="log" if y_scale == "Log" else "linear",
        # Explicitly set Y-axis range to eliminate gaps
        range=[np.log10(y_min_chart), np.log10(y_max_chart)] if y_scale == "Log" and not filtered_df.empty else [y_min_chart, y_max_chart] if not filtered_df.empty else None,
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
        orientation="h",  # Changed from "v" to "h" for horizontal
        bgcolor="rgba(0,0,0,0)",  # Transparent background
        color="#9CA3AF",
        activecolor="#5B6CFF"
    )
)

st.plotly_chart(fig, use_container_width=True, config={
    'displayModeBar': True,
    'displaylogo': False,
    'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
    'modeBarButtonsToAdd': ['hoverclosest', 'hovercompare'],
    'toImageButtonOptions': {
        'format': 'png',
        'filename': f'kaspa_enhanced_price_analysis_{datetime.now().strftime("%Y%m%d_%H%M")}',
        'height': 650,
        'width': 1400,
        'scale': 2
    }
})

# Calculate real metrics from combined data
if not combined_price_df.empty:
    current_price = combined_price_df['Price'].iloc[-1]
    
    # Calculate early data coverage
    early_data_count = len(early_data_df) if not early_data_df.empty else 0
    exchange_data_count = len(combined_price_df[combined_price_df['data_source'] == 'exchange']) if 'data_source' in combined_price_df.columns else len(combined_price_df)
    total_data_points = len(combined_price_df)
    
    # Calculate data coverage percentage
    early_coverage_pct = (early_data_count / total_data_points) * 100 if total_data_points > 0 else 0
    
    # Calculate 30-day metrics for power law slope and R² changes
    thirty_days_ago = combined_price_df['Date'].iloc[-1] - timedelta(days=30)
    df_30_days_ago = combined_price_df[combined_price_df['Date'] <= thirty_days_ago]
    
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
    df_30_days = combined_price_df[combined_price_df['Date'] >= thirty_days_ago]
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
    early_data_count = 0
    early_coverage_pct = 0

# Enhanced metrics cards with data coverage information
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
        <div class="metric-label">Early Data Points</div>
        <div class="metric-value">{early_data_count}</div>
        <div class="metric-change positive">{early_coverage_pct:.1f}% coverage</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Est. Market Cap</div>
        <div class="metric-value">${market_cap_estimate/1e9:.2f}B</div>
        <div class="metric-change {'positive' if price_pct_change >= 0 else 'negative'}">{price_pct_change:+.1f}%</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Enhanced analysis section with data source insights
price_trend = "bullish" if price_pct_change > 5 else "bearish" if price_pct_change < -5 else "sideways"
slope_trend = "increasing" if slope_pct_change > 0 else "decreasing"

# Calculate data quality metrics
high_confidence_count = len(early_data_df[early_data_df['confidence'] == 'high']) if not early_data_df.empty and 'confidence' in early_data_df.columns else 0
medium_confidence_count = len(early_data_df[early_data_df['confidence'] == 'medium']) if not early_data_df.empty and 'confidence' in early_data_df.columns else 0
low_confidence_count = len(early_data_df[early_data_df['confidence'] == 'low']) if not early_data_df.empty and 'confidence' in early_data_df.columns else 0

st.markdown(f"""
<div class="analysis-section">
    <div class="analysis-card">
        <h3 class="section-title">Enhanced Data Insights</h3>
        <ul class="insights-list">
            <li>Combined dataset spans <strong>{len(combined_price_df)}</strong> data points from genesis</li>
            <li>Early Discord estimates: <span class="data-quality-high">{high_confidence_count} high</span>, <span class="data-quality-medium">{medium_confidence_count} medium</span>, <span class="data-quality-low">{low_confidence_count} low</span> confidence</li>
            <li>Power law model R² of <strong>{r2_price:.3f}</strong> shows {'strong' if r2_price > 0.8 else 'moderate' if r2_price > 0.6 else 'weak'} correlation across full history</li>
            <li>Early data fills the critical first <strong>{early_coverage_pct:.1f}%</strong> of price history</li>
            <li>Combined analysis reveals more accurate long-term growth patterns</li>
        </ul>
    </div>
    <div class="analysis-card">
        <h3 class="section-title">Data Source Coverage</h3>
""", unsafe_allow_html=True)

# Enhanced mini chart showing data source coverage
if not combined_price_df.empty and 'data_source' in combined_price_df.columns:
    # Create a simple timeline showing data sources
    source_timeline = combined_price_df.groupby(['Date', 'data_source']).size().reset_index(name='count')
    
    mini_fig = go.Figure()
    
    # Add traces for each data source
    for source in source_timeline['data_source'].unique():
        source_data = source_timeline[source_timeline['data_source'] == source]
        color = '#ff8c00' if source == 'estimated' else '#5B6CFF'
        name = 'Discord Estimates' if source == 'estimated' else 'Exchange Data'
        
        mini_fig.add_trace(go.Scatter(
            x=source_data['Date'],
            y=[1] * len(source_data),
            mode='markers',
            name=name,
            marker=dict(
                color=color,
                size=8,
                symbol='circle'
            ),
            hovertemplate=f'<b>{name}</b><br>Date: %{{x}}<extra></extra>',
            showlegend=True
        ))
    
    mini_fig.update_layout(
        height=150,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#9CA3AF', family='Inter', size=10),
        xaxis=dict(
            gridcolor='#363650',
            gridwidth=1,
            color='#9CA3AF',
            showticklabels=True,
            title="Timeline Coverage"
        ),
        yaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False,
            range=[0.5, 1.5]
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5,
            bgcolor='rgba(0,0,0,0)',
            font=dict(size=10)
        ),
        margin=dict(l=0, r=0, t=10, b=40)
    )
    
    st.plotly_chart(mini_fig, use_container_width=True)

elif not combined_price_df.empty:
    # Fallback: show simple timeline of all data points
    mini_fig = go.Figure()
    
    mini_fig.add_trace(go.Scatter(
        x=combined_price_df['Date'],
        y=[1] * len(combined_price_df),
        mode='markers',
        name='Price Data',
        marker=dict(
            color='#5B6CFF',
            size=6,
            symbol='circle'
        ),
        hovertemplate='<b>Price Data</b><br>Date: %{x}<extra></extra>',
        showlegend=False
    ))
    
    mini_fig.update_layout(
        height=150,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#9CA3AF', family='Inter', size=10),
        xaxis=dict(
            gridcolor='#363650',
            gridwidth=1,
            color='#9CA3AF',
            showticklabels=True,
            title="Data Coverage Timeline"
        ),
        yaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False,
            range=[0.5, 1.5]
        ),
        margin=dict(l=0, r=0, t=10, b=40)
    )
    
    st.plotly_chart(mini_fig, use_container_width=True)
        yaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False,
            range=[0.5, 1.5]
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5,
            bgcolor='rgba(0,0,0,0)',
            font=dict(size=10)
        ),
        margin=dict(l=0, r=0, t=10, b=40)
    )
    
    st.plotly_chart(mini_fig, use_container_width=True)

else:
    st.info("No data available for source coverage visualization")

st.markdown("""
    </div>
</div>
""", unsafe_allow_html=True)

# Data quality and methodology section
st.markdown(f"""
<div class="analysis-section">
    <div class="analysis-card">
        <h3 class="section-title">Data Methodology</h3>
        <ul class="insights-list">
            <li><strong>Discord Estimates (2021-11-16 to 2022-08-09):</strong> Community-driven price estimates from Kaspa Discord</li>
            <li><strong>Confidence Levels:</strong> High, medium, and low based on market activity and offer volume</li>
            <li><strong>Exchange Data (2022-05-25+):</strong> Official trading data from cryptocurrency exchanges</li>
            <li><strong>Transition Period:</strong> Overlapping data sources provide validation of estimate accuracy</li>
            <li><strong>Power Law Fit:</strong> Applied across complete dataset for comprehensive trend analysis</li>
        </ul>
    </div>
    <div class="analysis-card">
        <h3 class="section-title">Historical Significance</h3>
        <ul class="insights-list">
            <li>Genesis date: <strong>November 7, 2021</strong> - Kaspa mainnet launch</li>
            <li>First ~200 days now captured through Discord community estimates</li>
            <li>Early price discovery period shows significant volatility and growth</li>
            <li>Transition to exchange trading marked increased stability and volume</li>
            <li>Combined dataset enables full-cycle analysis from launch to present</li>
        </ul>
    </div>
</div>
""", unsafe_allow_html=True)

# Enhanced data refresh controls
st.markdown("""
<div class="analysis-card" style="margin-top: 2rem;">
    <h3 class="section-title">Data Management</h3>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔄 Refresh Google Sheets Data", key="refresh_sheets"):
        # Clear the cache and reload data
        st.cache_data.clear()
        st.session_state.combined_price_df, st.session_state.price_genesis_date, st.session_state.early_data_df = combine_price_datasets()
        st.success("✅ Data refreshed successfully!")
        st.rerun()

with col2:
    if st.button("📊 Download Combined Dataset", key="download_data"):
        if not combined_price_df.empty:
            csv_data = combined_price_df.to_csv(index=False)
            st.download_button(
                label="💾 Download CSV",
                data=csv_data,
                file_name=f"kaspa_enhanced_price_data_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )

with col3:
    if st.button("📈 Export Chart Data", key="export_chart"):
        if not filtered_df.empty:
            chart_data = filtered_df[['Date', 'Price', 'days_from_genesis', 'data_source']].copy()
            csv_data = chart_data.to_csv(index=False)
            st.download_button(
                label="💾 Download Chart CSV",
                data=csv_data,
                file_name=f"kaspa_chart_data_{time_range}_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )

st.markdown("</div>", unsafe_allow_html=True)

# Footer with data source attribution
st.markdown("""
<div style="margin-top: 3rem; padding: 1.5rem; background: rgba(26, 26, 46, 0.3); border-radius: 12px; border: 1px solid rgba(54, 54, 80, 0.4);">
    <h4 style="color: #FFFFFF; margin-bottom: 1rem;">📊 Data Sources & Credits</h4>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; color: #9CA3AF; font-size: 0.9rem;">
        <div>
            <strong style="color: #ff8c00;">Early Discord Estimates:</strong><br>
            • Source: Kaspa Discord Community<br>
            • Period: Nov 2021 - Aug 2022<br>
            • Data Points: {early_data_count}<br>
            • Confidence Levels: High/Medium/Low
        </div>
        <div>
            <strong style="color: #5B6CFF;">Exchange Data:</strong><br>
            • Source: Cryptocurrency Exchanges<br>
            • Period: May 2022 - Present<br>
            • Data Points: {exchange_data_count}<br>
            • Quality: High (Official Trading)
        </div>
    </div>
    <hr style="border: none; border-top: 1px solid rgba(54, 54, 80, 0.4); margin: 1rem 0;">
    <p style="color: #9CA3AF; font-size: 0.85rem; margin: 0; text-align: center;">
        🔗 <strong>Google Sheets Integration:</strong> <a href="https://docs.google.com/spreadsheets/d/1zwQ_Ew2G_reqTYhCCIT276ph5aG-rxNT4BRLL88c38w/edit?gid=275707638#gid=275707638" 
        target="_blank" style="color: #5B6CFF;">KaspaPriceHistoryFirst200days</a> | 
        💡 <strong>Enhanced Analysis:</strong> Combined dataset provides comprehensive price history from genesis to present
    </p>
</div>
""".format(early_data_count=early_data_count, exchange_data_count=exchange_data_count), unsafe_allow_html=True)

# At the end of each page:
from footer import add_footer
add_footer()
