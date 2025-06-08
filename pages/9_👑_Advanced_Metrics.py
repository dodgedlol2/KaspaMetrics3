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
    st.metric("Transaction Count", "45.2K", "+5.7
