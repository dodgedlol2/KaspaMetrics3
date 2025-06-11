import streamlit as st

def add_navigation():
    """Add organized navigation to sidebar AND header (shared across all pages)"""
    
    # IMPROVED HEADER CSS - Fixed positioning and sidebar interactions
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
            z-index: 999997;  /* Lower than sidebar controls but higher than content */
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
        
        /* PUSH MAIN CONTENT DOWN - Critical for preventing overlap */
        .main .block-container {
            padding-top: 90px !important;
        }
        
        /* SIDEBAR POSITIONING - Move down to avoid header overlap */
        [data-testid="stSidebar"] {
            margin-top: 70px;
            height: calc(100vh - 70px);
        }
        
        /* SIDEBAR CONTROLS - Fixed positioning to prevent scrolling */
        
        /* Collapse button when sidebar is OPEN - FIXED to viewport */
        div[data-testid="stSidebarCollapseButton"] {
            position: fixed !important;
            top: calc(85px - 2cm) !important;  /* Moved 2cm up */
            left: calc(21rem - 2cm) !important;  /* Moved 2cm to the left */
            z-index: 999999 !important;
            background: transparent !important;  /* Made transparent */
            border: none !important;  /* Remove border */
            backdrop-filter: none !important;  /* Remove backdrop filter */
        }
        
        /* Make the button inside transparent too */
        div[data-testid="stSidebarCollapseButton"] button {
            background: transparent !important;
            border: none !important;
            opacity: 0 !important;  /* Completely invisible */
        }
        
        /* Expand button when sidebar is COLLAPSED - also fixed */
        div[data-testid="stSidebarCollapsedControl"] {
            position: fixed !important;
            top: 85px !important;  /* Just below header */
            left: 0px !important;
            z-index: 999998 !important;
        }
        
        /* Ensure all sidebar buttons remain clickable */
        div[data-testid="stSidebarCollapseButton"] button,
        div[data-testid="stSidebarCollapsedControl"] button,
        button[data-testid="collapsedControl"] {
            pointer-events: auto !important;
            cursor: pointer !important;
            background: rgba(255, 255, 255, 0.1) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
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
        
        /* SVG Logo specific styling */
        .kaspa-logo svg {
            height: 50px;
            width: 167px; /* Maintains 400:120 aspect ratio */
            display: block;
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
        
        /* HIDE NATIVE PAGE NAVIGATION - Your original working code */
        .css-1q1n0ol[data-testid="stSidebarNav"] {
            display: none;
        }
        
        div[data-testid="stSidebarNav"] {
            display: none;
        }
        
        section[data-testid="stSidebar"] nav {
            display: none;
        }
        
        /* Ensure sidebar content remains visible */
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
            }
            
            .kaspa-logo svg {
                height: 40px;
                width: 133px; /* Maintains 400:120 aspect ratio */
            }
            
            .kaspa-user-info {
                font-size: 12px;
            }
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Simple GhostDAG Logo without animations
    svg_logo = """<svg viewBox="0 0 400 120" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="ghostGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#00d4ff" />
                <stop offset="100%" stop-color="#7c3aed" />
            </linearGradient>
        </defs>
        
        <!-- Main chain -->
        <circle cx="30" cy="60" r="8" fill="#00d4ff" />
        <circle cx="70" cy="60" r="8" fill="#00d4ff" />
        <circle cx="110" cy="60" r="8" fill="#00d4ff" />
        <line x1="38" y1="60" x2="62" y2="60" stroke="#00d4ff" stroke-width="3" />
        <line x1="78" y1="60" x2="102" y2="60" stroke="#00d4ff" stroke-width="3" />
        
        <!-- Ghost nodes -->
        <circle cx="50" cy="30" r="6" fill="url(#ghostGrad)" opacity="0.7" />
        <circle cx="90" cy="30" r="6" fill="url(#ghostGrad)" opacity="0.7" />
        <circle cx="50" cy="90" r="6" fill="url(#ghostGrad)" opacity="0.7" />
        <circle cx="90" cy="90" r="6" fill="url(#ghostGrad)" opacity="0.7" />
        
        <!-- Ghost connections -->
        <line x1="35" y1="54" x2="45" y2="36" stroke="#7c3aed" stroke-width="2" opacity="0.5" stroke-dasharray="4 2" />
        <line x1="55" y1="36" x2="65" y2="54" stroke="#7c3aed" stroke-width="2" opacity="0.5" stroke-dasharray="4 2" />
        <line x1="75" y1="54" x2="85" y2="36" stroke="#7c3aed" stroke-width="2" opacity="0.5" stroke-dasharray="4 2" />
        <line x1="95" y1="36" x2="105" y2="54" stroke="#7c3aed" stroke-width="2" opacity="0.5" stroke-dasharray="4 2" />
        <line x1="35" y1="66" x2="45" y2="84" stroke="#7c3aed" stroke-width="2" opacity="0.5" stroke-dasharray="4 2" />
        <line x1="55" y1="84" x2="65" y2="66" stroke="#7c3aed" stroke-width="2" opacity="0.5" stroke-dasharray="4 2" />
        <line x1="75" y1="66" x2="85" y2="84" stroke="#7c3aed" stroke-width="2" opacity="0.5" stroke-dasharray="4 2" />
        <line x1="95" y1="84" x2="105" y2="66" stroke="#7c3aed" stroke-width="2" opacity="0.5" stroke-dasharray="4 2" />
        
        <!-- Logo text -->
        <text x="140" y="50" font-family="Arial, sans-serif" font-size="28" font-weight="700" fill="#00d4ff">Kaspa</text>
        <text x="230" y="50" font-family="Arial, sans-serif" font-size="28" font-weight="300" fill="#7c3aed">Metrics</text>
        <text x="140" y="75" font-family="Arial, sans-serif" font-size="12" font-weight="400" fill="#94a3b8" letter-spacing="2">GHOSTDAG</text>
    </svg>"""
    
    # GENERATE HEADER HTML - Improved with better user status handling
    if st.session_state.get('authentication_status'):
        user_name = st.session_state.get('name', 'User')
        is_premium = st.session_state.get('is_premium', False)
        
        # Better status display with expiration info
        if is_premium:
            status_text = "👑 PREMIUM"
            status_class = "premium"
            
            # Add expiration info if available
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
                {svg_logo}
            </div>
            <div class="kaspa-user-info">
                <div>Welcome, {user_name}</div>
                <div class="kaspa-user-status {status_class}">{status_text}</div>
            </div>
        </div>
        """
    else:
        header_html = f"""
        <div class="kaspa-header">
            <div class="kaspa-logo">
                {svg_logo}
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
    
    # Premium Analytics Section - PRESERVED EXACTLY with all access control logic
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
    
    # Footer info - PRESERVED EXACTLY
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
