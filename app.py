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
        st.write(f"Debug: Session ID: {session_id}")

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
                            
                            st.write(f"Debug: Logged in user {username}, premium status: {is_premium}")
                            if isinstance(expiry_info, str):
                                st.write(f"Debug: Premium info: {expiry_info}")
                            
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

# Sidebar navigation
st.sidebar.title("Navigation")

def load_page_module(file_path):
    """Dynamically load a page module"""
    spec = importlib.util.spec_from_file_location("page_module", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Define pages structure with file paths
pages = {
    "Mining": {
        "Hashrate": "pages/mining/hashrate.py",
        "Difficulty": "pages/mining/difficulty.py"
    },
    "Spot": {
        "Price": "pages/spot/price.py",
        "Volume": "pages/spot/volume.py",
        "Market Cap": "pages/spot/marketcap.py"
    },
    "Social Data": {
        "Test Page": "pages/social/test_page.py",
        "Test Page 2": "pages/social/test_page2.py"
    },
    "Paid Section": {
        "Premium Analytics": "pages/paid/test_paid.py",
        "Advanced Metrics": "pages/paid/test_paid2.py"
    }
}

# Sidebar navigation
selected_section = st.sidebar.selectbox("Select Section", list(pages.keys()))

# Check if user has access to paid section
if selected_section == "Paid Section":
    if st.session_state.get('authentication_status') != True:
        st.sidebar.warning("Please login to access paid features")
        selected_page = None
    elif not st.session_state.get('is_premium', False):
        st.sidebar.warning("Upgrade to premium to access this section")
        # Payment integration with pricing options
        st.sidebar.subheader("Choose Your Plan:")
        
        col1, col2 = st.sidebar.columns(2)
        with col1:
            if st.button("Monthly\n$9.99/mo", key="monthly"):
                try:
                    # Set session state for pricing
                    st.session_state['selected_plan'] = {'amount': 999, 'interval': 'month'}
                    payment_url = payment_handler.create_checkout_session(st.session_state['username'])
                    if payment_url:
                        st.sidebar.markdown(f"[Click here to upgrade]({payment_url})")
                except Exception as e:
                    st.sidebar.error(f"Error creating payment session: {str(e)}")
        with col2:
            if st.button("Annual\n$99/year", key="annual"):
                try:
                    # Set session state for pricing
                    st.session_state['selected_plan'] = {'amount': 9900, 'interval': 'year'}
                    payment_url = payment_handler.create_checkout_session(st.session_state['username'])
                    if payment_url:
                        st.sidebar.markdown(f"[Click here to upgrade]({payment_url})")
                except Exception as e:
                    st.sidebar.error(f"Error creating payment session: {str(e)}")
        
        selected_page = None
    else:
        selected_page = st.sidebar.selectbox("Select Page", list(pages[selected_section].keys()))
else:
    selected_page = st.sidebar.selectbox("Select Page", list(pages[selected_section].keys()))

# Define pages structure (keep existing file paths)
pages = {
    "Mining": {
        "Hashrate": "pages/mining/hashrate.py",
        "Difficulty": "pages/mining/difficulty.py"
    },
    "Spot": {
        "Price": "pages/spot/price.py",
        "Volume": "pages/spot/volume.py",
        "Market Cap": "pages/spot/marketcap.py"
    },
    "Social Data": {
        "Test Page": "pages/social/test_page.py",
        "Test Page 2": "pages/social/test_page2.py"
    },
    "Paid Section": {
        "Premium Analytics": "pages/paid/test_paid.py",
        "Advanced Metrics": "pages/paid/test_paid2.py"
    }
}

# Display selected page
if selected_section and selected_page:
    if selected_section in pages and selected_page in pages[selected_section]:
        page_file = pages[selected_section][selected_page]
        if os.path.exists(page_file):
            page_module = load_page_module(page_file)
            page_module.show()
        else:
            st.error(f"Page file not found: {page_file}")
    else:
        st.error("Invalid page selection")
else:
    # Show default home page when no page is selected
    st.title("⚡ Welcome to Kaspa Analytics")
    st.write("Select a page from the sidebar to get started.")
    
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
        
    # Quick navigation
    st.subheader("🚀 Quick Start")
    quick_col1, quick_col2, quick_col3 = st.columns(3)
    
    with quick_col1:
        if st.button("📈 View Mining Data", use_container_width=True):
            st.session_state['selected_section'] = 'Mining'
            st.session_state['selected_page'] = 'Hashrate'
            st.query_params.update({"page": "hashrate"})
            st.rerun()
            
    with quick_col2:
        if st.button("💰 Check Price", use_container_width=True):
            st.session_state['selected_section'] = 'Spot'
            st.session_state['selected_page'] = 'Price'
            st.query_params.update({"page": "price"})
            st.rerun()
            
    with quick_col3:
        if st.button("📱 Social Metrics", use_container_width=True):
            st.session_state['selected_section'] = 'Social Data'
            st.session_state['selected_page'] = 'Test Page'
            st.query_params.update({"page": "social"})
            st.rerun()
