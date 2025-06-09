import streamlit as st
import sys
import os

# Page config MUST be first!
st.set_page_config(
    page_title="Header Experiment - Kaspa Analytics", 
    page_icon="🎨", 
    layout="wide",
    initial_sidebar_state="expanded"  # Show sidebar
)

# Add parent directory to path for imports
parent_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(parent_dir)

from database import Database
from auth_handler import AuthHandler
from payment_handler import PaymentHandler
from email_handler import EmailHandler
from navigation import add_navigation  # Add navigation import

# Initialize handlers
@st.cache_resource
def init_handlers():
    db = Database()
    auth_handler = AuthHandler(db)
    payment_handler = PaymentHandler()
    email_handler = EmailHandler()
    return db, auth_handler, payment_handler, email_handler

db, auth_handler, payment_handler, email_handler = init_handlers()

# Check for persistent login
if not st.session_state.get('authentication_status'):
    auth_handler.check_persistent_login()

# Add navigation sidebar
add_navigation()

# Custom CSS for real website header
st.markdown("""
<style>
    /* Hide Streamlit default elements */
    .stApp > header {
        background-color: transparent;
    }
    
    .stApp {
        margin-top: -80px;
    }
    
    /* Aggressively hide trigger buttons */
    button[title="Hidden"],
    button:contains("TRIGGER_"),
    [data-testid="stButton"]:has(button:contains("TRIGGER_")) {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        height: 0 !important;
        width: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        border: none !important;
        position: absolute !important;
        top: -9999px !important;
        left: -9999px !important;
        pointer-events: none !important;
        z-index: -9999 !important;
    }
    
    /* Custom Real Website Header */
    .real-website-header {
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        width: 100vw !important;
        height: 70px;
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.95) 100%);
        backdrop-filter: blur(20px);
        border-bottom: 1px solid rgba(0, 212, 255, 0.2);
        z-index: 999999 !important;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 2rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    
    /* Logo Section */
    .header-logo {
        display: flex;
        align-items: center;
        gap: 12px;
        font-size: 24px;
        font-weight: 700;
        color: #00d4ff;
        text-decoration: none;
        transition: all 0.3s ease;
    }
    
    .header-logo:hover {
        color: #ffffff;
        transform: translateY(-1px);
    }
    
    .logo-icon {
        font-size: 28px;
        background: linear-gradient(135deg, #00d4ff 0%, #0ea5e9 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* User Account Section */
    .header-user-section {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .user-info {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        gap: 2px;
    }
    
    .user-name {
        color: #f1f5f9;
        font-weight: 600;
        font-size: 14px;
    }
    
    .user-status {
        color: #00d4ff;
        font-size: 11px;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .user-status.premium {
        color: #fbbf24;
    }
    
    /* Header Buttons */
    .header-btn {
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.1) 0%, rgba(0, 212, 255, 0.2) 100%);
        border: 1px solid rgba(0, 212, 255, 0.3);
        border-radius: 8px;
        padding: 8px 16px;
        color: #00d4ff;
        text-decoration: none;
        font-weight: 500;
        font-size: 13px;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .header-btn:hover {
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.2) 0%, rgba(0, 212, 255, 0.3) 100%);
        border-color: #00d4ff;
        color: #ffffff;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 212, 255, 0.2);
    }
    
    .header-btn.logout {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(239, 68, 68, 0.2) 100%);
        border-color: rgba(239, 68, 68, 0.3);
        color: #ef4444;
    }
    
    .header-btn.logout:hover {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(239, 68, 68, 0.3) 100%);
        border-color: #ef4444;
        color: #ffffff;
    }
    
    /* Main Content Area */
    .main-content {
        margin-top: 90px;
        padding: 2rem;
    }
    
    /* Welcome Section */
    .welcome-section {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.8) 0%, rgba(30, 41, 59, 0.8) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(0, 212, 255, 0.2);
        border-radius: 16px;
        padding: 3rem;
        margin-bottom: 3rem;
        text-align: center;
    }
    
    .welcome-title {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #00d4ff 0%, #0ea5e9 50%, #ffffff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
    }
    
    .welcome-subtitle {
        color: #cbd5e1;
        font-size: 1.2rem;
        font-weight: 400;
        margin-bottom: 2rem;
    }
    
    /* Stats Grid */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 2rem;
        margin: 3rem 0;
    }
    
    .stat-card {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.6) 0%, rgba(30, 41, 59, 0.6) 100%);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(0, 212, 255, 0.2);
        border-radius: 12px;
        padding: 2rem;
        transition: all 0.3s ease;
    }
    
    .stat-card:hover {
        border-color: #00d4ff;
        transform: translateY(-4px);
        box-shadow: 0 8px 32px rgba(0, 212, 255, 0.2);
    }
    
    .stat-value {
        font-size: 2rem;
        font-weight: 700;
        color: #00d4ff;
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        color: #94a3b8;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stat-change {
        font-size: 0.8rem;
        font-weight: 500;
        margin-top: 0.5rem;
    }
    
    .stat-change.positive {
        color: #10b981;
    }
    
    .stat-change.negative {
        color: #ef4444;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .real-website-header {
            padding: 0 1rem;
        }
        
        .header-logo {
            font-size: 20px;
        }
        
        .user-info {
            display: none;
        }
        
        .welcome-title {
            font-size: 2rem;
        }
        
        .stats-grid {
            grid-template-columns: 1fr;
        }
    }
</style>
""", unsafe_allow_html=True)

