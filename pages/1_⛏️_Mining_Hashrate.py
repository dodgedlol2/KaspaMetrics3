import streamlit as st

# Page config MUST be first!
st.set_page_config(page_title="Mining Hashrate", page_icon="📈", layout="wide")

import plotly.graph_objects as go
import pandas as pd
import numpy as np
import sys
import os

# Add parent directory to path for imports
parent_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(parent_dir)

from database import Database
from auth_handler import AuthHandler
from payment_handler import PaymentHandler
from navigation import add_navigation

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

# Custom CSS for Betterstack-inspired dark theme
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
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1200px;
}

/* Main gradient title */
.hero-section {
    padding: 2rem 0;
    margin-bottom: 3rem;
}

.gradient-title {
    background: linear-gradient(90deg, #FFFFFF 0%, #A0A0B8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 3.5rem;
    font-weight: 800;
    text-align: center;
    margin-bottom: 1rem;
    font-family: 'Inter', sans-serif;
    letter-spacing: -0.03em;
    line-height: 1.1;
    text-shadow: 0 0 20px rgba(255, 255, 255, 0.15);
    filter: drop-shadow(0 0 8px rgba(255, 255, 255, 0.1));
}

.hero-subtitle {
    color: #9CA3AF;
    font-size: 1.25rem;
    text-align: center;
    margin-bottom: 0;
    font-weight: 400;
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
}

/* Metrics cards */
.metrics-container {
    display: flex;
    gap: 1.5rem;
    margin-bottom: 3rem;
    flex-wrap: wrap;
}

.metric-card {
    background: linear-gradient(135deg, #1A1A2E 0%, #161629 100%);
    border: 1px solid #363650;
    border-radius: 16px;
    padding: 1.5rem;
    flex: 1;
    min-width: 250px;
    position: relative;
    overflow: hidden;
}

.metric-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, #5B6CFF, #6366F1);
}

.metric-value {
    font-size: 2.5rem;
    font-weight: 700;
    color: #FFFFFF;
    margin-bottom: 0.5rem;
    font-family: 'Inter', sans-serif;
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
    .gradient-title {
        font-size: 2.5rem;
    }
    
    .analysis-section {
        grid-template-columns: 1fr;
    }
    
    .metrics-container {
        flex-direction: column;
    }
    
    .hero-section {
        padding: 2rem 1rem;
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

# Hero Section
st.markdown("""
<div class="hero-section">
    <h1 class="gradient-title">Kaspa Network Hashrate</h1>
    <p class="hero-subtitle">Real-time network hashrate metrics and comprehensive mining analytics</p>
</div>
""", unsafe_allow_html=True)

# Sample data - replace with real Kaspa API data later
dates = pd.date_range(start='2024-01-01', end='2024-06-01', freq='D')
hashrate_data = np.random.normal(1.2, 0.1, len(dates))  # EH/s

# Custom metrics cards
st.markdown("""
<div class="metrics-container">
    <div class="metric-card">
        <div class="metric-label">Current Hashrate</div>
        <div class="metric-value">1.24 EH/s</div>
        <div class="metric-change">+2.1%</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">7d Average</div>
        <div class="metric-value">1.18 EH/s</div>
        <div class="metric-change">+0.8%</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">30d Average</div>
        <div class="metric-value">1.15 EH/s</div>
        <div class="metric-change">+5.2%</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Hashrate chart with dark theme
st.markdown('<div class="chart-container">', unsafe_allow_html=True)

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=dates,
    y=hashrate_data,
    mode='lines',
    name='Hashrate (EH/s)',
    line=dict(color='#5B6CFF', width=3),
    fill='tonexty',
    fillcolor='rgba(91, 108, 255, 0.1)'
))

fig.update_layout(
    title={
        'text': "Network Hashrate Trends",
        'font': {'size': 24, 'color': '#FFFFFF', 'family': 'Inter'},
        'x': 0.02
    },
    xaxis_title="Date",
    yaxis_title="Hashrate (EH/s)",
    height=450,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#9CA3AF', family='Inter'),
    xaxis=dict(
        gridcolor='#363650',
        gridwidth=1,
        color='#9CA3AF'
    ),
    yaxis=dict(
        gridcolor='#363650',
        gridwidth=1,
        color='#9CA3AF'
    ),
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Analysis section
st.markdown("""
<div class="analysis-section">
    <div class="analysis-card">
        <h3 class="section-title">Key Insights</h3>
        <ul class="insights-list">
            <li>Network hashrate has grown 15% over the past month</li>
            <li>Mining difficulty adjustment maintains ~1 block per second</li>
            <li>Increased hashrate indicates growing miner confidence</li>
            <li>Current hashrate suggests strong network security</li>
        </ul>
    </div>
    <div class="analysis-card">
        <h3 class="section-title">30-Day Trend</h3>
""", unsafe_allow_html=True)

# Mini chart for recent trends
recent_dates = dates[-30:]
recent_data = hashrate_data[-30:]

mini_fig = go.Figure()
mini_fig.add_trace(go.Scatter(
    x=recent_dates,
    y=recent_data,
    mode='lines+markers',
    name='30-Day Trend',
    line=dict(color='#6366F1', width=3),
    marker=dict(color='#5B6CFF', size=4),
    fill='tonexty',
    fillcolor='rgba(99, 102, 241, 0.1)'
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
        color='#9CA3AF'
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
