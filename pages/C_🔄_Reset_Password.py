import streamlit as st

# Page config MUST be first!
st.set_page_config(page_title="Reset Password", page_icon="🔄", layout="wide")

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

# Get reset token from URL parameters
query_params = st.query_params
reset_token = None

# Try different ways to get the reset token
if hasattr(query_params, 'get'):
    if isinstance(query_params.get("reset_token"), list):
        reset_token = query_params.get("reset_token")[0] if query_params.get("reset_token") else None
    else:
        reset_token = query_params.get("reset_token")

# Also try direct access
if not reset_token:
    for key, value in st.query_params.items():
        if key == "reset_token":
            reset_token = value
            break

# Main page content
if reset_token:
    st.title("🔄 Reset Your Password")
    st.write("You've clicked a password reset link from your email. Please set your new password below.")
    
    # Verify token
    user = db.verify_reset_token(reset_token)
    if user:
        st.success(f"✅ Password reset verified for **{user['username']}**")
        
        # Password reset form
        with st.form("reset_password_form", clear_on_submit=True):
            st.subheader("🔐 Set Your New Password")
            
            col1, col2 = st.columns(2)
            
            with col1:
                new_password = st.text_input(
                    "New Password", 
                    type="password", 
                    placeholder="Enter your new password",
                    help="Password must be at least 6 characters long"
                )
            
            with col2:
                confirm_password = st.text_input(
                    "Confirm Password", 
                    type="password", 
                    placeholder="Confirm your new password"
                )
            
            st.markdown("### 🛡️ Password Requirements")
            st.info("""
            • **Minimum 6 characters** (recommended: 8+ characters)
            • Use a mix of letters, numbers, and symbols
            • Don't reuse passwords from other accounts
            • Make it unique and memorable
            """)
            
            reset_submit = st.form_submit_button("🔄 Reset My Password", use_container_width=True, type="primary")
            
            if reset_submit:
                if new_password and confirm_password:
                    if new_password == confirm_password:
                        if len(new_password) >= 6:
                            if db.reset_password(reset_token, new_password):
                                st.success("🎉 **Password Reset Successful!**")
                                st.balloons()
                                
                                # Clear URL parameters
                                st.query_params.clear()
                                
                                # Set a session state flag to show success outside the form
                                st.session_state['password_reset_success'] = True
                                st.rerun()
                                
                            else:
                                st.error("❌ Failed to reset password. Please try again or contact support.")
                        else:
                            st.error("⚠️ Password must be at least 6 characters long")
                    else:
                        st.error("⚠️ Passwords do not match. Please try again.")
                else:
                    st.error("⚠️ Please fill in both password fields")
        
        # Show success message and navigation OUTSIDE the form
        if st.session_state.get('password_reset_success'):
            st.markdown("---")
            st.subheader("✅ What's Next?")
            st.write("Your password has been successfully updated. You can now login with your new credentials.")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("🔑 Go to Login", use_container_width=True, type="primary"):
                    st.session_state.pop('password_reset_success', None)  # Clear the flag
                    st.switch_page("pages/0_🔑_Login.py")
            with col2:
                if st.button("🏠 Go to Home", use_container_width=True):
                    st.session_state.pop('password_reset_success', None)  # Clear the flag
                    st.switch_page("Home.py")
            with col3:
                if st.button("📊 Browse Analytics", use_container_width=True):
                    st.session_state.pop('password_reset_success', None)  # Clear the flag
                    st.switch_page("pages/1_⛏️_Mining_Hashrate.py")
        
        # Security information
        st.markdown("---")
        st.subheader("🔒 Security Information")
        col1, col2 = st.columns(2)
        
        with col1:
            st.info("""
            **🛡️ Your Security Matters**
            
            • This reset link expires in 1 hour
            • The link can only be used once
            • Your old password is now invalid
            • We never store passwords in plain text
            """)
        
        with col2:
            st.warning("""
            **⚠️ Need Help?**
            
            • Contact: support@kaspaanalytics.com
            • Include your username in any support requests
            • Never share your password with anyone
            • Report suspicious activity immediately
            """)
        
    else:
        # Invalid or expired token
        st.error("❌ **Invalid or Expired Reset Link**")
        st.write("This password reset link is either invalid or has expired.")
        
        st.markdown("### 🤔 What happened?")
        st.info("""
        **Possible reasons:**
        • The reset link is older than 1 hour (expired)
        • The link has already been used
        • The link was copied incorrectly
        • The reset request was cancelled
        """)
        
        st.markdown("### 🔄 What can you do?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📧 Request New Reset", use_container_width=True, type="primary"):
                st.switch_page("pages/0_🔑_Login.py")
        with col2:
            if st.button("🏠 Back to Home", use_container_width=True):
                st.switch_page("Home.py")

else:
    # No reset token in URL
    st.title("🔄 Password Reset")
    st.warning("⚠️ **No Reset Token Found**")
    st.write("This page is for resetting passwords using a reset link from your email.")
    
    st.markdown("### 🔑 How to reset your password:")
    st.info("""
    1. **Go to the login page**
    2. **Click "Forgot Password?"**
    3. **Enter your email address**
    4. **Check your email** for the reset link
    5. **Click the link** in the email to return here
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔑 Go to Login Page", use_container_width=True, type="primary"):
            st.switch_page("pages/0_🔑_Login.py")
    with col2:
        if st.button("🏠 Back to Home", use_container_width=True):
            st.switch_page("Home.py")

# Quick navigation
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("Home.py")
with col2:
    if st.button("🔑 Login", use_container_width=True):
        st.switch_page("pages/0_🔑_Login.py")
with col3:
    if st.button("👑 Premium Features", use_container_width=True):
        st.switch_page("pages/B_👑_Premium_Features.py")
