import streamlit as st

# Page config MUST be first!
st.set_page_config(page_title="Social Trends", page_icon="📈", layout="wide")

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
        if st.button("Logout", key="logout_trends"):
            st.session_state.clear()
            st.switch_page("Home.py")
    else:
        if st.button("Login", key="login_trends"):
            st.switch_page("Home.py")

# Main content
st.title("📈 Social Trends")
st.write("Trending topics and community discussions")

# Trending topics
st.subheader("🔥 Trending Topics")
topics = ["Mining Updates", "Price Analysis", "Tech Developments", "Community Events"]
engagement = [1250, 890, 650, 420]

# Trending topics chart
fig = go.Figure(data=[
    go.Bar(x=topics, y=engagement, marker_color='#bcbd22')
])

fig.update_layout(
    title="Topic Engagement (Last 24h)",
    xaxis_title="Topics",
    yaxis_title="Engagement Score",
    height=400,
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

# Hashtag trends
st.subheader("#️⃣ Trending Hashtags")
col1, col2 = st.columns(2)

with col1:
    hashtag_data = {
        "Hashtag": ["#KaspaNetwork", "#BlockDAG", "#Mining", "#DeFi", "#Crypto"],
        "Mentions (24h)": [2341, 1876, 1234, 987, 654],
        "Growth": ["+15%", "+8%", "+22%", "-3%", "+5%"]
    }
    
    df_hashtags = pd.DataFrame(hashtag_data)
    st.dataframe(df_hashtags, use_container_width=True)

with col2:
    # Word cloud simulation
    st.markdown("""
    **Top Keywords:**
    - **BlockDAG** (trending up 🔥)
    - **Mining** (highly discussed)
    - **Decentralization** (community focus)
    - **Scalability** (technical interest)
    - **Innovation** (development buzz)
    """)

# Recent mentions
st.subheader("📢 Recent Mentions")
mentions_data = {
    "Platform": ["Twitter", "Reddit", "Discord", "Telegram"],
    "Mentions": [1540, 820, 450, 320],
    "Sentiment": ["Positive", "Neutral", "Positive", "Positive"],
    "Top Post": ["Price milestone reached!", "Technical discussion on DAG", "Community celebration", "News sharing"]
}

df_mentions = pd.DataFrame(mentions_data)
st.dataframe(df_mentions, use_container_width=True)

# Sentiment over time
st.subheader("😊 Sentiment Timeline")
dates = pd.date_range(start='2024-05-15', end='2024-06-01', freq='D')
sentiment_scores = np.random.normal(0.7, 0.1, len(dates))

sentiment_fig = go.Figure()
sentiment_fig.add_trace(go.Scatter(
    x=dates,
    y=sentiment_scores,
    mode='lines+markers',
    name='Daily Sentiment',
    line=dict(color='#ff7f0e', width=3)
))

sentiment_fig.update_layout(
    title="Community Sentiment (Past 2 Weeks)",
    xaxis_title="Date",
    yaxis_title="Sentiment Score (0-1)",
    height=300,
    template="plotly_white"
)

st.plotly_chart(sentiment_fig, use_container_width=True)

# Navigation
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("📱 Social Metrics", use_container_width=True):
        st.switch_page("pages/6_📱_Social_Metrics.py")
with col2:
    if st.button("💰 Market Data", use_container_width=True):
        st.switch_page("pages/3_💰_Spot_Price.py")
with col3:
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("Home.py")
