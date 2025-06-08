import streamlit as st

# Page config
st.set_page_config(page_title="Trading Volume", page_icon="📊", layout="wide")

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
st.set_page_config(page_title="Trading Volume", page_icon="📊", layout="wide")

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
        if st.button("Logout", key="logout_volume"):
            st.session_state.clear()
            st.switch_page("Home.py")
    else:
        if st.button("Login", key="login_volume"):
            st.switch_page("Home.py")

# Main content
st.title("📊 Trading Volume")
st.write("24h trading volume across exchanges")

# Sample volume data
dates = pd.date_range(start='2024-01-01', end='2024-06-01', freq='D')
volume_data = np.random.normal(45000000, 10000000, len(dates))

# Current metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("24h Volume", "$42.8M", "-5.2%")
with col2:
    st.metric("7d Average", "$47.2M", "+2.1%")
with col3:
    st.metric("Volume Rank", "#45", "")

# Volume chart
fig = go.Figure()
fig.add_trace(go.Bar(
    x=dates[-30:],  # Last 30 days
    y=volume_data[-30:],
    name='Volume (USD)',
    marker_color='#d62728'
))

fig.update_layout(
    title="Daily Trading Volume (30 Days)",
    xaxis_title="Date",
    yaxis_title="Volume (USD)",
    height=400,
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

# Exchange breakdown
st.subheader("📈 Exchange Breakdown")
col1, col2 = st.columns(2)

with col1:
    # Pie chart of exchange volumes
    exchanges = ['KuCoin', 'Gate.io', 'MEXC', 'Others']
    exchange_volumes = [15.2, 12.8, 8.4, 6.4]
    
    pie_fig = go.Figure(data=[go.Pie(labels=exchanges, values=exchange_volumes)])
    pie_fig.update_layout(title="Volume by Exchange (24h)")
    st.plotly_chart(pie_fig, use_container_width=True)

with col2:
    st.markdown("""
    **Volume Analysis:**
    - KuCoin leads with 35.5% of total volume
    - Gate.io follows with 29.9% market share
    - Volume decreased 5.2% in last 24h
    - Weekly average remains healthy at $47.2M
    """)

# Navigation
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("💵 Price", use_container_width=True):
        st.switch_page("pages/3_💰_Spot_Price.py")
with col2:
    if st.button("🏦 Market Cap", use_container_width=True):
        st.switch_page("pages/5_💰_Spot_Market_Cap.py")
with col3:
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("Home.py")
