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
            if payment_handler.handle_successful_payment(session_id, username_from_stripe):
                db.update_premium_status(username_from_stripe, True)
                
                # Auto-login the user if they're not logged in
                if not st.session_state.get('authentication_status'):
                    st.session_state['authentication_status'] = True
                    st.session_state['username'] = username_from_stripe
                    user = db.get_user(username_from_stripe)
                    st.session_state['name'] = user['name']
                    st.session_state['is_premium'] = True
                    
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
                            st.session_state['authentication_status'] = True
                            st.session_state['username'] = username
                            user = db.get_user(username)
                            st.session_state['name'] = user['name']
                            st.session_state['is_premium'] = user['is_premium']
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
        st.write(f"Welcome, {st.session_state['name']}!")
        if st.button("Logout"):
            st.session_state['authentication_status'] = None
            st.session_state['username'] = None
            st.session_state['name'] = None
            st.session_state['is_premium'] = False
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

# Display selected page
if selected_page:
    page_file = pages[selected_section][selected_page]
    if os.path.exists(page_file):
        page_module = load_page_module(page_file)
        page_module.show()
    else:
        st.error(f"Page file not found: {page_file}")
else:
    if selected_section == "Paid Section":
        st.title("Premium Access Required")
        st.write("Please login and upgrade to access premium features.")
        
        col1, col2, col3 = st.columns(3)
        with col2:
            st.info("Premium Features Include:\n- Advanced Analytics\n- Real-time Data\n- Custom Alerts\n- Priority Support")
    else:
        # Show default home page
        st.title("Welcome to Kaspa Analytics")
        st.write("Select a section and page from the sidebar to get started.")
        
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
