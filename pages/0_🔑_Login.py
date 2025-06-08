import streamlit as st

# Page config MUST be first!
st.set_page_config(page_title="Login", page_icon="🔑", layout="wide")

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

# Check if already logged in
if st.session_state.get('authentication_status'):
    st.success(f"✅ Already logged in as {st.session_state.get('name', 'User')}")
    if st.session_state.get('is_premium'):
        st.success("👑 You have premium access!")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🏠 Go to Home", use_container_width=True):
            st.switch_page("Home.py")
    with col2:
        if st.button("👤 View Profile", use_container_width=True):
            st.switch_page("pages/A_👤_Account.py")
    with col3:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.clear()
            st.rerun()
    st.stop()

# Header
st.title("🔑 Login to Kaspa Analytics")
st.write("Access your analytics dashboard and premium features")

# Create two columns for login and register
col1, col2 = st.columns(2, gap="large")

with col1:
    st.subheader("🔐 Sign In")
    with st.form("login_form"):
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        col_login, col_demo = st.columns(2)
        with col_login:
            login_button = st.form_submit_button("🔑 Sign In", use_container_width=True)
        with col_demo:
            demo_button = st.form_submit_button("🎮 Demo", use_container_width=True)
        
        if login_button:
            if username and password:
                if auth_handler.authenticate(username, password):
                    user = db.get_user(username)
                    is_premium, expiry_info = db.check_premium_expiration(username)
                    
                    st.session_state['authentication_status'] = True
                    st.session_state['username'] = username
                    st.session_state['name'] = user['name']
                    st.session_state['is_premium'] = is_premium
                    st.session_state['premium_expires_at'] = user.get('premium_expires_at')
                    
                    st.success(f"✅ Welcome back, {user['name']}!")
                    st.balloons()
                    st.switch_page("Home.py")
                else:
                    st.error("❌ Invalid username or password")
            else:
                st.error("⚠️ Please enter both username and password")
        
        if demo_button:
            if auth_handler.authenticate("demo_user", "demo123"):
                user = db.get_user("demo_user")
                is_premium, expiry_info = db.check_premium_expiration("demo_user")
                
                st.session_state['authentication_status'] = True
                st.session_state['username'] = "demo_user"
                st.session_state['name'] = user['name']
                st.session_state['is_premium'] = is_premium
                st.session_state['premium_expires_at'] = user.get('premium_expires_at')
                
                st.success("🎮 Logged in as Demo User!")
                st.switch_page("Home.py")

with col2:
    st.subheader("📝 Create Account")
    with st.form("register_form"):
        new_username = st.text_input("Username", placeholder="Choose a username")
        new_email = st.text_input("Email", placeholder="Enter your email")
        new_name = st.text_input("Full Name", placeholder="Enter your full name")
        new_password = st.text_input("Password", type="password", placeholder="Choose a password")
        register_button = st.form_submit_button("📝 Create Account", use_container_width=True)
        
        if register_button:
            if new_username and new_email and new_name and new_password:
                if db.add_user(new_username, new_email, new_password, new_name):
                    st.success("🎉 Account created successfully!")
                    st.info("👆 Please sign in using the form on the left")
                    st.balloons()
                else:
                    st.error("❌ Username or email already exists")
            else:
                st.error("⚠️ Please fill in all fields")

# Demo accounts info
st.markdown("---")
st.subheader("🎮 Demo Accounts")
col1, col2 = st.columns(2)
with col1:
    st.info("""
    **Free Demo Account:**
    - Username: `demo_user`
    - Password: `demo123`
    - Access: All free features
    """)
with col2:
    st.success("""
    **Premium Demo Account:**
    - Username: `premium_user`
    - Password: `demo123`
    - Access: All premium features
    """)

# Quick navigation
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🏠 Back to Home", use_container_width=True):
        st.switch_page("Home.py")
with col2:
    if st.button("👑 View Premium Features", use_container_width=True):
        st.switch_page("pages/B_👑_Premium_Features.py")
with col3:
    if st.button("📊 Browse Analytics", use_container_width=True):
        st.switch_page("pages/1_⛏️_Mining_Hashrate.py")
