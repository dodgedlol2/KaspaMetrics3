import streamlit as st
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from database import Database
from auth_handler import AuthHandler
from payment_handler import PaymentHandler
from email_handler import EmailHandler
from navigation import add_navigation  # ← MAKE SURE THIS LINE EXISTS
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
    email_handler = EmailHandler()
    return db, auth_handler, payment_handler, email_handler

db, auth_handler, payment_handler, email_handler = init_app()

# Add shared navigation to sidebar
add_navigation()

# Check for password reset token in URL and redirect to login page
query_params = st.query_params
reset_token = query_params.get("reset_token", [None])[0] if isinstance(query_params.get("reset_token"), list) else query_params.get("reset_token")

if reset_token:
    st.info("🔄 **Password Reset Detected** - Redirecting you to the login page...")
    st.write("You clicked a password reset link. Redirecting you to complete the password reset...")
    
    # Show the reset link for manual navigation if auto-redirect doesn't work
    reset_login_url = f"https://kaspametrics3test1.streamlit.app/Login?reset_token={reset_token}"
    st.markdown(f"If you're not automatically redirected, [click here to reset your password]({reset_login_url})")
    
    # Auto-redirect using JavaScript
    st.markdown(f"""
    <script>
    window.location.href = "/Login?reset_token={reset_token}";
    </script>
    """, unsafe_allow_html=True)
    
    # Streamlit native redirect (backup)
    st.switch_page(f"pages/0_🔑_Login.py")

# Check for payment success in URL parameters
if query_params.get("upgrade") == "success" and query_params.get("session_id"):
    session_id = query_params.get("session_id")
    
    # Show big success message at the top
    st.success("🎉 **PAYMENT SUCCESSFUL!** Welcome to Kaspa Analytics Premium!")
    st.balloons()
    
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
                
                # Update session state for already logged in users
                st.session_state['is_premium'] = True
                st.session_state['premium_expires_at'] = expires_at
                
                # Send premium subscription email
                try:
                    user = db.get_user(username_from_stripe)
                    if user:
                        # Determine plan type based on amount
                        amount = payment_result.get('amount', 0)
                        plan_type = "Monthly Premium" if amount == 999 else "Annual Premium"
                        email_handler.send_premium_subscription_email(user['email'], user['name'], plan_type)
                        st.info("📧 Premium welcome email sent to your inbox!")
                except Exception as e:
                    st.write(f"Debug: Could not send premium email: {e}")
                
                # Show premium access confirmation
                st.info("✅ **Your account has been upgraded to Premium!** You now have access to all advanced analytics features.")
                
                # Add button to explore premium features
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("🔬 Explore Premium Analytics", use_container_width=True):
                        st.switch_page("pages/8_👑_Premium_Analytics.py")
                with col2:
                    if st.button("📊 View Advanced Metrics", use_container_width=True):
                        st.switch_page("pages/9_👑_Advanced_Metrics.py")
                with col3:
                    if st.button("🏠 Continue to Home", use_container_width=True):
                        st.query_params.clear()
                        st.rerun()
                
                # Clear URL parameters after a delay
                if st.button("Close Success Message"):
                    st.query_params.clear()
                    st.rerun()
            else:
                st.error("Payment verification failed. Please contact support.")
        else:
            st.error("Could not identify user from payment. Please contact support.")
            
    except Exception as e:
        st.error(f"Error processing upgrade: {str(e)}")

elif query_params.get("upgrade") == "cancelled":
    st.warning("⚠️ Payment was cancelled. You can try again anytime!")
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

# Header with logo and user info
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown('<div class="logo">⚡ Kaspa Analytics</div>', unsafe_allow_html=True)

with col2:
    if st.session_state.get('authentication_status'):
        # Show user info with premium status
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
        
        if st.button("👤 Account", key="header_account"):
            st.switch_page("pages/A_👤_Account.py")
    else:
        if st.button("🔑 Login", key="header_login", use_container_width=True):
            st.switch_page("pages/0_🔑_Login.py")

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
