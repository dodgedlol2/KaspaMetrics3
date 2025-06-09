import streamlit as st

# Page config MUST be first!
st.set_page_config(page_title="Account", page_icon="👤", layout="wide")

import sys
import os
from datetime import datetime

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

# Check if user is logged in
if not st.session_state.get('authentication_status'):
    st.warning("🔐 Please login to view your account")
    col1, col2, col3 = st.columns(3)
    with col2:
        if st.button("🔑 Go to Login", use_container_width=True):
            st.switch_page("pages/0_🔑_Login.py")
    st.stop()

# Get current user info
username = st.session_state.get('username')
user = db.get_user(username)

# Header
st.title("👤 Account Profile")
st.write(f"Manage your Kaspa Analytics account")

# Account overview
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📋 Account Information")
    
    # Account details in a nice format
    st.markdown(f"""
    **👤 Full Name:** {user['name']}  
    **🔑 Username:** {user['username']}  
    **📧 Email:** {user['email']}  
    **📅 Member Since:** {user.get('created_at', 'N/A')[:10] if user.get('created_at') else 'N/A'}  
    """)

with col2:
    # Account status
    if st.session_state.get('is_premium'):
        st.success("👑 **Premium Account**")
        
        # Subscription details
        expires_at = st.session_state.get('premium_expires_at')
        if expires_at:
            try:
                if isinstance(expires_at, str):
                    expiry_date = datetime.fromisoformat(expires_at.replace('Z', '+00:00'))
                else:
                    expiry_date = expires_at
                
                days_left = (expiry_date - datetime.now()).days
                
                if days_left > 0:
                    st.metric("📅 Days Remaining", f"{days_left} days")
                    st.metric("🗓️ Expires On", expiry_date.strftime('%Y-%m-%d'))
                    
                    # Progress bar
                    if days_left <= 7:
                        st.error(f"⚠️ Subscription expires in {days_left} days!")
                    elif days_left <= 30:
                        st.warning(f"⏰ Subscription expires in {days_left} days")
                else:
                    st.error("❌ Subscription has expired")
            except:
                st.info("✅ Premium Active")
        else:
            st.info("✅ Premium Active")
    else:
        st.info("🔓 **Free Account**")
        st.write("Upgrade to premium for advanced features")

# Subscription management
st.markdown("---")
st.subheader("💳 Subscription Management")

