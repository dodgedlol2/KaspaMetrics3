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

st.markdown("**Kaspa Network Hashrate**")

st.markdown("""
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
