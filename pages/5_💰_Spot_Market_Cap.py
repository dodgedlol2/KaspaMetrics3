import streamlit as st
# Page config MUST be first!
st.set_page_config(page_title="Market Cap", page_icon="🏦", layout="wide")
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
        if st.button("Logout", key="logout_marketcap"):
            st.session_state.clear()
            st.switch_page("Home.py")
    else:
        if st.button("Login", key="login_marketcap"):
            st.switch_page("Home.py")

# Main content
st.title("🏦 Market Capitalization")
st.write("Kaspa market cap and ranking metrics")

# Sample market cap data
dates = pd.date_range(start='2024-01-01', end='2024-06-01', freq='D')
mcap_data = np.random.normal(3100000000, 200000000, len(dates))

# Current metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Market Cap", "$3.14B", "+1.8%")
with col2:
    st.metric("Rank", "#32", "↑2")
with col3:
    st.metric("Circulating Supply", "25.2B KAS", "")
with col4:
    st.metric("Max Supply", "28.7B KAS", "")

# Market cap chart with gradient fill
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=dates,
    y=mcap_data,
    mode='lines',
    name='Market Cap',
    line=dict(color='#9467bd', width=2),
    fill='tozeroy',
    fillgradient=dict(
        type="vertical",
        colorscale=[
            [0, "rgba(148, 103, 189, 0.8)"],  # Top: more opaque purple
            [1, "rgba(148, 103, 189, 0.1)"]   # Bottom: more transparent
        ]
    )
))

fig.update_layout(
    title="Market Capitalization Over Time",
    xaxis_title="Date",
    yaxis_title="Market Cap (USD)",
    height=400,
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

# Supply metrics
st.subheader("📊 Supply Analysis")
col1, col2 = st.columns(2)
with col1:
    # Supply distribution pie chart
    supply_labels = ['Circulating', 'Remaining']
    supply_values = [25.2, 3.5]
    
    supply_fig = go.Figure(data=[go.Pie(labels=supply_labels, values=supply_values)])
    supply_fig.update_layout(title="Token Supply Distribution")
    st.plotly_chart(supply_fig, use_container_width=True)

with col2:
    st.markdown("""
    **Supply Metrics:**
    - 87.8% of max supply already circulating
    - Emission rate decreasing over time
    - No inflation concerns unlike PoS chains
    - Fair launch with no pre-mine
    """)

# Market comparison
st.subheader("📈 Market Position")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("vs Bitcoin", "0.0065%", "Market cap ratio")
with col2:
    st.metric("vs Ethereum", "0.087%", "Market cap ratio")
with col3:
    st.metric("PoW Rank", "#4", "Among PoW coins")

# Navigation
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("💵 Price", use_container_width=True):
        st.switch_page("pages/3_💰_Spot_Price.py")
with col2:
    if st.button("📊 Volume", use_container_width=True):
        st.switch_page("pages/4_💰_Spot_Volume.py")
with col3:
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("Home.py")
