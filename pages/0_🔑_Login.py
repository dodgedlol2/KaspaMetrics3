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

# Check for password reset token in URL
query_params = st.query_params
reset_token = query_params.get("reset_token")

if reset_token:
    st.markdown("---")
    st.subheader("🔄 Reset Your Password")
    
    # Verify token
    user = db.verify_reset_token(reset_token)
    if user:
        st.success(f"✅ Token verified for {user['username']}!")
        
        with st.form("reset_password_form"):
            new_password = st.text_input("New Password", type="password", placeholder="Enter your new password")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your new password")
            reset_submit = st.form_submit_button("🔄 Reset Password", use_container_width=True)
            
            if reset_submit:
                if new_password and confirm_password:
                    if new_password == confirm_password:
                        if len(new_password) >= 6:
                            if db.reset_password(reset_token, new_password):
                                st.success("🎉 Password reset successfully!")
                                st.info("👆 You can now login with your new password")
                                st.balloons()
                                # Clear the URL parameter
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
    else:
        st.error("❌ Invalid or expired reset token")
        st.info("Please request a new password reset if needed.")
    
    st.markdown("---")

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