# Real Website Header
def render_real_header():
    if st.session_state.get('authentication_status'):
        # Logged in user
        user_name = st.session_state.get('name', 'User')
        is_premium = st.session_state.get('is_premium', False)
        premium_expires = st.session_state.get('premium_expires_at')
        
        # Calculate days left for premium users
        days_left_text = ""
        if is_premium and premium_expires:
            from datetime import datetime
            try:
                expires = datetime.fromisoformat(premium_expires.replace('Z', '+00:00'))
                days_left = (expires - datetime.now()).days
                if days_left > 0:
                    days_left_text = f" ({days_left} days left)"
            except:
                pass
        
        status_text = f"👑 PREMIUM{days_left_text}" if is_premium else "FREE TIER"
        status_class = "premium" if is_premium else ""
        
        # Create header HTML without onclick buttons
        header_html = f"""
        <div class="real-website-header">
            <div class="header-logo">
                <span class="logo-icon">⚡</span>
                <span>Kaspa Analytics</span>
            </div>
            <div class="header-user-section">
                <div class="user-info">
                    <div class="user-name">Welcome, {user_name}</div>
                    <div class="user-status {status_class}">{status_text}</div>
                </div>
                <div id="header-account-btn" class="header-btn">👤 Account</div>
                <div id="header-logout-btn" class="header-btn logout">🚪 Logout</div>
            </div>
        </div>
        """
        
        # Add the header
        st.markdown(header_html, unsafe_allow_html=True)
        
        # Create invisible Streamlit buttons that we'll trigger with JavaScript
        st.markdown('<div class="hidden-header-buttons">', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("Hidden Account", key="hidden_account_btn", type="primary"):
                st.switch_page("pages/A_👤_Account.py")
        
        with col2:
            if st.button("Hidden Logout", key="hidden_logout_btn", type="secondary"):
                auth_handler.logout()
                st.success("✅ Logged out successfully!")
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # JavaScript to connect header buttons to Streamlit buttons
        button_script = """
        <script>
        setTimeout(function() {
            // Find and click the appropriate hidden button
            function clickHiddenButton(buttonType) {
                const buttons = document.querySelectorAll('[data-testid="stButton"] button');
                buttons.forEach(button => {
                    if (buttonType === 'account' && button.textContent.includes('Hidden Account')) {
                        button.click();
                    } else if (buttonType === 'logout' && button.textContent.includes('Hidden Logout')) {
                        button.click();
                    }
                });
            }
            
            // Connect header buttons
            const headerAccountBtn = document.getElementById('header-account-btn');
            const headerLogoutBtn = document.getElementById('header-logout-btn');
            
            if (headerAccountBtn) {
                headerAccountBtn.style.cursor = 'pointer';
                headerAccountBtn.addEventListener('click', function() {
                    clickHiddenButton('account');
                });
            }
            
            if (headerLogoutBtn) {
                headerLogoutBtn.style.cursor = 'pointer';
                headerLogoutBtn.addEventListener('click', function() {
                    clickHiddenButton('logout');
                });
            }
        }, 1000);
        </script>
        """
        st.markdown(button_script, unsafe_allow_html=True)
        
    else:
        # Not logged in - create header with login buttons
        header_html = """
        <div class="real-website-header">
            <div class="header-logo">
                <span class="logo-icon">⚡</span>
                <span>Kaspa Analytics</span>
            </div>
            <div class="header-user-section">
                <div id="header-login-btn" class="header-btn">🔑 Login</div>
                <div id="header-signup-btn" class="header-btn">📝 Sign Up</div>
            </div>
        </div>
        """
        
        st.markdown(header_html, unsafe_allow_html=True)
        
        # Create invisible Streamlit buttons for login
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if st.button("Hidden Login", key="hidden_login_btn", type="primary"):
                st.switch_page("pages/0_🔑_Login.py")
        
        with col2:
            if st.button("Hidden Signup", key="hidden_signup_btn", type="secondary"):
                st.switch_page("pages/0_🔑_Login.py")
        
        # JavaScript for login buttons
        login_script = """
        <script>
        setTimeout(function() {
            // Hide the invisible Streamlit buttons
            const hiddenButtons = document.querySelectorAll('[data-testid="stButton"]');
            hiddenButtons.forEach(button => {
                if (button.textContent.includes('Hidden Login') || button.textContent.includes('Hidden Signup')) {
                    button.style.display = 'none';
                }
            });
            
            // Connect header buttons to Streamlit buttons
            const headerLoginBtn = document.getElementById('header-login-btn');
            const headerSignupBtn = document.getElementById('header-signup-btn');
            
            if (headerLoginBtn) {
                headerLoginBtn.addEventListener('click', function() {
                    const loginBtn = document.querySelector('[data-testid="stButton"] button[kind="primary"]');
                    if (loginBtn && loginBtn.textContent.includes('Hidden Login')) {
                        loginBtn.click();
                    }
                });
            }
            
            if (headerSignupBtn) {
                headerSignupBtn.addEventListener('click', function() {
                    const signupBtn = document.querySelector('[data-testid="stButton"] button[kind="secondary"]');
                    if (signupBtn && signupBtn.textContent.includes('Hidden Signup')) {
                        signupBtn.click();
                    }
                });
            }
        }, 500);
        </script>
        """
        st.markdown(login_script, unsafe_allow_html=True)

# Render the header
render_real_header()

# Remove the old logout handling script since we now handle it differently

# Main Content
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# Welcome Section
welcome_html = """
<div class="welcome-section">
    <h1 class="welcome-title">Header Design Experiment</h1>
    <p class="welcome-subtitle">Testing real website-style header with Kaspa Analytics branding and user account integration</p>
</div>
"""
st.markdown(welcome_html, unsafe_allow_html=True)

# Demo Stats Section
stats_html = """
<div class="stats-grid">
    <div class="stat-card">
        <div class="stat-value">$0.125</div>
        <div class="stat-label">Current Price</div>
        <div class="stat-change positive">+2.4%</div>
    </div>
    <div class="stat-card">
        <div class="stat-value">$3.1B</div>
        <div class="stat-label">Market Cap</div>
        <div class="stat-change positive">+1.8%</div>
    </div>
    <div class="stat-card">
        <div class="stat-value">$45M</div>
        <div class="stat-label">24h Volume</div>
        <div class="stat-change negative">-5.2%</div>
    </div>
    <div class="stat-card">
        <div class="stat-value">1.2 EH/s</div>
        <div class="stat-label">Network Hashrate</div>
        <div class="stat-change positive">+0.8%</div>
    </div>
</div>
"""
st.markdown(stats_html, unsafe_allow_html=True)

# Test Section
st.markdown("## 🧪 Header Features Test")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### ✅ Working Features")
    st.write("• Fixed position header")
    st.write("• Logo with gradient effect")
    st.write("• User account info display")
    st.write("• Premium status indicator")
    st.write("• Responsive design")
    st.write("• Glassmorphism effects")

with col2:
    st.markdown("### 🎨 Design Elements")
    st.write("• Gradient backgrounds")
    st.write("• Backdrop blur effects")
    st.write("• Hover animations")
    st.write("• Professional typography")
    st.write("• Kaspa brand colors")
    st.write("• Mobile responsive")

with col3:
    st.markdown("### 🔧 Technical Implementation")
    st.write("• Fixed CSS positioning")
    st.write("• Z-index layering")
    st.write("• JavaScript integration")
    st.write("• Streamlit state management")
    st.write("• Cross-page compatibility")
    st.write("• Session persistence")

# Action Buttons
st.markdown("### 🚀 Test Header Functionality")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🏠 Go to Home", use_container_width=True):
        st.switch_page("Home.py")

with col2:
    if st.button("🔑 Login Page", use_container_width=True):
        st.switch_page("pages/0_🔑_Login.py")

with col3:
    if st.button("👤 Account Page", use_container_width=True):
        st.switch_page("pages/A_👤_Account.py")

with col4:
    if st.session_state.get('authentication_status'):
        if st.button("🚪 Test Logout", use_container_width=True):
            auth_handler.logout()
            st.success("✅ Logged out successfully!")
            st.rerun()
    else:
        if st.button("🎮 Demo Login", use_container_width=True):
            if auth_handler.login_user("demo_user", "demo123", True):
                st.success("✅ Demo login successful!")
                st.rerun()

# Info Section
st.markdown("---")
st.info("""
**🎨 Header Design Notes:**
- Fixed position header that stays at top during scroll
- Left side: Kaspa Analytics logo with gradient effects
- Right side: User account info (name, premium status, action buttons)
- Glassmorphism design with backdrop blur
- Responsive for mobile devices
- Integrates with existing authentication system
""")

st.markdown('</div>', unsafe_allow_html=True)

# Footer
footer_html = f"""
<div style="text-align: center; padding: 2rem; margin-top: 3rem; 
     background: rgba(15, 20, 25, 0.3); backdrop-filter: blur(20px);
     border-top: 1px solid rgba(255, 255, 255, 0.08);">
    <p style="color: #64748b; font-size: 13px;">
        Header Design Experiment • Real Website Header Implementation
    </p>
    <div style="color: #475569; font-size: 11px;">
        URL: https://kaspametrics3test1.streamlit.app/X_🎨_Header_Experiment
    </div>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)
