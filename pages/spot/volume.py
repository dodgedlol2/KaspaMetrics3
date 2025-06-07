import streamlit as st
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from database import Database
from auth_handler import AuthHandler
from payment_handler import PaymentHandler

# Import page modules using absolute imports
import sys
import os
sys.path.append(os.path.dirname(__file__))

from pages.mining.hashrate import show as hashrate_show
from pages.mining.difficulty import show as difficulty_show
from pages.spot.price import show as price_show
from pages.spot.volume import show as volume_show
from pages.spot.marketcap import show as marketcap_show
from pages.social.test_page import show as test_page_show
from pages.social.test_page2 import show as test_page2_show
from pages.paid.test_paid import show as test_paid_show
from pages.paid.test_paid2 import show as test_paid2_show

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

# Define pages structure
pages = {
    "Mining": {
        "Hashrate": {"show": hashrate_show},
        "Difficulty": {"show": difficulty_show}
    },
    "Spot": {
        "Price": {"show": price_show},
        "Volume": {"show": volume_show},
        "Market Cap": {"show": marketcap_show}
    },
    "Social Data": {
        "Test Page": {"show": test_page_show},
        "Test Page 2": {"show": test_page2_show}
    },
    "Paid Section": {
        "Premium Analytics": {"show": test_paid_show},
        "Advanced Metrics": {"show": test_paid2_show}
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
        # Payment integration
        if st.sidebar.button("Upgrade to Premium"):
            payment_url = payment_handler.create_checkout_session(st.session_state['username'])
            if payment_url:
                st.sidebar.markdown(f"[Click here to upgrade]({payment_url})")
        selected_page = None
    else:
        selected_page = st.sidebar.selectbox("Select Page", list(pages[selected_section].keys()))
else:
    selected_page = st.sidebar.selectbox("Select Page", list(pages[selected_section].keys()))

# Display selected page
if selected_page:
    page_function = pages[selected_section][selected_page]["show"]
    page_function()
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
