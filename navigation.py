import streamlit as st
import os

def load_global_css():
    """Load global CSS file if it exists"""
    try:
        css_file_path = os.path.join('.streamlit', 'style.css')
        if os.path.exists(css_file_path):
            with open(css_file_path) as f:
                st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        else:
            # Fallback CSS if file doesn't exist
            st.markdown("""
                <style>
                /* Hide native Streamlit page navigation */
                .css-1q1n0ol[data-testid="stSidebarNav"] {
                    display: none !important;
                }
                
                div[data-testid="stSidebarNav"] {
                    display: none !important;
                }
                
                section[data-testid="stSidebar"] nav {
                    display: none !important;
                }
                
                /* Ensure our content remains visible */
                section[data-testid="stSidebar"] > div {
                    display: block !important;
                }
                </style>
            """, unsafe_allow_html=True)
    except Exception as e:
        # If anything fails, use basic CSS
        st.markdown("""
            <style>
            [data-testid="stSidebarNav"] { display: none !important; }
            section[data-testid="stSidebar"] nav { display: none !important; }
            </style>
        """, unsafe_allow_html=True)

def add_navigation():
    """Add organized navigation to sidebar (shared across all pages)"""
    
    # Load global CSS first
    load_global_css()
    
    # Add home button at top
    if st.sidebar.button("🏠 Home", key="nav_home", use_container_width=True):
        st.switch_page("Home.py")
    
    # Account buttons right under Home
    if st.session_state.get('authentication_status'):
        # User is logged in - show Account and Logout side by side
        col1, col2 = st.sidebar.columns(2)
        with col1:
            if st.button("👤 Account", key="nav_account", use_container_width=True):
                st.switch_page("pages/A_👤_Account.py")
        with col2:
            if st.button("🚪 Logout", key="nav_logout", use_container_width=True):
                st.session_state.clear()
                st.switch_page("Home.py")
    else:
        # User not logged in
        if st.sidebar.button("🔑 Login / Register", key="nav_login", use_container_width=True):
            st.switch_page("pages/0_🔑_Login.py")
    
    st.sidebar.markdown("---")
    
    # Mining Section (COLLAPSED by default)
    with st.sidebar.expander("⛏️ Mining", expanded=False):
        if st.button("📈 Hashrate", key="sidebar_hashrate", use_container_width=True):
            st.switch_page("pages/1_⛏️_Mining_Hashrate.py")
        if st.button("⚙️ Difficulty", key="sidebar_difficulty", use_container_width=True):
            st.switch_page("pages/2_⛏️_Mining_Difficulty.py")
    
    # Spot Section (EXPANDED by default - main focus for new visitors)
    with st.sidebar.expander("💰 Spot Market", expanded=True):
        if st.button("💵 Price", key="sidebar_price", use_container_width=True):
            st.switch_page("pages/3_💰_Spot_Price.py")
        if st.button("📊 Volume", key="sidebar_volume", use_container_width=True):
            st.switch_page("pages/4_💰_Spot_Volume.py")
        if st.button("🏦 Market Cap", key="sidebar_marketcap", use_container_width=True):
            st.switch_page("pages/5_💰_Spot_Market_Cap.py")
    
    # Social Section (COLLAPSED by default)
    with st.sidebar.expander("📱 Social Data", expanded=False):
        if st.button("📈 Social Metrics", key="sidebar_social1", use_container_width=True):
            st.switch_page("pages/6_📱_Social_Metrics.py")
        if st.button("📊 Social Trends", key="sidebar_social2", use_container_width=True):
            st.switch_page("pages/7_📱_Social_Trends.py")
    
    # Premium Analytics Section (COLLAPSED by default)
    if st.session_state.get('authentication_status') and st.session_state.get('is_premium'):
        with st.sidebar.expander("👑 Premium Analytics", expanded=False):
            if st.button("👑 Premium Features", key="sidebar_premium_features", use_container_width=True):
                st.switch_page("pages/B_👑_Premium_Features.py")
            if st.button("🔬 Premium Analytics", key="sidebar_premium1", use_container_width=True):
                st.switch_page("pages/8_👑_Premium_Analytics.py")
            if st.button("📊 Advanced Metrics", key="sidebar_premium2", use_container_width=True):
                st.switch_page("pages/9_👑_Advanced_Metrics.py")
    elif st.session_state.get('authentication_status'):
        with st.sidebar.expander("👑 Premium Analytics", expanded=False):
            # Premium Features accessible to logged-in users (but not paying)
            if st.button("👑 Premium Features", key="sidebar_premium_features_free", use_container_width=True):
                st.switch_page("pages/B_👑_Premium_Features.py")
            st.warning("Upgrade Required")
            st.write("**Monthly:** $9.99")
            st.write("**Annual:** $99")
            if st.button("💳 Upgrade Now", key="sidebar_upgrade", use_container_width=True):
                st.switch_page("pages/B_👑_Premium_Features.py")
    else:
        with st.sidebar.expander("👑 Premium Analytics", expanded=False):
            # Premium Features accessible to everyone (including non-logged users)
            if st.button("👑 Premium Features", key="sidebar_premium_features_guest", use_container_width=True):
                st.switch_page("pages/B_👑_Premium_Features.py")
            st.info("Login Required")
            st.write("Sign in to access premium analytics")
            if st.button("🔑 Login", key="sidebar_login_premium", use_container_width=True):
                st.switch_page("pages/0_🔑_Login.py")
    
    # Footer info
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ℹ️ Status")
    
    if st.session_state.get('is_premium'):
        st.sidebar.success("👑 Premium Active")
        if st.session_state.get('premium_expires_at'):
            try:
                expires_str = str(st.session_state['premium_expires_at'])[:10]
                st.sidebar.write(f"Expires: {expires_str}")
            except:
                st.sidebar.write("Expires: Active")
        else:
            st.sidebar.write("Expires: Active")
    elif st.session_state.get('authentication_status'):
        st.sidebar.warning("🔒 Free Account")
        st.sidebar.write("Upgrade for premium features")
    else:
        st.sidebar.info("🔐 Not Logged In")
        st.sidebar.write("Login for full access")
