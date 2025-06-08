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

# Header with user info
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("### ⚡ Kaspa Analytics")
with col2:
    if st.session_state.get('authentication_status'):
        welcome_msg = f"👋 {st.session_state.get('name', 'User')}"
        if st.session_state.get('is_premium'):
            welcome_msg += " 👑"
        st.write(welcome_msg)
        if st.button("Logout", key="logout_hashrate"):
            st.session_state.clear()
            st.switch_page("Home.py")
    else:
        if st.button("Login", key="login_hashrate"):
            st.switch_page("Home.py")

# Main content
st.title("📈 Kaspa Network Hashrate")
st.write("Current network hashrate metrics and mining trends")

# Sample data - replace with real Kaspa API data later
dates = pd.date_range(start='2024-01-01', end='2024-06-01', freq='D')
hashrate_data = np.random.normal(1.2, 0.1, len(dates))  # EH/s

# Current metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Current Hashrate", "1.24 EH/s", "+2.1%")
with col2:
    st.metric("7d Average", "1.18 EH/s", "+0.8%")
with col3:
    st.metric("30d Average", "1.15 EH/s", "+5.2%")

# Hashrate chart
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=dates,
    y=hashrate_data,
    mode='lines',
    name='Hashrate (EH/s)',
    line=dict(color='#1f77b4', width=2)
))

fig.update_layout(
    title="Kaspa Network Hashrate Over Time",
    xaxis_title="Date",
    yaxis_title="Hashrate (EH/s)",
    height=400,
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

# Additional insights
st.subheader("📊 Hashrate Analysis")

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    **Key Insights:**
    - Network hashrate has grown 15% over the past month
    - Mining difficulty adjustment maintains ~1 block per second
    - Increased hashrate indicates growing miner confidence
    - Current hashrate suggests strong network security
    """)

with col2:
    # Mini chart for recent trends
    recent_dates = dates[-30:]
    recent_data = hashrate_data[-30:]
    
    mini_fig = go.Figure()
    mini_fig.add_trace(go.Scatter(
        x=recent_dates,
        y=recent_data,
        mode='lines+markers',
        name='30-Day Trend',
        line=dict(color='#ff7f0e', width=3)
    ))
    
    mini_fig.update_layout(
        title="30-Day Hashrate Trend",
        height=250,
        template="plotly_white",
        showlegend=False
    )
    
    st.plotly_chart(mini_fig, use_container_width=True)

# Navigation
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("⚙️ Mining Difficulty", use_container_width=True):
        st.switch_page("pages/2_⛏️_Mining_Difficulty.py")
with col2:
    if st.button("💰 Price Data", use_container_width=True):
        st.switch_page("pages/3_💰_Spot_Price.py")
with col3:
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("Home.py")
