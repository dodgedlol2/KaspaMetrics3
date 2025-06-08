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
st.set_page_config(page_title="Advanced Metrics", page_icon="📊", layout="wide")

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
    st.info("Upgrade your account to access advanced metrics")
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
    if st.button("Logout", key="logout_advanced"):
        st.session_state.clear()
        st.switch_page("Home.py")

# Main content
st.title("📊 Advanced Metrics")
st.write("Deep dive analytics and custom indicators")

# Advanced metrics grid
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("MVRV Ratio", "1.85", "+0.12")
with col2:
    st.metric("NVT Ratio", "28.4", "-2.1")
with col3:
    st.metric("Active Addresses", "12.5K", "+8.2%")
with col4:
    st.metric("Transaction Count", "45.2K", "+5.7%")

# Correlation matrix
st.subheader("🔗 Correlation Analysis")

# Sample correlation data
metrics = ['Price', 'Volume', 'Hashrate', 'Active Addresses', 'Transaction Count']
correlation_matrix = np.random.rand(5, 5)
correlation_matrix = (correlation_matrix + correlation_matrix.T) / 2  # Make symmetric
np.fill_diagonal(correlation_matrix, 1)  # Diagonal should be 1

fig = go.Figure(data=go.Heatmap(
    z=correlation_matrix,
    x=metrics,
    y=metrics,
    colorscale='RdBu',
    zmid=0
))

fig.update_layout(
    title="Metrics Correlation Matrix",
    height=400,
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

# Custom indicators
st.subheader("🎯 Custom Indicators")
col1, col2 = st.columns(2)

with col1:
    # Network health score
    health_score = 8.7
    health_fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = health_score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Network Health Score"},
        delta = {'reference': 8.5},
        gauge = {
            'axis': {'range': [None, 10]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 5], 'color': "lightgray"},
                {'range': [5, 8], 'color': "gray"},
                {'range': [8, 10], 'color': "lightgreen"}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 9}}))
    
    health_fig.update_layout(height=300)
    st.plotly_chart(health_fig, use_container_width=True)

with col2:
    # Market momentum indicator
    momentum_dates = pd.date_range(start='2024-05-15', end='2024-06-01', freq='D')
    momentum_data = np.random.normal(0.6, 0.2, len(momentum_dates))
    
    momentum_fig = go.Figure()
    momentum_fig.add_trace(go.Scatter(
        x=momentum_dates,
        y=momentum_data,
        mode='lines+markers',
        name='Market Momentum',
        line=dict(color='#ff7f0e', width=3)
    ))
    
    momentum_fig.update_layout(
        title="Market Momentum Index",
        height=300,
        template="plotly_white"
    )
    
    st.plotly_chart(momentum_fig, use_container_width=True)

# Custom alerts
st.subheader("🔔 Custom Alerts")

col1, col2 = st.columns(2)
with col1:
    st.selectbox("Metric", ["Price", "Volume", "Hashrate", "Active Addresses"])
    st.selectbox("Condition", ["Above", "Below", "Change %"])
    st.number_input("Threshold", value=0.15)

with col2:
    st.text_input("Alert Name", "Price Alert")
    st.selectbox("Notification", ["Email", "SMS", "Discord"])
    if st.button("Create Alert", type="primary"):
        st.success("Alert created successfully!")

# Advanced analytics table
st.subheader("📈 Advanced Analytics Summary")
analytics_data = {
    "Metric": ["Sharpe Ratio", "Volatility (30d)", "Beta vs BTC", "Max Drawdown", "Recovery Time"],
    "Value": ["1.42", "68.5%", "0.73", "-23.1%", "12 days"],
    "Trend": ["↑", "→", "↓", "↑", "↓"],
    "Rating": ["Good", "High", "Moderate", "Acceptable", "Fast"]
}

df_analytics = pd.DataFrame(analytics_data)
st.dataframe(df_analytics, use_container_width=True)

# Export functionality
st.subheader("💾 Data Export")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("📊 Export Charts", use_container_width=True):
        st.success("Charts exported to PNG format")
with col2:
    if st.button("📋 Export Data (CSV)", use_container_width=True):
        st.success("Data exported to CSV format")
with col3:
    if st.button("📑 Generate Report", use_container_width=True):
        st.success("PDF report generated")

# Navigation
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🔬 Premium Analytics", use_container_width=True):
        st.switch_page("pages/8_👑_Premium_Analytics.py")
with col2:
    if st.button("💰 Market Data", use_container_width=True):
        st.switch_page("pages/3_💰_Spot_Price.py")
with col3:
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("Home.py")
