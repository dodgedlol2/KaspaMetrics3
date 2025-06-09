import streamlit as st
import sys
import os

# Page config
st.set_page_config(
    page_title="Realistic Header - Kaspa Analytics", 
    page_icon="🎯", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add parent directory to path for imports
parent_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(parent_dir)

from database import Database
from auth_handler import AuthHandler
from payment_handler import PaymentHandler
from email_handler import EmailHandler
from navigation import add_navigation

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

# Custom CSS for a realistic header that works within Streamlit's constraints
st.markdown("""
<style>
    /* Hide Streamlit's default header */
    .stApp > header {
        background-color: transparent;
    }
    
    /* Custom header that stays at the top but scrolls naturally */
    .realistic-header {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.95) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(0, 212, 255, 0.2);
        border-radius: 12px;
        padding: 1rem 2rem;
        margin-bottom: 2rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    
    .header-logo {
        display: flex;
        align-items: center;
        gap: 12px;
        font-size: 24px;
        font-weight: 700;
        color: #00d4ff;
    }
    
    .logo-icon {
        font-size: 28px;
        background: linear-gradient(135deg, #00d4ff 0%, #0ea5e9 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .header-user-info {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        gap: 4px;
    }
    
    .user-name {
        color: #f1f5f9;
        font-weight: 600;
        font-size: 16px;
    }
    
    .user-status {
        color: #00d4ff;
        font-size: 12px;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .user-status.premium {
        color: #fbbf24;
    }
    
    /* Working header buttons using Streamlit's column system */
    .header-buttons {
        display: flex;
        gap: 0.5rem;
        align-items: center;
    }
    
    /* Style the actual Streamlit buttons to look like header buttons */
    .stButton > button {
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.1) 0%, rgba(0, 212, 255, 0.2) 100%) !important;
        border: 1px solid rgba(0, 212, 255, 0.3) !important;
        border-radius: 8px !important;
        color: #00d4ff !important;
        font-weight: 500 !important;
        font-size: 13px !important;
        padding: 0.25rem 0.75rem !important;
        height: 2rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.2) 0%, rgba(0, 212, 255, 0.3) 100%) !important;
        border-color: #00d4ff !important;
        color: #ffffff !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(0, 212, 255, 0.2) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) !important;
    }
    
    /* Special styling for logout button */
    .logout-btn > button {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(239, 68, 68, 0.2) 100%) !important;
        border-color: rgba(239, 68, 68, 0.3) !important;
        color: #ef4444 !important;
    }
    
    .logout-btn > button:hover {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(239, 68, 68, 0.3) 100%) !important;
        border-color: #ef4444 !important;
        color: #ffffff !important;
    }
    
    /* Info section styling */
    .feature-info {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.6) 0%, rgba(30, 41, 59, 0.6) 100%);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(0, 212, 255, 0.2);
        border-radius: 12px;
        padding: 2rem;
        margin: 2rem 0;
    }
    
    .comparison-table {
        background: rgba(15, 20, 25, 0.8);
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .check-mark {
        color: #10b981;
        font-weight: bold;
    }
    
    .x-mark {
        color: #ef4444;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Realistic Header Implementation
def render_realistic_header():
    # Create the header container
    header_container = st.container()
    
    with header_container:
        # Use columns to create header layout
        if st.session_state.get('authentication_status'):
            # Logged in layout
            logo_col, user_info_col, buttons_col = st.columns([2, 2, 2])
            
            with logo_col:
                st.markdown("""
                <div class="header-logo">
                    <span class="logo-icon">⚡</span>
                    <span>Kaspa Analytics</span>
                </div>
                """, unsafe_allow_html=True)
            
            with user_info_col:
                user_name = st.session_state.get('name', 'User')
                is_premium = st.session_state.get('is_premium', False)
                premium_expires = st.session_state.get('premium_expires_at')
                
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
                
                st.markdown(f"""
                <div class="header-user-info">
                    <div class="user-name">Welcome, {user_name}</div>
                    <div class="user-status {status_class}">{status_text}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with buttons_col:
                # Working Streamlit buttons styled to look like header buttons
                btn_col1, btn_col2 = st.columns(2)
                
                with btn_col1:
                    if st.button("👤 Account", key="header_account", use_container_width=True):
                        st.switch_page("pages/A_👤_Account.py")
                
                with btn_col2:
                    # Add logout-btn class via markdown wrapper
                    st.markdown('<div class="logout-btn">', unsafe_allow_html=True)
                    if st.button("🚪 Logout", key="header_logout", use_container_width=True):
                        auth_handler.logout()
                        st.success("✅ Logged out successfully!")
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
        
        else:
            # Not logged in layout
            logo_col, spacer_col, buttons_col = st.columns([2, 2, 2])
            
            with logo_col:
                st.markdown("""
                <div class="header-logo">
                    <span class="logo-icon">⚡</span>
                    <span>Kaspa Analytics</span>
                </div>
                """, unsafe_allow_html=True)
            
            with spacer_col:
                st.empty()
            
            with buttons_col:
                btn_col1, btn_col2 = st.columns(2)
                
                with btn_col1:
                    if st.button("🔑 Login", key="header_login", use_container_width=True):
                        st.switch_page("pages/0_🔑_Login.py")
                
                with btn_col2:
                    if st.button("📝 Sign Up", key="header_signup", use_container_width=True):
                        st.switch_page("pages/0_🔑_Login.py")

# Apply the header styling and render
st.markdown('<div class="realistic-header">', unsafe_allow_html=True)
render_realistic_header()
st.markdown('</div>', unsafe_allow_html=True)

# Main content
st.title("🎯 Realistic Header Implementation")
st.write("A header design that actually works within Streamlit's constraints")

# Feature comparison
st.markdown("""
<div class="feature-info">
    <h3>📊 Header Implementation Comparison</h3>
    <div class="comparison-table">
""", unsafe_allow_html=True)

comparison_data = {
    "Feature": [
        "Visual Design", 
        "Button Functionality", 
        "Position Behavior", 
        "Mobile Responsive", 
        "Easy to Maintain",
        "Streamlit Compatible",
        "No Visible Bugs"
    ],
    "Fixed Header (CSS)": ["✅", "❌", "✅", "❌", "❌", "❌", "❌"],
    "Realistic Header": ["✅", "✅", "📜 Scrolls", "✅", "✅", "✅", "✅"],
    "st.navigation": ["⚠️ Sidebar", "✅", "🔒 Fixed", "✅", "✅", "✅", "✅"]
}

df = st.dataframe(comparison_data, use_container_width=True)

st.markdown('</div></div>', unsafe_allow_html=True)

# Explanation sections
col1, col2 = st.columns(2)

with col1:
    st.markdown("### ✅ What Works")
    st.write("• Beautiful header design with gradients")
    st.write("• Fully functional buttons")
    st.write("• User authentication integration") 
    st.write("• Premium status display")
    st.write("• Mobile responsive")
    st.write("• Easy to maintain")
    st.write("• No JavaScript conflicts")
    st.write("• Proper Streamlit navigation")

with col2:
    st.markdown("### 🔧 Technical Implementation")
    st.write("• Uses `st.columns()` for layout")
    st.write("• Real `st.button()` elements")
    st.write("• CSS styling within Streamlit constraints")
    st.write("• Integrates with session state")
    st.write("• Works with `st.switch_page()`")
    st.write("• No hidden button workarounds")
    st.write("• Natural scrolling behavior")
    st.write("• Compatible with all Streamlit features")

# Test section
st.markdown("---")
st.markdown("### 🧪 Test the Header")

st.info("""
**Try the header buttons above!** 
- If logged in: Try Account and Logout buttons
- If not logged in: Try Login and Sign Up buttons
- All buttons work perfectly with proper Streamlit navigation
""")

# Navigation test buttons
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("Home.py")

with col2:
    if st.button("🔑 Login Page", use_container_width=True):
        st.switch_page("pages/0_🔑_Login.py")

with col3:
    if st.button("🎨 CSS Experiment", use_container_width=True):
        st.switch_page("pages/X_🎨_Header_Experiment.py")

with col4:
    if st.session_state.get('authentication_status'):
        if st.button("👤 Account", use_container_width=True):
            st.switch_page("pages/A_👤_Account.py")
    else:
        if st.button("🎮 Demo Login", use_container_width=True):
            if auth_handler.login_user("demo_user", "demo123", True):
                st.success("✅ Demo login successful!")
                st.rerun()

# Conclusion
st.markdown("---")
st.success("""
**🎯 Conclusion:** This realistic header implementation provides the best balance of:
- Professional visual design
- Full button functionality  
- Streamlit compatibility
- Easy maintenance
- No JavaScript workarounds needed

While it scrolls with the page (instead of being fixed), it provides a much better user experience than broken fixed headers!
""")

# Footer
st.markdown(f"""
<div style="text-align: center; padding: 2rem; margin-top: 3rem; 
     background: rgba(15, 20, 25, 0.3); backdrop-filter: blur(20px);
     border-top: 1px solid rgba(255, 255, 255, 0.08);">
    <p style="color: #64748b; font-size: 13px;">
        Realistic Header Implementation • Working Within Streamlit's Design Patterns
    </p>
    <div style="color: #475569; font-size: 11px;">
        URL: https://kaspametrics3test1.streamlit.app/Y_🎯_Realistic_Header
    </div>
</div>
""", unsafe_allow_html=True)
