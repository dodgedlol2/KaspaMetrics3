import streamlit as st

# Page config
st.set_page_config(page_title="Social Metrics", page_icon="📱", layout="wide")

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
        if st.button("Logout", key="logout_social"):
            st.session_state.clear()
            st.switch_page("Home.py")
    else:
        if st.button("Login", key="login_social"):
            st.switch_page("Home.py")

# Main content
st.title("📱 Social Metrics")
st.write("Kaspa community engagement and social sentiment")

# Social metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Twitter Followers", "285K", "+1.2%")
with col2:
    st.metric("Reddit Members", "42K", "+2.8%")
with col3:
    st.metric("Discord Members", "18K", "+0.5%")
with col4:
    st.metric("Social Score", "8.2/10", "+0.1")

# Sample sentiment data
dates = pd.date_range(start='2024-05-01', end='2024-06-01', freq='D')
sentiment_data = np.random.normal(0.65, 0.15, len(dates))

# Sentiment chart
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=dates,
    y=sentiment_data,
    mode='lines+markers',
    name='Sentiment Score',
    line=dict(color='#17becf', width=2)
))

fig.update_layout(
    title="Social Sentiment Trend",
    xaxis_title="Date",
    yaxis_title="Sentiment Score",
    height=400,
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

# Platform breakdown
st.subheader("🌐 Platform Activity")
col1, col2 = st.columns(2)

with col1:
    # Platform engagement chart
    platforms = ['Twitter', 'Reddit', 'Discord', 'Telegram']
    engagement = [8.5, 7.2, 6.8, 5.5]
    
    platform_fig = go.Figure(data=[go.Bar(x=platforms, y=engagement, marker_color='#2ca02c')])
    platform_fig.update_layout(title="Platform Engagement Score", yaxis_title="Score")
    st.plotly_chart(platform_fig, use_container_width=True)

with col2:
    st.markdown("""
    **Community Insights:**
    - Twitter shows highest engagement rates
    - Reddit discussions focus on technical topics
    - Discord active with 500+ daily messages
    - Growing international community presence
    """)

# Recent activity
st.subheader("📊 Recent Activity")
activity_data = {
    "Platform": ["Twitter", "Reddit", "Discord", "Telegram"],
    "Daily Posts": [125, 45, 230, 89],
    "Engagement Rate": ["3.2%", "5.8%", "12.1%", "4.5%"],
    "Top Topic": ["Price Analysis", "Tech Discussion", "Community Chat", "News Sharing"]
}

df = pd.DataFrame(activity_data)
st.dataframe(df, use_container_width=True)

# Navigation
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("📊 Social Trends", use_container_width=True):
        st.switch_page("pages/7_📱_Social_Trends.py")
with col2:
    if st.button("⛏️ Mining Data", use_container_width=True):
        st.switch_page("pages/1_⛏️_Mining_Hashrate.py")
with col3:
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("Home.py")
