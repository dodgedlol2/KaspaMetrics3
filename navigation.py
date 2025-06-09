import streamlit as st

def add_navigation():
    """Add organized navigation to sidebar AND custom header (shared across all pages)"""
    
    # First, add the custom header
    _add_custom_header()
    
    # Then add the sidebar navigation
    _add_sidebar_navigation()

def _add_custom_header():
    """Add the custom website header with Kaspa Analytics branding"""
    
    # IMMEDIATE CSS injection - loads before anything else renders
    st.markdown("""
    <style>
        /* CRITICAL: Load these styles FIRST to prevent flicker */
        .stApp { margin-top: -80px !important; }
        .real-website-header { 
            position: fixed !important; 
            top: 0 !important; 
            left: 0 !important; 
            right: 0 !important; 
            width: 100vw !important; 
            height: 70px !important; 
            z-index: 999999 !important; 
            background: rgba(15, 23, 42, 0.95) !important;
            display: flex !important;
        }
        [data-testid="stSidebar"] { margin-top: 80px !important; }
        [data-testid="collapsedControl"] { top: 90px !important; z-index: 1000000 !important; }
    </style>
    """, unsafe_allow_html=True)
    
    # Render header HTML IMMEDIATELY after critical CSS
    if st.session_state.get('authentication_status'):
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
        
        header_html = f"""
        <div class="real-website-header" style="
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
        ">
            <div class="header-logo" style="
                display: flex !important;
                align-items: center !important;
                gap: 12px !important;
                font-size: 24px !important;
                font-weight: 700 !important;
                color: #00d4ff !important;
            ">
                <span class="logo-icon" style="
                    font-size: 28px !important;
                    background: linear-gradient(135deg, #00d4ff 0%, #0ea5e9 100%) !important;
                    -webkit-background-clip: text !important;
                    -webkit-text-fill-color: transparent !important;
                    background-clip: text !important;
                ">⚡</span>
                <span>Kaspa Analytics</span>
            </div>
            <div class="header-user-section" style="
                display: flex !important;
                align-items: center !important;
                gap: 1rem !important;
            ">
                <div class="user-info" style="
                    display: flex !important;
                    flex-direction: column !important;
                    align-items: flex-end !important;
                    gap: 2px !important;
                ">
                    <div class="user-name" style="
                        color: #f1f5f9 !important;
                        font-weight: 600 !important;
                        font-size: 14px !important;
                    ">Welcome, {user_name}</div>
                    <div class="user-status {status_class}" style="
                        color: {'#fbbf24' if is_premium else '#00d4ff'} !important;
                        font-size: 11px !important;
                        font-weight: 500 !important;
                        text-transform: uppercase !important;
                        letter-spacing: 0.5px !important;
                    ">{status_text}</div>
                </div>
            </div>
        </div>
        """
    else:
        header_html = """
        <div class="real-website-header" style="
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
        ">
            <div class="header-logo" style="
                display: flex !important;
                align-items: center !important;
                gap: 12px !important;
                font-size: 24px !important;
                font-weight: 700 !important;
                color: #00d4ff !important;
            ">
                <span class="logo-icon" style="
                    font-size: 28px !important;
                    background: linear-gradient(135deg, #00d4ff 0%, #0ea5e9 100%) !important;
                    -webkit-background-clip: text !important;
                    -webkit-text-fill-color: transparent !important;
                    background-clip: text !important;
                ">⚡</span>
                <span>Kaspa Analytics</span>
            </div>
            <div class="header-user-section" style="
                display: flex !important;
                align-items: center !important;
                gap: 1rem !important;
            ">
                <div class="user-info" style="
                    display: flex !important;
                    flex-direction: column !important;
                    align-items: flex-end !important;
                    gap: 2px !important;
                ">
                    <div class="user-name" style="
                        color: #f1f5f9 !important;
                        font-weight: 600 !important;
                        font-size: 14px !important;
                    ">Please log in</div>
                    <div class="user-status" style="
                        color: #00d4ff !important;
                        font-size: 11px !important;
                        font-weight: 500 !important;
                        text-transform: uppercase !important;
                        letter-spacing: 0.5px !important;
                    ">GUEST</div>
                </div>
            </div>
        </div>
        """
    
    st.markdown(header_html, unsafe_allow_html=True)
    
    # FULL CSS for enhanced styling (loads after header is already positioned)
    st.markdown("""
    <style>
        /* ANTI-FLICKER: Preload header positioning */
        .stApp {
            margin-top: -80px !important;
        }
        
        .real-website-header {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            right: 0 !important;
            width: 100vw !important;
            height: 70px !important;
            z-index: 999999 !important;
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.95) 100%) !important;
        }
        /* Hide Streamlit default elements */
        .stApp > header {
            background-color: transparent !important;
            display: none !important;
        }
        
        /* ENHANCED: Better sidebar positioning with no flicker */
        [data-testid="stSidebar"] {
            margin-top: 80px !important;
            transition: none !important;
        }
        
        [data-testid="collapsedControl"] {
            top: 90px !important;
            z-index: 1000000 !important;
            transition: none !important;
        }
        
        /* Force immediate positioning without animation */
        .css-1lcbmhc.e1fqkh3o0 {
            margin-top: 3.8rem !important;
            transition: none !important;
        }
        
        .css-sg054d.e1fqkh3o3 {
            margin-top: 5rem !important;
            transition: none !important;
        }
        
        /* Additional modern Streamlit sidebar selectors */
        .st-emotion-cache-1cypcdb {
            margin-top: 80px !important;
            transition: none !important;
        }
        
        .st-emotion-cache-16txtl3 {
            top: 90px !important;
            z-index: 1000000 !important;
            transition: none !important;
        }
        
        /* Force sidebar collapse button visibility with no animation */
        button[data-testid="collapsedControl"] {
            top: 90px !important;
            z-index: 1000000 !important;
            position: fixed !important;
            transition: none !important;
        }
        
        /* Custom Real Website Header - ANTI-FLICKER VERSION */
        .real-website-header {
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.95) 100%) !important;
            backdrop-filter: blur(20px) !important;
            border-bottom: 1px solid rgba(0, 212, 255, 0.2) !important;
            display: flex !important;
            align-items: center !important;
            justify-content: space-between !important;
            padding: 0 2rem !important;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3) !important;
            /* Remove any transitions to prevent flicker */
            transition: none !important;
            animation: none !important;
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
        
        /* Main Content Area */
        .main-content {
            margin-top: 90px;
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
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Render the header HTML
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
        
        # Header for logged in users
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
        # Not logged in - simple header
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
    
    # Add margin to main content
    st.markdown('<div class="main-content" style="margin-top: 90px !important;">', unsafe_allow_html=True)

def _add_sidebar_navigation():
    """Add the sidebar navigation (existing functionality)"""
    
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
