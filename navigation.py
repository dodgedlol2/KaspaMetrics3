import streamlit as st

def add_navigation():
    """Add organized navigation to sidebar AND minimal header (shared across all pages)"""
    
    # ULTRA-MINIMAL header CSS - absolutely no sidebar interference
    st.markdown("""
    <style>
        /* ONLY header styles - NO global changes */
        .kaspa-header-only {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            width: 100vw;
            height: 70px;
            z-index: 999999;
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.95) 100%);
            backdrop-filter: blur(20px);
            border-bottom: 1px solid rgba(0, 212, 255, 0.2);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 2rem;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        }
        
        .kaspa-logo {
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 24px;
            font-weight: 700;
            color: #00d4ff;
        }
        
        .kaspa-logo-icon {
            font-size: 28px;
            background: linear-gradient(135deg, #00d4ff 0%, #0ea5e9 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .kaspa-user-info {
            display: flex;
            flex-direction: column;
            align-items: flex-end;
            gap: 2px;
        }
        
        .kaspa-user-name {
            color: #f1f5f9;
            font-weight: 600;
            font-size: 14px;
        }
        
        .kaspa-user-status {
            color: #00d4ff;
            font-size: 11px;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .kaspa-user-status.premium {
            color: #fbbf24;
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
        <div class="kaspa-header-only">
            <div class="kaspa-logo">
                <span class="kaspa-logo-icon">⚡</span>
                <span>Kaspa Analytics</span>
            </div>
            <div class="kaspa-user-info">
                <div class="kaspa-user-name">Welcome, {user_name}</div>
                <div class="kaspa-user-status {status_class}">{status_text}</div>
            </div>
        </div>
        """
        
    else:
        # Not logged in
        header_html = """
        <div class="kaspa-header-only">
            <div class="kaspa-logo">
                <span class="kaspa-logo-icon">⚡</span>
                <span>Kaspa Analytics</span>
            </div>
            <div class="kaspa-user-info">
                <div class="kaspa-user-name">Please log in</div>
                <div class="kaspa-user-status">GUEST</div>
            </div>
        </div>
        """
    
    st.markdown(header_html, unsafe_allow_html=True)

    # YOUR ORIGINAL SIDEBAR CODE - EXACTLY AS IT WAS
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
