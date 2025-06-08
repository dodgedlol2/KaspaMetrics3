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

from navigation import add_navigation

# NOW add navigation (after page config)
add_navigation()

# Page config
st.set_page_config(page_title="Mining Difficulty", page_icon="⚙️", layout="wide")

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
        if st.button("Logout", key="logout_difficulty"):
            st.session_state.clear()
            st.switch_page("Home.py")
    else:
        if st.button("Login", key="login_difficulty"):
            st.switch_page("Home.py")

# Main content
st.title("⚙️ Mining Difficulty")
st.write("Network difficulty adjustments and mining complexity metrics")

# Sample difficulty data
dates = pd.date_range(start='2024-01-01', end='2024-06-01', freq='D')
difficulty_data = np.random.normal(15.5e12, 1e12, len(dates))

# Current metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Current Difficulty", "15.8T", "+1.2%")
with col2:
    st.metric("Next Adjustment", "~2 days", "")
with col3:
    st.metric("Est. Change", "+0.8%", "")

# Difficulty chart
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=dates,
    y=difficulty_data,
    mode='lines',
    name='Difficulty',
    line=dict(color='#ff7f0e', width=2)
))

fig.update_layout(
    title="Mining Difficulty Over Time",
    xaxis_title="Date",
    yaxis_title="Difficulty",
    height=400,
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

# Difficulty adjustment info
st.subheader("🔄 Difficulty Adjustment Mechanism")

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    **How It Works:**
    - Kaspa adjusts difficulty every block
    - Target: 1 block per second average
    - Based on recent block times
    - Maintains network stability
    """)

with col2:
    # Adjustment prediction chart
    future_dates = pd.date_range(start='2024-06-01', periods=14, freq='D')
    predicted_difficulty = np.random.normal(16.0e12, 0.5e12, 14)
    
    pred_fig = go.Figure()
    pred_fig.add_trace(go.Scatter(
        x=future_dates,
        y=predicted_difficulty,
        mode='lines+markers',
        name='Predicted Difficulty',
        line=dict(color='#2ca02c', width=2, dash='dash')
    ))
    
    pred_fig.update_layout(
        title="14-Day Difficulty Prediction",
        height=250,
        template="plotly_white"
    )
    
    st.plotly_chart(pred_fig, use_container_width=True)

# Navigation
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("📈 Hashrate", use_container_width=True):
        st.switch_page("pages/1_⛏️_Mining_Hashrate.py")
with col2:
    if st.button("💰 Price Data", use_container_width=True):
        st.switch_page("pages/3_💰_Spot_Price.py")
with col3:
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("Home.py")
