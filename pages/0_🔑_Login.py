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
from email_handler import EmailHandler
from navigation import add_navigation

# Add shared navigation to sidebar
add_navigation()

# Initialize handlers
@st.cache_resource
def init_handlers():
    db = Database()
    auth_handler = AuthHandler(db)
    payment_handler = PaymentHandler()
    email_handler = EmailHandler()
    return db, auth_handler, payment_handler, email_handler

db, auth_handler, payment_handler, email_handler = init_handlers()

# ✅ NEW: Check for persistent login cookie before showing login form
if not st.session_state.get('authentication_status'):
    if auth_handler.check_persistent_login():
        st.success("🔐 **Welcome back!** Auto-logged in from saved session.")
        st.info("Redirecting to home page...")
        st.switch_page("Home.py")

# Check for password reset token in URL - Multiple ways to get it
query_params = st.query_params
reset_token = None

# Try different ways to get the reset token
if hasattr(query_params, 'get'):
    if isinstance(query_params.get("reset_token"), list):
        reset_token = query_params.get("reset_token")[0] if query_params.get("reset_token") else None
    else:
        reset_token = query_params.get("reset_token")

# Also try accessing it directly from the URL
if not reset_token:
    try:
        for key, value in st.query_params.items():
            if key == "reset_token":
                reset_token = value
                break
    except:
        pass

# Debug: Show what we found
if reset_token:
    st.write(f"Debug: Found reset token: {reset_token[:10]}...")

if reset_token:
    st.title("🔄 Reset Your Password")
    st.info("You've been redirected from a password reset email. Please set your new password below.")
    
    # Verify token
    user = db.verify_reset_token(reset_token)
    if user:
        st.success(f"✅ Token verified for {user['username']}!")
        
        with st.form("reset_password_form"):
            st.write("**Set your new password:**")
            new_password = st.text_input("New Password", type="password", placeholder="Enter your new password (min 6 characters)")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your new password")
            reset_submit = st.form_submit_button("🔄 Reset Password", use_container_width=True)
            
            if reset_submit:
                if new_password and confirm_password:
                    if new_password == confirm_password:
                        if len(new_password) >= 6:
                            if db.reset_password(reset_token, new_password):
                                st.success("🎉 Password reset successfully!")
                                st.info("👆 You can now login with your new password using the form below")
                                st.balloons()
                                # Clear the reset token
                                st.query_params.clear()
                                st.rerun()
                            else:
                                st.error("❌ Failed to reset password. Please try again.")
                        else:
                            st.error("⚠️ Password must be at least 6 characters long")
                    else:
                        st.error("⚠️ Passwords do not match")
                else:
                    st.error("⚠️ Please fill in both password fields")
        
        # Add option to go back if needed
        if st.button("← Back to Home", key="back_to_home"):
            st.query_params.clear()
            st.switch_page("Home.py")
            
    else:
        st.error("❌ Invalid or expired reset token")
        st.info("The reset token may have expired (valid for 1 hour) or is invalid.")
        st.write("Please request a new password reset if needed.")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Request New Reset", use_container_width=True):
                st.query_params.clear()
                st.rerun()
        with col2:
            if st.button("🏠 Go Home", use_container_width=True):
                st.query_params.clear()
                st.switch_page("Home.py")
    
    st.markdown("---")
    st.markdown("### 🔐 Or Login with Existing Credentials")

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
            # ✅ MODIFIED: Use enhanced logout that clears cookies too
            auth_handler.logout()
            st.success("✅ **Logged out successfully!**")
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
        
        # ✅ NEW: Add remember me checkbox
        remember_me = st.checkbox("🔐 **Remember me** (stay logged in for 30 days)", value=True)
        
        col_login, col_demo = st.columns(2)
        with col_login:
            login_button = st.form_submit_button("🔑 Sign In", use_container_width=True)
        with col_demo:
            demo_button = st.form_submit_button("🎮 Demo", use_container_width=True)
        
        if login_button:
            if username and password:
                # ✅ MODIFIED: Use enhanced login with remember me
                if auth_handler.login_user(username, password, remember_me):
                    user = db.get_user(username)
                    st.success(f"✅ Welcome back, {user['name']}!")
                    
                    if remember_me:
                        st.info("🔐 **Remember me enabled** - You'll stay logged in for 30 days")
                    
                    st.balloons()
                    st.switch_page("Home.py")
                else:
                    st.error("❌ Invalid username or password")
            else:
                st.error("⚠️ Please enter both username and password")
        
        if demo_button:
            # ✅ MODIFIED: Use enhanced login for demo with remember me
            if auth_handler.login_user("demo_user", "demo123", remember_me):
                st.success("🎮 Logged in as Demo User!")
                
                if remember_me:
                    st.info("🔐 **Remember me enabled** - You'll stay logged in for 30 days")
                
                st.switch_page("Home.py")
    
    # Forgot Password Section
    st.markdown("---")
    with st.expander("🔒 Forgot Password?", expanded=False):
        st.write("Enter your email address to receive a password reset link.")
        
        with st.form("forgot_password_form"):
            reset_email = st.text_input("Email Address", placeholder="Enter your registered email")
            forgot_submit = st.form_submit_button("📧 Send Reset Link", use_container_width=True)
            
            if forgot_submit:
                if reset_email:
                    # Check if email exists
                    user = db.get_user_by_email(reset_email)
                    if user:
                        # Create reset token
                        token = db.create_reset_token(reset_email)
                        if token:
                            # Send email
                            if email_handler.send_password_reset_email(reset_email, token, user['username']):
                                st.success("📧 Password reset email sent!")
                                st.info("Check your inbox for the reset link. The link expires in 1 hour.")
                            else:
                                st.error("❌ Failed to send email. Please try again.")
                        else:
                            st.error("❌ Failed to create reset token. Please try again.")
                    else:
                        # Don't reveal if email exists or not for security
                        st.success("📧 If that email exists in our system, a reset link has been sent.")
                        st.info("Check your inbox for the reset link.")
                else:
                    st.error("⚠️ Please enter your email address")

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
                if len(new_password) >= 6:
                    if db.add_user(new_username, new_email, new_password, new_name):
                        st.success("🎉 Account created successfully!")
                        st.info("👆 Please sign in using the form on the left")
                        st.balloons()
                        
                        # Send welcome email to new user
                        try:
                            email_handler.send_welcome_email(new_email, new_name)
                            st.success("📧 Welcome email sent! Check your inbox.")
                        except Exception as e:
                            st.warning("⚠️ Account created but welcome email could not be sent.")
                            st.write(f"Debug: Email error - {e}")
                        
                        # ✅ NEW: Auto-login new user with remember me enabled
                        if auth_handler.login_user(new_username, new_password, True):
                            st.success("🔐 **Auto-logged in with persistent session!**")
                            st.switch_page("Home.py")
                        
                    else:
                        st.error("❌ Username or email already exists")
                else:
                    st.error("⚠️ Password must be at least 6 characters long")
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
