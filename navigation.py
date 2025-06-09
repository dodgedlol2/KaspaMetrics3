import streamlit as st

def add_navigation():
    """Add organized navigation to sidebar AND custom header (shared across all pages)"""
    
    # First add the header
    _add_custom_header()
    
    # Then add the sidebar navigation (your original code)
    _add_sidebar_navigation()

def _add_custom_header():
    """Add the custom website header"""
    
    # CSS for header and the WORKING sidebar fix
    st.markdown("""
    <style>
        /* Header positioning */
        .stApp { margin-top: -80px !important; }
        
        /* WORKING SIDEBAR FIX - exactly what worked in console */
        [data-testid="stSidebar"] {
            margin-top: 80px !important;
        }
        
        /* Custom header */
        .real-website-header {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            right: 0 !important;
            width: 100vw !important;
            height: 70px !important;
            z-index: 999999 !important;
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.95) 100%) !important;
            backdrop-filter: blur(20px) !important;
            border-bottom: 1px solid rgba(0, 212, 255, 0.2) !important;
            display: flex !important;
            align-items: center !important;
            justify-content: space-between !important;
            padding: 0 2rem !important;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3) !important;
        }
        
        /* Logo styles */
        .header-logo {
            display: flex !important;
            align-items: center !important;
            gap: 12px !important;
            font-size: 24px !important;
            font-weight: 700 !important;
            color: #00d4ff !important;
        }
        
        .logo-icon {
            font-size: 28px !important;
            background: linear-gradient(135deg, #00d4ff 0%, #0ea5e9 100%) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            background-clip: text !important;
        }
        
        /* User info styles */
        .header-user-section {
            display: flex !important;
            align-items: center !important;
            gap: 1rem !important;
        }
        
        .user-info {
            display: flex !important;
            flex-direction: column !important;
            align-items: flex-end !important;
            gap: 2px !important;
        }
        
        .user-name {
            color: #f1f5f9 !important;
            font-weight: 600 !important;
            font-size: 14px !important;
        }
        
        .user-status {
            color: #00d4ff !important;
            font-size: 11px !important;
            font-weight: 500 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.5px !important;
        }
        
        .user-status.premium {
            color: #fbbf24 !important;
        }
        
        /* Main content positioning */
        .main-content {
            margin-top: 90px !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Render header HTML
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
            </div>
        </div>
        """
        
    else:
        # Not logged in
        header_html = """
        <div class="real-website-header">
            <div class="header-logo">
                <span class="logo-icon">⚡</span>
                <span>Kaspa Analytics</span>
            </div>
            <div class="header-user-section">
                <div class="user-info">
                    <div class="user-name">Please log in</div>
                    <div class="user-status">GUEST</div>
                </div>
            </div>
        </div>
        """
    
    st.markdown(header_html, unsafe_allow_html=True)
    
    # Add margin to main content
    st.markdown('<div class="main-content">', unsafe_allow_html=True)

def _add_sidebar_navigation():
    """Add the sidebar navigation (your original code)"""
    
    # More precise CSS to hide only native page navigation
    st.markdown("""
        <style>
        /* Hide only the native Streamlit page list */
        .css-1q1n0ol[data-testid="stSidebarNav"] {
            display: none;
        }
        
        /* Alternative selectors for native page navigation */
        div[data-testid="stSidebarNav"] {
            display: none;
        }
        
        /* Keep sidebar visible but hide page selector */
        section[data-testid="stSidebar"] nav {
            display: none;
        }
        
        /* Ensure our content remains visible */
        section[data-testid="stSidebar"] > div {
            display: block !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
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
    
    # Mining Section (REMOVED "📊 Analytics" header text/icon)
    with st.sidebar.expander("⛏️ Mining", expanded=True):
        if st.button("📈 Hashrate", key="sidebar_hashrate", use_container_width=True):
            st.switch_page("pages/1_⛏️_Mining_Hashrate.py")
        if st.button("⚙️ Difficulty", key="sidebar_difficulty", use_container_width=True):
            st.switch_page("pages/2_⛏️_Mining_Difficulty.py")
    
    # Spot Section
    with st.sidebar.expander("💰 Spot Market", expanded=True):
        if st.button("💵 Price", key="sidebar_price", use_container_width=True):
            st.switch_page("pages/3_💰_Spot_Price.py")
        if st.button("📊 Volume", key="sidebar_volume", use_container_width=True):
            st.switch_page("pages/4_💰_Spot_Volume.py")
        if st.button("🏦 Market Cap", key="sidebar_marketcap", use_container_width=True):
            st.switch_page("pages/5_💰_Spot_Market_Cap.py")
    
    # Social Section
    with st.sidebar.expander("📱 Social Data", expanded=True):
        if st.button("📈 Social Metrics", key="sidebar_social1", use_container_width=True):
            st.switch_page("pages/6_📱_Social_Metrics.py")
        if st.button("📊 Social Trends", key="sidebar_social2", use_container_width=True):
            st.switch_page("pages/7_📱_Social_Trends.py")
    
    # Premium Analytics Section (MOVED Premium Features here + access control)
    if st.session_state.get('authentication_status') and st.session_state.get('is_premium'):
        with st.sidebar.expander("👑 Premium Analytics", expanded=True):
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