if st.session_state.get('is_premium'):
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("✅ **Current Plan: Premium**")
        st.write("• Advanced analytics")
        st.write("• AI-powered insights")
        st.write("• Custom alerts")
        st.write("• Data export")
        st.write("• Priority support")
        
        # Show subscription status
        if user.get('subscription_cancelled', False):
            st.warning("⚠️ **Subscription Cancelled**")
            st.write("Your subscription has been cancelled but you'll keep premium access until your billing period ends.")
            
            # Show expiry information
            expires_at = st.session_state.get('premium_expires_at')
            if expires_at:
                try:
                    if isinstance(expires_at, str):
                        expiry_date = datetime.fromisoformat(expires_at.replace('Z', '+00:00'))
                    else:
                        expiry_date = expires_at
                    days_left = (expiry_date - datetime.now()).days
                    if days_left > 0:
                        st.info(f"🗓️ Premium access expires in **{days_left} days** ({expiry_date.strftime('%Y-%m-%d')})")
                    else:
                        st.error("❌ Premium access has expired")
                except:
                    st.info("✅ Premium access active until expiry")
        else:
            st.info("💡 **Subscription Active**")
            st.write("Your premium subscription is currently active and will auto-renew.")
    
    with col2:
        # Only show cancellation option if not already cancelled
        if not user.get('subscription_cancelled', False):
            st.warning("⚠️ **Cancel Subscription**")
            st.write("Cancel your subscription (you'll keep access until current period ends).")
            
            # Cancellation confirmation
            if st.button("❌ Cancel My Subscription", use_container_width=True, type="secondary"):
                st.session_state['show_cancel_confirmation'] = True
            
            # Show confirmation dialog
            if st.session_state.get('show_cancel_confirmation'):
                st.error("🚨 **Are you sure you want to cancel?**")
                st.write("This action cannot be undone. You will:")
                st.write("• ❌ Stop future billing")
                st.write("• ✅ Keep premium access until period ends")
                st.write("• ✅ Keep your account and free features")
                
                col_cancel, col_keep = st.columns(2)
                with col_cancel:
                    if st.button("🗑️ Yes, Cancel Subscription", use_container_width=True, type="primary"):
                        # Process cancellation
                        success, message = db.cancel_premium_subscription(username)
                        
                        if success:
                            # Clear confirmation dialog
                            st.session_state.pop('show_cancel_confirmation', None)
                            
                            # Send cancellation email
                            try:
                                email_handler.send_cancellation_email(user['email'], user['name'])
                                st.success(f"✅ {message}")
                                st.success("📧 Cancellation confirmation email sent!")
                                st.info("⚠️ You'll keep premium access until your current billing period ends.")
                            except Exception as e:
                                st.success(f"✅ {message}")
                                st.warning("⚠️ Could not send confirmation email, but cancellation was processed.")
                            
                            st.balloons()
                            st.rerun()
                        else:
                            st.error(f"❌ {message}")
                
                with col_keep:
                    if st.button("💙 Keep My Subscription", use_container_width=True):
                        st.session_state.pop('show_cancel_confirmation', None)
                        st.success("😊 Great choice! Your subscription remains active.")
                        st.rerun()
        else:
            # Already cancelled - show reactivation option
            st.info("🔄 **Reactivate Subscription**")
            st.write("Your subscription is cancelled but you still have premium access.")
            st.write("Want to reactivate? Subscribe again to continue after expiry.")
            
            col_monthly, col_annual = st.columns(2)
            with col_monthly:
                if st.button("💳 Monthly ($9.99)", use_container_width=True):
                    st.session_state['selected_plan'] = {'amount': 999, 'interval': 'month'}
                    payment_url = payment_handler.create_checkout_session(username)
                    if payment_url:
                        st.markdown(f"[💳 Complete Payment]({payment_url})")
            
            with col_annual:
                if st.button("💳 Annual ($99)", use_container_width=True):
                    st.session_state['selected_plan'] = {'amount': 9900, 'interval': 'year'}
                    payment_url = payment_handler.create_checkout_session(username)
                    if payment_url:
                        st.markdown(f"[💳 Complete Payment]({payment_url})")

else:
    # Upgrade options for free users
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 💎 Upgrade to Premium")
        st.success("**Monthly Plan - $9.99/month**")
        st.write("• All premium features")
        st.write("• Cancel anytime")
        st.write("• Instant access")
        
        if st.button("💳 Upgrade Monthly", key="upgrade_monthly", use_container_width=True):
            st.session_state['selected_plan'] = {'amount': 999, 'interval': 'month'}
            payment_url = payment_handler.create_checkout_session(username)
            if payment_url:
                st.markdown(f"[💳 Complete Payment]({payment_url})")
    
    with col2:
        st.markdown("### 💎 Best Value")
        st.success("**Annual Plan - $99/year**")
        st.write("• All premium features")  
        st.write("• 2 months free!")
        st.write("• Best value option")
        
        if st.button("💳 Upgrade Annually", key="upgrade_annual", use_container_width=True):
            st.session_state['selected_plan'] = {'amount': 9900, 'interval': 'year'}
            payment_url = payment_handler.create_checkout_session(username)
            if payment_url:
                st.markdown(f"[💳 Complete Payment]({payment_url})")

# Account actions
st.markdown("---")
st.subheader("⚙️ Account Actions")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🔄 Account Settings")
    if st.button("🔑 Change Password", use_container_width=True):
        st.info("🚧 Password change feature coming soon!")
    
    if st.button("📧 Update Email", use_container_width=True):
        st.info("🚧 Email update feature coming soon!")

with col2:
    st.markdown("### 📊 Usage Statistics")
    st.metric("📈 Pages Viewed", "47")
    st.metric("📅 Last Login", "Today")
    st.metric("🎯 Favorite Section", "Mining")

with col3:
    st.markdown("### 🚪 Account Management")
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.clear()
        st.success("👋 Logged out successfully!")
        st.switch_page("Home.py")
    
    if st.button("❌ Delete Account", use_container_width=True):
        st.error("Please contact support to delete your account.")

# Quick navigation
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("Home.py")
with col2:
    if st.button("👑 Premium Features", use_container_width=True):
        st.switch_page("pages/B_👑_Premium_Features.py")
with col3:
    if st.button("📊 Analytics", use_container_width=True):
        st.switch_page("pages/1_⛏️_Mining_Hashrate.py")
