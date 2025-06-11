import streamlit as st

def add_navigation():
    """Add organized navigation to sidebar AND header (shared across all pages)"""
    
    # SIMPLIFIED HEADER - Let Streamlit handle sidebar behavior naturally
    st.markdown("""
    <style>
        /* FIXED HEADER - Simple and clean */
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
        
        /* PUSH MAIN CONTENT DOWN */
        .main .block-container {
            padding-top: 90px !important;
        }
        
        /* MOVE SIDEBAR DOWN */
        [data-testid="stSidebar"] {
            margin-top: 70px;
            height: calc(100vh - 70px);
        }
        
        /* SIDEBAR CONTROLS - Keep them functional but invisible */
        div[data-testid="stSidebarCollapseButton"] {
            position: fixed !important;
            top: calc(85px - 2cm) !important;
            z-index: 999999 !important;
            background: transparent !important;
            border: none !important;
        }
        
        div[data-testid="stSidebarCollapseButton"] button {
            background: transparent !important;
            border: none !important;
            opacity: 0 !important;
        }
        
        div[data-testid="stSidebarCollapsedControl"] {
            top: 85px !important;
            z-index: 999998 !important;
            position: fixed !important;
        }
        
        /* HEADER STYLING */
        .kaspa-logo {
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 24px;
            font-weight: 700;
            color: #00d4ff;
            text-shadow: 0 0 10px rgba(0, 212, 255, 0.3);
        }
        
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
        
        /* RESPONSIVE DESIGN */
        @media (max-width: 768px) {
            .kaspa-header {
                padding: 0 1rem;
            }
            
            .kaspa-logo {
                font-size: 20px;
            }
            
            .kaspa-user-info {
                font-size: 12px;
            }
        }
    </style>
    """, unsafe_allow_html=True)
    
    # GENERATE HEADER HTML
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
                <span>⚡ Kaspa Analytics</span>
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
                <span>⚡ Kaspa Analytics</span>
            </div>
            <div class="kaspa-user-info">
                <div>Please log in</div>
                <div class="kaspa-user-status guest">👤 GUEST</div>
            </div>
        </div>
        """
    
    st.markdown(header_html, unsafe_allow_html=True)

    # STREAMLIT NATIVE HOVER ZONE - NO JAVASCRIPT
    st.markdown("""
    <style>
    /* Make sidebar visible and positioned normally */
    [data-testid="stSidebar"] {
        margin-top: 70px !important;
        height: calc(100vh - 70px) !important;
        position: relative !important;
        z-index: 999996 !important;
        transition: margin-left 0.3s ease !important;
    }
    
    /* CSS-ONLY HOVER ZONE with pure CSS interactions */
    .hover-zone-css {
        position: fixed !important;
        top: 70px !important;
        left: 0 !important;
        width: 200px !important;
        height: calc(100vh - 70px) !important;
        background: rgba(0, 212, 255, 0.2) !important;
        z-index: 999995 !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
    }
    
    .hover-zone-css::after {
        content: "HOVER ZONE\\A200px wide\\AMouse over me!";
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        color: white;
        font-weight: bold;
        text-align: center;
        white-space: pre;
        font-size: 14px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.8);
    }
    
    /* CSS HOVER EFFECTS - Sidebar slides in on hover */
    .hover-zone-css:hover {
        background: rgba(0, 212, 255, 0.4) !important;
    }
    
    /* When hovering the zone, show sidebar at full opacity and push content */
    .hover-zone-css:hover ~ [data-testid="stSidebar"] {
        margin-left: 0px !important;
        opacity: 1 !important;
    }
    
    .hover-zone-css:hover ~ .main .block-container {
        margin-left: 200px !important;
        width: calc(100vw - 200px - 2rem) !important;
    }
    
    /* When NOT hovering, sidebar stays normal but content adjusts for hover zone */
    .main .block-container {
        padding-top: 90px !important;
        margin-left: 0px !important;
        transition: all 0.3s ease !important;
    }
    
    /* Hide the expand button since we don't need it */
    [data-testid="stSidebarCollapsedControl"] {
        display: none !important;
    }
    
    /* Keep collapse button visible */
    [data-testid="stSidebarCollapseButton"] {
        display: block !important;
        z-index: 999998 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # CSS-ONLY HOVER ZONE ELEMENT
    st.markdown("""
    <div class="hover-zone-css"></div>
    """, unsafe_allow_html=True)

    # YOUR ORIGINAL SIDEBAR NAVIGATION - UNCHANGED
    if st.sidebar.button("🏠 Home", key="nav_home", use_container_width=True):
        st.switch_page("Home.py")
    
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
