import streamlit as st
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from database import Database
from auth_handler import AuthHandler
from payment_handler import PaymentHandler
import importlib.util
import sys
import os

# Page configuration
st.set_page_config(
    page_title="Kaspa Analytics",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database and handlers
@st.cache_resource
def init_app():
    db = Database()
    auth_handler = AuthHandler(db)
    payment_handler = PaymentHandler()
    return db, auth_handler, payment_handler

db, auth_handler, payment_handler = init_app()

# Check for payment success in URL parameters
query_params = st.query_params
if query_params.get("upgrade") == "success" and query_params.get("session_id"):
    session_id = query_params.get("session_id")
    
    # Try to get username from Stripe session metadata
    try:
        import stripe
        stripe.api_key = payment_handler.stripe_secret_key
        stripe_session = stripe.checkout.Session.retrieve(session_id)
        username_from_stripe = stripe_session.metadata.get('username')
        
        if username_from_stripe:
            # Upgrade the user in database
            payment_result = payment_handler.handle_successful_payment(session_id, username_from_stripe)
            if payment_result.get('success'):
                expires_at = payment_result.get('expires_at')
                subscription_id = payment_result.get('subscription_id')
                
                db.update_premium_status(username_from_stripe, True, expires_at, subscription_id)
                
                # Auto-login the user if they're not logged in
                if not st.session_state.get('authentication_status'):
                    st.session_state['authentication_status'] = True
                    st.session_state['username'] = username_from_stripe
                    user = db.get_user(username_from_stripe)
                    st.session_state['name'] = user['name']
                    st.session_state['is_premium'] = True
                    st.session_state['premium_expires_at'] = expires_at
                    
                st.success("🎉 Payment successful! You now have premium access!")
                st.balloons()
                
                # Clear URL parameters
                st.query_params.clear()
                # Force a rerun to update the UI
                st.rerun()
            else:
                st.error("Payment verification failed. Please contact support.")
        else:
            st.error("Could not identify user from payment. Please contact support.")
            
    except Exception as e:
        st.error(f"Error processing upgrade: {str(e)}")

elif query_params.get("upgrade") == "cancelled":
    st.warning("Payment was cancelled. You can try again anytime!")
    # Clear URL parameters
    if st.button("Continue"):
        st.query_params.clear()
        st.rerun()

# Custom CSS for better styling
st.markdown("""
<style>
.main-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 0;
    border-bottom: 1px solid #e0e0e0;
    margin-bottom: 20px;
}
.logo {
    font-size: 24px;
    font-weight: bold;
    color: #1f77b4;
}
.auth-buttons {
    display: flex;
    gap: 10px;
}
</style>
""", unsafe_allow_html=True)

# Header with logo and auth buttons
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown('<div class="logo">⚡ Kaspa Analytics</div>', unsafe_allow_html=True)

# Authentication logic
if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = None
    st.session_state['username'] = None
    st.session_state['name'] = None

# Login/Register form in header
with col2:
    if st.session_state['authentication_status'] is None:
        with st.expander("Login / Register"):
            tab1, tab2 = st.tabs(["Login", "Register"])
            
            with tab1:
                with st.form("login_form"):
                    username = st.text_input("Username")
                    password = st.text_input("Password", type="password")
                    login_button = st.form_submit_button("Login")
                    
                    if login_button:
                        if auth_handler.authenticate(username, password):
                            user = db.get_user(username)
                            
                            # Check premium expiration
                            is_premium, expiry_info = db.check_premium_expiration(username)
                            
                            st.session_state['authentication_status'] = True
                            st.session_state['username'] = username
                            st.session_state['name'] = user['name']
                            st.session_state['is_premium'] = is_premium
                            st.session_state['premium_expires_at'] = user.get('premium_expires_at')
                            
                            st.rerun()
                        else:
                            st.error("Invalid username or password")
            
            with tab2:
                with st.form("register_form"):
                    new_username = st.text_input("Username", key="reg_username")
                    new_email = st.text_input("Email", key="reg_email")
                    new_name = st.text_input("Full Name", key="reg_name")
                    new_password = st.text_input("Password", type="password", key="reg_password")
                    register_button = st.form_submit_button("Register")
                    
                    if register_button:
                        if db.add_user(new_username, new_email, new_password, new_name):
                            st.success("Account created successfully! Please login.")
                        else:
                            st.error("Username or email already exists")
    
    elif st.session_state['authentication_status']:
        # Check for expired premium subscriptions
        if st.session_state.get('username'):
            is_premium, expiry_info = db.check_premium_expiration(st.session_state['username'])
            st.session_state['is_premium'] = is_premium
            
            if isinstance(expiry_info, str) and expiry_info == "Subscription expired":
                st.warning("⚠️ Your premium subscription has expired. Please renew to continue accessing premium features.")
        
        # Show user info with premium status
        col1, col2 = st.columns([3, 1])
        with col1:
            welcome_msg = f"Welcome, {st.session_state['name']}!"
            if st.session_state.get('is_premium'):
                welcome_msg += " 👑 PREMIUM"
                if st.session_state.get('premium_expires_at'):
                    from datetime import datetime
                    try:
                        expires = datetime.fromisoformat(st.session_state['premium_expires_at'].replace('Z', '+00:00'))
                        days_left = (expires - datetime.now()).days
                        if days_left > 0:
                            welcome_msg += f" ({days_left} days left)"
                    except:
                        pass
            st.write(welcome_msg)
        with col2:
            if st.button("Logout"):
                st.session_state['authentication_status'] = None
                st.session_state['username'] = None
                st.session_state['name'] = None
                st.session_state['is_premium'] = False
                st.session_state['premium_expires_at'] = None
                st.rerun()

# Main content
st.title("⚡ Welcome to Kaspa Analytics")
st.write("Your comprehensive platform for Kaspa blockchain analytics and insights.")

# Quick stats cards
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Current Price", "$0.125", "+2.4%")
with col2:
    st.metric("Market Cap", "$3.1B", "+1.8%")
with col3:
    st.metric("24h Volume", "$45M", "-5.2%")
with col4:
    st.metric("Hashrate", "1.2 EH/s", "+0.8%")

# Navigation sections
st.subheader("📊 Analytics Sections")

# Free sections
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### ⛏️ Mining Analytics")
    st.write("Network hashrate, difficulty, and mining metrics")
    if st.button("📈 View Mining Data", use_container_width=True):
        st.switch_page("pages/1_⛏️_Mining_Hashrate.py")

with col2:
    st.markdown("### 💰 Spot Market")
    st.write("Price tracking, volume analysis, and market cap data")
    if st.button("💵 View Market Data", use_container_width=True):
        st.switch_page("pages/3_💰_Spot_Price.py")

with col3:
    st.markdown("### 📱 Social Data")
    st.write("Community metrics and social sentiment analysis")
    if st.button("📊 View Social Data", use_container_width=True):
        st.switch_page("pages/6_📱_Social_Metrics.py")

# Premium section
st.subheader("👑 Premium Features")

if not st.session_state.get('authentication_status'):
    st.info("🔐 **Login required** to access premium analytics features")
    
elif not st.session_state.get('is_premium', False):
    st.warning("🔒 **Premium subscription required** for advanced analytics")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("#### 💎 Premium Benefits")
        st.write("• Advanced on-chain analytics")
        st.write("• Real-time alerts and notifications") 
        st.write("• Custom data exports")
        st.write("• Priority customer support")
        
    with col2:
        st.markdown("#### 💳 Monthly Plan")
        st.write("**$9.99/month**")
        st.write("• All premium features")
        st.write("• Cancel anytime")
        if st.button("Subscribe Monthly", key="home_monthly", use_container_width=True):
            st.session_state['selected_plan'] = {'amount': 999, 'interval': 'month'}
            payment_url = payment_handler.create_checkout_session(st.session_state['username'])
            if payment_url:
                st.markdown(f"[💳 Complete Payment]({payment_url})")
                
    with col3:
        st.markdown("#### 💳 Annual Plan")
        st.write("**$99/year** *(Save 17%)*")
        st.write("• All premium features")
        st.write("• 2 months free")
        if st.button("Subscribe Annually", key="home_annual", use_container_width=True):
            st.session_state['selected_plan'] = {'amount': 9900, 'interval': 'year'}
            payment_url = payment_handler.create_checkout_session(st.session_state['username'])
            if payment_url:
                st.markdown(f"[💳 Complete Payment]({payment_url})")
else:
    st.success("🎉 **You have premium access!** Explore all advanced analytics features.")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔬 Premium Analytics")
        st.write("Advanced metrics and AI-powered insights")
        if st.button("🚀 Launch Premium Analytics", use_container_width=True):
            st.switch_page("pages/8_👑_Premium_Analytics.py")
            
    with col2:
        st.markdown("### 📊 Advanced Metrics")
        st.write("Custom indicators and correlation analysis")
        if st.button("📈 View Advanced Metrics", use_container_width=True):
            st.switch_page("pages/9_👑_Advanced_Metrics.py")

# Footer
st.markdown("---")
st.markdown("### 🚀 Getting Started")
st.write("**New to Kaspa Analytics?** Start with our mining data to understand network health, then explore market metrics and social sentiment. Premium users get access to advanced analytics and custom alerts.")

# Sidebar info
with st.sidebar:
    st.markdown("### ℹ️ Quick Info")
    st.info("Use the navigation above or pages in the sidebar to explore different analytics sections.")
    
    if st.session_state.get('is_premium'):
        st.success("👑 Premium Active")
        if st.session_state.get('premium_expires_at'):
            st.write(f"Expires: {st.session_state['premium_expires_at'][:10]}")
    elif st.session_state.get('authentication_status'):
        st.warning("🔒 Free Account")
        st.write("Upgrade for premium features")
    else:
        st.info("🔐 Not Logged In")
        st.write("Login for full access")
