import streamlit as st

# Page config MUST be first!
st.set_page_config(page_title="Premium Analytics", page_icon="🔬", layout="wide")

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

# Add shared navigation to sidebar
add_navigation()

# Initialize handlers
@st.cache_resource
def init_handlers():
    db = Database()
    auth_handler = AuthHandler(db)
    payment_handler = PaymentHandler()
    return db, auth_handler, payment_handler

db, auth_handler, payment_handler = init_handlers()

# Premium access check
if not st.session_state.get('authentication_status'):
    st.error("🔐 Please login to access premium features")
    if st.button("Go to Login"):
        st.switch_page("Home.py")
    st.stop()

if not st.session_state.get('is_premium', False):
    st.error("🔒 Premium subscription required for this page")
    st.info("Upgrade your account to access advanced analytics")
    if st.button("Upgrade Now"):
        st.switch_page("Home.py")
    st.stop()

# Header with user info
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("### ⚡ Kaspa Analytics")
with col2:
    welcome_msg = f"👋 {st.session_state.get('name', 'User')} 👑"
    st.write(welcome_msg)
    if st.button("Logout", key="logout_premium"):
        st.session_state.clear()
        st.switch_page("Home.py")

# Main content
st.title("🔬 Premium Analytics")
st.write("Advanced analytics and insights for premium subscribers")

# Premium metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Whale Activity", "High", "↑15%")
with col2:
    st.metric("Flow Ratio", "1.24", "+0.08")
with col3:
    st.metric("Network Value", "$2.8B", "+3.2%")

# Advanced chart with multiple metrics
dates = pd.date_range(start='2024-01-01', end='2024-06-01', freq='D')

fig = go.Figure()

# Price
price_data = np.random.normal(0.125, 0.01, len(dates))
fig.add_trace(go.Scatter(
    x=dates, y=price_data, name='Price', 
    line=dict(color='#1f77b4'), yaxis='y'
))

# Volume (secondary y-axis)
volume_data = np.random.normal(45000000, 10000000, len(dates))
fig.add_trace(go.Scatter(
    x=dates, y=volume_data, name='Volume',
    line=dict(color='#ff7f0e'), yaxis='y2'
))

fig.update_layout(
    title="Premium Multi-Metric Analysis",
    xaxis_title="Date",
    yaxis=dict(title="Price (USD)", side="left"),
    yaxis2=dict(title="Volume (USD)", side="right", overlaying="y"),
    height=400,
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

# Advanced metrics grid
st.subheader("📊 Advanced On-Chain Metrics")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("MVRV Ratio", "1.85", "+0.12")
with col2:
    st.metric("NVT Ratio", "28.4", "-2.1")
with col3:
    st.metric("Active Addresses", "12.5K", "+8.2%")
with col4:
    st.metric("Transaction Count", "45.2K", "+5.7%")

# AI-Powered insights
st.subheader("🎯 AI-Powered Insights")
col1, col2 = st.columns(2)

with col1:
    st.info("📊 Current market conditions suggest accumulation phase based on on-chain metrics")
    st.success("🚀 Technical indicators show potential breakout in 7-14 days")
    st.warning("⚠️ Whale activity increased by 15% - monitor for potential volatility")

with col2:
    # Prediction chart
    future_dates = pd.date_range(start='2024-06-01', periods=30, freq='D')
    prediction_data = np.random.normal(0.135, 0.005, 30)
    
    pred_fig = go.Figure()
    pred_fig.add_trace(go.Scatter(
        x=future_dates,
        y=prediction_data,
        mode='lines',
        name='AI Prediction',
        line=dict(color='#2ca02c', width=3, dash='dash')
    ))
    
    pred_fig.update_layout(
        title="30-Day Price Prediction",
        height=250,
        template="plotly_white"
    )
    
    st.plotly_chart(pred_fig, use_container_width=True)

# Whale tracking
st.subheader("🐋 Whale Activity Monitor")
whale_data = {
    "Wallet": ["Whale_1", "Whale_2", "Whale_3", "Whale_4"],
    "Balance": ["2.5M KAS", "1.8M KAS", "1.2M KAS", "950K KAS"],
    "24h Change": ["+50K", "-25K", "+15K", "0"],
    "Action": ["Accumulating", "Distributing", "Accumulating", "Holding"]
}

df_whales = pd.DataFrame(whale_data)
st.dataframe(df_whales, use_container_width=True)

# Navigation
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("📊 Advanced Metrics", use_container_width=True):
        st.switch_page("pages/9_👑_Advanced_Metrics.py")
with col2:
    if st.button("💰 Market Data", use_container_width=True):
        st.switch_page("pages/3_💰_Spot_Price.py")
with col3:
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("Home.py")
