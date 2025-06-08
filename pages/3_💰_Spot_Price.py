import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from database import Database
from auth_handler import AuthHandler
from payment_handler import PaymentHandler

# Page config
st.set_page_config(page_title="Kaspa Price", page_icon="💵", layout="wide")

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
        if st.button("Logout", key="logout_price"):
            st.session_state.clear()
            st.switch_page("Home.py")
    else:
        if st.button("Login", key="login_price"):
            st.switch_page("Home.py")

# Main content
st.title("💵 Kaspa Price")
st.write("Real-time price data and market trends")

# Sample price data
dates = pd.date_range(start='2024-01-01', end='2024-06-01', freq='h')
price_data = np.random.normal(0.125, 0.01, len(dates))

# Current metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Current Price", "$0.1247", "+2.4%")
with col2:
    st.metric("24h High", "$0.1289", "")
with col3:
    st.metric("24h Low", "$0.1205", "")
with col4:
    st.metric("24h Change", "+$0.0029", "+2.4%")

# Price chart
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=dates[-168:],  # Last 7 days
    y=price_data[-168:],
    mode='lines',
    name='KAS/USD',
    line=dict(color='#2ca02c', width=2)
))

fig.update_layout(
    title="KAS/USD Price (7 Days)",
    xaxis_title="Time",
    yaxis_title="Price (USD)",
    height=400,
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

# Price analysis
st.subheader("📈 Price Analysis")

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    **Market Summary:**
    - KAS has shown strong upward momentum
    - Trading volume increased 15% in past 24h
    - Support level established at $0.120
    - Resistance near $0.130 level
    """)

with col2:
    # Volume chart
    volume_dates = dates[-24:]  # Last 24 hours
    volume_data = np.random.normal(5000000, 1000000, 24)
    
    vol_fig = go.Figure()
    vol_fig.add_trace(go.Bar(
        x=volume_dates,
        y=volume_data,
        name='Hourly Volume',
        marker_color='#ff7f0e'
    ))
    
    vol_fig.update_layout(
        title="24h Trading Volume",
        height=250,
        template="plotly_white"
    )
    
    st.plotly_chart(vol_fig, use_container_width=True)

# Price targets
st.subheader("🎯 Technical Levels")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Support 1", "$0.120", "Strong")
with col2:
    st.metric("Resistance 1", "$0.130", "Moderate")
with col3:
    st.metric("Next Target", "$0.140", "Bullish")

# Navigation
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("📊 Volume", use_container_width=True):
        st.switch_page("pages/4_💰_Spot_Volume.py")
with col2:
    if st.button("🏦 Market Cap", use_container_width=True):
        st.switch_page("pages/5_💰_Spot_Market_Cap.py")
with col3:
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("Home.py")
