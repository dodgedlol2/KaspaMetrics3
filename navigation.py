import streamlit as st

def add_navigation():
    """Add organized navigation to sidebar AND header with animated DAG logo"""
    
    # IMPROVED HEADER CSS with Animated DAG Logo
    st.markdown("""
    <style>
        /* FIXED HEADER - Improved positioning and z-index management */
        .kaspa-header {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            width: 100vw;
            height: 70px;
            z-index: 999997;
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.95) 100%);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 2rem;
            border-bottom: 1px solid rgba(0, 212, 255, 0.3);
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }
        
        /* ANIMATED DAG LOGO STYLES */
        .kaspa-logo {
            display: flex;
            align-items: center;
            gap: 15px;
            font-size: 24px;
            font-weight: 700;
            color: #00d4ff;
            text-shadow: 0 0 10px rgba(0, 212, 255, 0.3);
        }
        
        .dag-logo-header {
            width: 120px;
            height: 40px;
        }
        
        .dag-block-header {
            fill: #00d4ff;
            opacity: 0;
            rx: 2;
        }
        
        .dag-connection-header {
            stroke: #00d4ff;
            stroke-width: 1.5;
            opacity: 0;
        }
        
        /* Header animation - faster and more subtle */
        .block1-header { animation: block-appear-header 4s ease-in-out infinite; }
        .block2-header { animation: block-appear-header 4s ease-in-out infinite 0.2s; }
        .block3-header { animation: block-appear-header 4s ease-in-out infinite 0.4s; }
        .block4-header { animation: block-appear-header 4s ease-in-out infinite 0.6s; }
        .block5-header { animation: block-appear-header 4s ease-in-out infinite 0.8s; }
        .block6-header { animation: block-appear-header 4s ease-in-out infinite 1.0s; }
        
        .conn1-header { animation: connection-appear-header 4s ease-in-out infinite 0.3s; }
        .conn2-header { animation: connection-appear-header 4s ease-in-out infinite 0.5s; }
        .conn3-header { animation: connection-appear-header 4s ease-in-out infinite 0.7s; }
        .conn4-header { animation: connection-appear-header 4s ease-in-out infinite 0.9s; }
        .conn5-header { animation: connection-appear-header 4s ease-in-out infinite 1.1s; }
        
        @keyframes block-appear-header {
            0%, 20% { opacity: 0; transform: scale(0); }
            25%, 75% { opacity: 0.7; transform: scale(1); }
            100% { opacity: 0.7; transform: scale(1); }
        }
        
        @keyframes connection-appear-header {
            0%, 15% { opacity: 0; }
            20%, 75% { opacity: 0.5; }
            100% { opacity: 0.5; }
        }
        
        /* PUSH MAIN CONTENT DOWN */
        .main .block-container {
            padding-top: 90px !important;
        }
        
        /* SIDEBAR POSITIONING */
        [data-testid="stSidebar"] {
            margin-top: 70px;
            height: calc(100vh - 70px);
        }
        
        /* SIDEBAR CONTROLS */
        div[data-testid="stSidebarCollapseButton"] {
            position: fixed !important;
            top: calc(85px - 2cm) !important;
            left: calc(21rem - 2cm) !important;
            z-index: 999999 !important;
            background: transparent !important;
            border: none !important;
            backdrop-filter: none !important;
        }
        
        div[data-testid="stSidebarCollapseButton"] button {
            background: transparent !important;
            border: none !important;
            opacity: 0 !important;
        }
        
        div[data-testid="stSidebarCollapsedControl"] {
            position: fixed !important;
            top: 85px !important;
            left: 0px !important;
            z-index: 999998 !important;
        }
        
        div[data-testid="stSidebarCollapseButton"] button,
        div[data-testid="stSidebarCollapsedControl"] button,
        button[data-testid="collapsedControl"] {
            pointer-events: auto !important;
            cursor: pointer !important;
            background: rgba(255, 255, 255, 0.1) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
        }
        
        /* USER INFO STYLING */
        .kaspa-user-info {
            color: #f1f5f9;
            font-size: 14px;
            text-align: right;
        }
        
        .kaspa-user-status {
            color: #00d4ff;
            font-size: 11px;
            text-transform: uppercase;
            font-weight: 600;
            margin-top: 2px;
        }
        
        .kaspa-user-status.premium {
            color: #fbbf24;
            text-shadow: 0 0 5px rgba(251, 191, 36, 0.5);
        }
        
        .kaspa-user-status.free {
            color: #94a3b8;
        }
        
        .kaspa-user-status.guest {
            color: #64748b;
        }
        
        /* HIDE NATIVE PAGE NAVIGATION */
        .css-1q1n0ol[data-testid="stSidebarNav"] {
            display: none;
        }
        
        div[data-testid="stSidebarNav"] {
            display: none;
        }
        
        section[data-testid="stSidebar"] nav {
            display: none;
        }
        
        section[data-testid="stSidebar"] > div {
            display: block !important;
        }
        
        /* RESPONSIVE ADJUSTMENTS */
        @media (max-width: 768px) {
            .kaspa-header {
                padding: 0 1rem;
            }
            
            .kaspa-logo {
                font-size: 20px;
                gap: 10px;
            }
            
            .dag-logo-header {
                width: 80px;
                height: 30px;
            }
            
            .kaspa-user-info {
                font-size: 12px;
            }
        }
    </style>
    """, unsafe_allow_html=True)
    
    # GENERATE HEADER HTML with Animated DAG Logo
    if st.session_state.get('authentication_status'):
        user_name = st.session_state.get('name', 'User')
        is_premium = st.session_state.get('is_premium', False)
        
        if is_premium:
            status_text = "👑 PREMIUM"
            status_class = "premium"
            
            if st.session_state.get('premium_expires_at'):
                try:
                    from datetime import datetime
                    expires = datetime.fromisoformat(str(st.session_state['premium_expires_at']).replace('Z', '+00:00'))
                    days_left = (expires - datetime.now()).days
                    if days_left > 0:
                        status_text += f" ({days_left}d left)"
                    elif days_left == 0:
                        status_text += " (Expires today)"
                    else:
                        status_text = "🔒 EXPIRED"
                        status_class = "free"
                except:
                    pass
        else:
            status_text = "🔒 FREE TIER"
            status_class = "free"
        
        header_html = f"""
        <div class="kaspa-header">
            <div class="kaspa-logo">
                <svg class="dag-logo-header" viewBox="0 0 120 40" xmlns="http://www.w3.org/2000/svg">
                    <rect class="dag-block-header block1-header" x="8" y="18" width="6" height="6"></rect>
                    <rect class="dag-block-header block2-header" x="20" y="12" width="6" height="6"></rect>
                    <rect class="dag-block-header block3-header" x="20" y="18" width="6" height="6"></rect>
                    <rect class="dag-block-header block4-header" x="20" y="24" width="6" height="6"></rect>
                    <rect class="dag-block-header block5-header" x="32" y="15" width="6" height="6"></rect>
                    <rect class="dag-block-header block6-header" x="32" y="21" width="6" height="6"></rect>
                    
                    <line class="dag-connection-header conn1-header" x1="14" y1="21" x2="20" y2="15"></line>
                    <line class="dag-connection-header conn2-header" x1="14" y1="21" x2="20" y2="21"></line>
                    <line class="dag-connection-header conn3-header" x1="14" y1="21" x2="20" y2="27"></line>
                    <line class="dag-connection-header conn4-header" x1="26" y1="15" x2="32" y2="18"></line>
                    <line class="dag-connection-header conn5-header" x1="26" y1="21" x2="32" y2="24"></line>
                </svg>
                <span>Kaspa Analytics</span>
            </div>
            <div class="kaspa-user-info">
                <div>Welcome, {user_name}</div>
                <div class="kaspa-user-status {status_class}">{status_text}</div>
            </div>
        </div>
        """
    else:
        header_html = """
        <div class="kaspa-header">
            <div class="kaspa-logo">
                <svg class="dag-logo-header" viewBox="0 0 120 40" xmlns="http://www.w3.org/2000/svg">
                    <rect class="dag-block-header block1-header" x="8" y="18" width="6" height="6"></rect>
                    <rect class="dag-block-header block2-header" x="20" y="12" width="6" height="6"></rect>
                    <rect class="dag-block-header block3-header" x="20" y="18" width="6" height="6"></rect>
                    <rect class="dag-block-header block4-header" x="20" y="24" width="6" height="6"></rect>
                    <rect class="dag-block-header block5-header" x="32" y="15" width="6" height="6"></rect>
                    <rect class="dag-block-header block6-header" x="32" y="21" width="6" height="6"></rect>
                    
                    <line class="dag-connection-header conn1-header" x1="14" y1="21" x2="20" y2="15"></line>
                    <line class="dag-connection-header conn2-header" x1="14" y1="21" x2="20" y2="21"></line>
                    <line class="dag-connection-header conn3-header" x1="14" y1="21" x2="20" y2="27"></line>
                    <line class="dag-connection-header conn4-header" x1="26" y1="15" x2="32" y2="18"></line>
                    <line class="dag-connection-header conn5-header" x1="26" y1="21" x2="32" y2="24"></line>
                </svg>
                <span>Kaspa Analytics</span>
            </div>
            <div class="kaspa-user-info">
                <div>Please log in</div>
                <div class="kaspa-user-status guest">👤 GUEST</div>
            </div>
        </div>
        """
    
    st.markdown(header_html, unsafe_allow_html=True)

    # YOUR ORIGINAL SIDEBAR NAVIGATION - PRESERVED EXACTLY
    # Add home button at top
    if st.sidebar.button("🏠 Home", key="nav_home", use_container_width=True):
        st.switch_page("Home.py")
    
    # Account buttons right under Home
    if st.session_state.get('authentication_status'):
        col1, col2 = st.sidebar.columns(2)
        with col1:
            if st.button("👤 Account", key="nav_account", use_container_width=True):
                st.switch_page("pages/A_👤_Account.py")
        with col2:
            if st.button("🚪 Logout", key="nav_logout", use_container_width=True):
                st.session_state.clear()
                st.switch_page("Home.py")
    else:
        if st.sidebar.button("🔑 Login / Register", key="nav_login", use_container_width=True):
            st.switch_page("pages/0_🔑_Login.py")
    
    st.sidebar.markdown("---")
    
    # Mining Section
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
    
    # Premium Analytics Section
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
            if st.button("👑 Premium Features", key="sidebar_premium_features_free", use_container_width=True):
                st.switch_page("pages/B_👑_Premium_Features.py")
            st.warning("Upgrade Required")
            st.write("**Monthly:** $9.99")
            st.write("**Annual:** $99")
            if st.button("💳 Upgrade Now", key="sidebar_upgrade", use_container_width=True):
                st.switch_page("pages/B_👑_Premium_Features.py")
    else:
        with st.sidebar.expander("👑 Premium Analytics", expanded=False):
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
