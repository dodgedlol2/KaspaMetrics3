import streamlit as st
from footer import add_footer

def add_navigation():
    """Add organized navigation to sidebar AND header (shared across all pages)"""
    
    # CRITICAL FIX: Inject CSS IMMEDIATELY to prevent flickering
    # This runs before Streamlit renders its default header
    st.markdown("""
    <style>
        /* IMMEDIATE COMPLETE HEADER REMOVAL - Multiple targeting approaches */
        header[data-testid="stHeader"] {
            display: none !important;
            visibility: hidden !important;
            height: 0 !important;
            min-height: 0 !important;
            max-height: 0 !important;
        }
        
        /* HIDE ALL STREAMLIT HEADER VARIATIONS */
        [data-testid="stHeader"] {
            display: none !important;
        }
        
        .stApp > header[data-testid="stHeader"] {
            display: none !important;
        }
        
        /* REMOVE THE RUNNING MAN AND LOADING ANIMATIONS */
        [data-testid="stStatusWidget"] {
            display: none !important;
        }
        
        /* HIDE ALL STATUS AND LOADING ELEMENTS */
        div[data-testid*="stStatus"] {
            display: none !important;
        }
        
        /* HIDE TOOLBAR AND MENU */
        .stAppToolbar {
            display: none !important;
        }
        
        div[data-testid="stToolbar"] {
            display: none !important;
        }
        
        [data-testid="stDecoration"] {
            display: none !important;
        }
        
        /* HIDE FOOTER TOO */
        footer {
            display: none !important;
        }
        
        /* REMOVE ANY MARGIN/PADDING FROM TOP */
        .main .block-container {
            padding-top: 90px !important;
        }
        
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
        
        /* ENHANCED SIDEBAR WITH BEAUTIFUL GRADIENT */
        [data-testid="stSidebar"] {
            margin-top: 70px;
            height: calc(100vh - 70px);
            background: linear-gradient(180deg, 
                rgba(15, 20, 25, 0.98) 0%, 
                rgba(30, 41, 59, 0.95) 25%, 
                rgba(15, 23, 42, 0.98) 50%, 
                rgba(20, 30, 45, 0.95) 75%, 
                rgba(15, 20, 25, 0.98) 100%) !important;
            backdrop-filter: blur(25px) !important;
            -webkit-backdrop-filter: blur(25px) !important;
            border-right: 1px solid rgba(0, 212, 255, 0.2) !important;
            box-shadow: 2px 0 20px rgba(0, 0, 0, 0.3) !important;
        }
        
        /* Style sidebar content container */
        [data-testid="stSidebar"] > div {
            background: transparent !important;
            padding-top: 20px !important;
        }
        
        /* Style sidebar buttons with glassmorphism */
        .stButton > button {
            background: linear-gradient(135deg, 
                rgba(30, 41, 59, 0.8) 0%, 
                rgba(15, 23, 42, 0.9) 100%) !important;
            border: 1px solid rgba(100, 116, 139, 0.3) !important;
            border-radius: 12px !important;
            color: #f1f5f9 !important;
            backdrop-filter: blur(15px) !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2) !important;
            font-weight: 600 !important;
        }
        
        .stButton > button:hover {
            background: linear-gradient(135deg, 
                rgba(0, 212, 255, 0.2) 0%, 
                rgba(30, 41, 59, 0.9) 100%) !important;
            border-color: #00d4ff !important;
            box-shadow: 0 8px 32px rgba(0, 212, 255, 0.2), 
                        0 0 0 1px rgba(0, 212, 255, 0.3) !important;
            transform: translateY(-2px) !important;
        }
        
        /* Style expanders - COMPLETELY CLEAN, NO BACKGROUNDS */
        
        /* Target details elements (the actual expanders) */
        [data-testid="stSidebar"] details {
            border: none !important;  /* Completely remove border */
            outline: none !important;
            background: transparent !important;  /* Remove default background */
            border-radius: 0 !important;  /* Remove border radius */
            backdrop-filter: none !important;  /* Remove backdrop filter */
            box-shadow: none !important;  /* Remove any shadow */
            margin: 0 !important;
            padding: 0 !important;
        }
        
        /* Also target any wrapper divs around details */
        [data-testid="stSidebar"] details > div {
            border: none !important;
            background: transparent !important;
            box-shadow: none !important;
        }
        
        /* Style the summary (clickable header) - NO BACKGROUND */
        [data-testid="stSidebar"] summary {
            border: none !important;  /* No border on summary either */
            outline: none !important;
            background: transparent !important;  /* NO BACKGROUND - completely transparent */
            color: #e2e8f0 !important;
            font-weight: 600 !important;
            cursor: pointer !important;
            border-radius: 0 !important;  /* No border radius */
            padding: 8px 12px !important;
            backdrop-filter: none !important;  /* No backdrop filter */
            margin: 0 !important;
        }
        
        /* Hover effect for summary - still no background, just text color change */
        [data-testid="stSidebar"] summary:hover {
            background: transparent !important;  /* Keep transparent on hover */
            color: #00d4ff !important;  /* Just change text color on hover */
            box-shadow: none !important;
        }
        
        /* Make sure content area is also transparent */
        [data-testid="stSidebar"] details[open] {
            border: none !important;
            background: transparent !important;
            box-shadow: none !important;
        }
        
        /* Style sidebar text */
        [data-testid="stSidebar"] .stMarkdown {
            color: #cbd5e1 !important;
        }
        
        /* Style warning/info/success boxes in sidebar */
        [data-testid="stSidebar"] .stAlert {
            background: linear-gradient(135deg, 
                rgba(30, 41, 59, 0.8) 0%, 
                rgba(15, 23, 42, 0.9) 100%) !important;
            border: 1px solid rgba(100, 116, 139, 0.3) !important;
            border-radius: 8px !important;
            backdrop-filter: blur(10px) !important;
            color: #e2e8f0 !important;
        }
        
        /* ENHANCED SIDEBAR CONTROLS - Single functional button */
        
        /* Collapse button when sidebar is OPEN - Make it invisible */
        div[data-testid="stSidebarCollapseButton"] {
            position: fixed !important;
            top: calc(85px - 2cm) !important;  /* Moved 2cm up */
            left: calc(21rem - 2cm) !important;  /* Moved 2cm to the left */
            z-index: 999999 !important;
            background: transparent !important;  /* Made transparent */
            border: none !important;  /* Remove border */
            backdrop-filter: none !important;  /* Remove backdrop filter */
        }

        /* Make the collapse button completely invisible */
        div[data-testid="stSidebarCollapseButton"] button {
            background: transparent !important;
            border: none !important;
            opacity: 0 !important;  /* Completely invisible */
            pointer-events: auto !important;
            cursor: pointer !important;
        }

        /* Expand button when sidebar is COLLAPSED - Clean hamburger only */
        div[data-testid="stSidebarCollapsedControl"] {
            position: fixed !important;
            top: 85px !important;  /* Just below header */
            left: 20px !important;  /* Moved 10px to the right (was 10px, now 20px) */
            z-index: 999998 !important;
            background: transparent !important;  /* Remove dark background */
            border: none !important;  /* Remove border */
            backdrop-filter: none !important;  /* Remove backdrop filter */
            box-shadow: none !important;  /* Remove shadow */
            width: 40px !important;
            height: 40px !important;
        }

        /* Style the expand button - clean and minimal */
        div[data-testid="stSidebarCollapsedControl"] button,
        button[data-testid="collapsedControl"] {
            background: transparent !important;
            border: none !important;
            width: 100% !important;
            height: 100% !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            font-size: 0 !important;  /* Hide original > text */
            cursor: pointer !important;
            position: relative !important;
            color: transparent !important;  /* Hide any default text */
        }

        /* Add custom hamburger icon - grey by default */
        div[data-testid="stSidebarCollapsedControl"] button::before,
        button[data-testid="collapsedControl"]::before {
            content: "☰" !important;
            font-size: 18px !important;
            color: #9ca3af !important;  /* Grey color */
            transition: all 0.3s ease !important;
            display: block !important;
            line-height: 1 !important;
        }

        /* Light blue glow on hover and click */
        div[data-testid="stSidebarCollapsedControl"]:hover button::before,
        div[data-testid="stSidebarCollapsedControl"]:active button::before,
        button[data-testid="collapsedControl"]:hover::before,
        button[data-testid="collapsedControl"]:active::before {
            color: #00d4ff !important;
            text-shadow: 0 0 8px rgba(0, 212, 255, 0.8) !important;
            transform: scale(1.1) !important;
            transition: all 0.2s ease !important;
        }

        /* Ensure the functional button remains clickable */
        div[data-testid="stSidebarCollapsedControl"] button,
        button[data-testid="collapsedControl"] {
            pointer-events: auto !important;
            cursor: pointer !important;
        }
        
        /* HEADER STYLING WITH DATA MATRIX LOGO */
        .kaspa-logo {
            display: flex;
            align-items: center;
            gap: 12px;
            font-family: 'SF Pro Display', -apple-system, sans-serif;
            font-size: 22px;
            font-weight: 600;
            color: #ffffff;
        }
        
        .matrix {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 2px;
            width: 29px;
            height: 29px;
        }
        
        .cell {
            width: 7px;
            height: 7px;
            background: linear-gradient(45deg, #e5e7eb, #9ca3af, #6b7280);
            border-radius: 1px;
            box-shadow: 
                0 0 7px rgba(156, 163, 175, 0.6),
                inset 0 1px 1px rgba(255, 255, 255, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .cell:nth-child(1) { 
            opacity: 1; 
            background: linear-gradient(45deg, #00d4ff, #0ea5e9); 
            box-shadow: 0 0 9px rgba(0, 212, 255, 0.8), inset 0 1px 1px rgba(255, 255, 255, 0.3); 
        }
        .cell:nth-child(2) { opacity: 0.9; }
        .cell:nth-child(3) { 
            opacity: 0.7; 
            background: linear-gradient(45deg, #00d4ff, #0ea5e9); 
            box-shadow: 0 0 9px rgba(0, 212, 255, 0.8), inset 0 1px 1px rgba(255, 255, 255, 0.3); 
        }
        .cell:nth-child(4) { opacity: 0.8; }
        .cell:nth-child(5) { 
            opacity: 1; 
            background: linear-gradient(45deg, #00d4ff, #0ea5e9); 
            box-shadow: 0 0 9px rgba(0, 212, 255, 0.8), inset 0 1px 1px rgba(255, 255, 255, 0.3); 
        }
        .cell:nth-child(6) { opacity: 0.8; }
        .cell:nth-child(7) { 
            opacity: 0.6; 
            background: linear-gradient(45deg, #00d4ff, #0ea5e9); 
            box-shadow: 0 0 9px rgba(0, 212, 255, 0.8), inset 0 1px 1px rgba(255, 255, 255, 0.3); 
        }
        .cell:nth-child(8) { opacity: 0.9; }
        .cell:nth-child(9) { 
            opacity: 0.5; 
            background: linear-gradient(45deg, #00d4ff, #0ea5e9); 
            box-shadow: 0 0 9px rgba(0, 212, 255, 0.8), inset 0 1px 1px rgba(255, 255, 255, 0.3); 
        }
        
        .logo-text { 
            color: #ffffff; 
            letter-spacing: -0.5px;
            background: linear-gradient(45deg, #f8fafc, #e2e8f0, #cbd5e1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
            font-weight: 700;
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
        
        /* PREVENT BODY OVERFLOW DURING TRANSITIONS */
        body {
            overflow-x: hidden;
        }
        
        /* SMOOTH TRANSITIONS FOR ALL ELEMENTS */
        * {
            transition: none !important;
        }
        
        /* Google Material Icons styling */
        .material-icons {
            font-family: 'Material Icons';
            font-weight: normal;
            font-style: normal;
            font-size: 18px;
            line-height: 1;
            letter-spacing: normal;
            text-transform: none;
            display: inline-block;
            white-space: nowrap;
            word-wrap: normal;
            direction: ltr;
            vertical-align: middle;
            margin-right: 8px;
        }
        
        /* Icon color in sidebar */
        [data-testid="stSidebar"] .material-icons {
            color: #cbd5e1 !important;
        }
        
        /* Icon color on hover */
        .stButton:hover .material-icons {
            color: #00d4ff !important;
        }
        @media (max-width: 768px) {
            .kaspa-header {
                padding: 0 1rem;
            }
            
            .kaspa-logo {
                font-size: 17px;
                gap: 10px;
            }
            
            .matrix {
                width: 22px;
                height: 22px;
            }
            
            .cell {
                width: 5px;
                height: 5px;
            }
            
            .kaspa-user-info {
                font-size: 12px;
            }
        }
    </style>
    """, unsafe_allow_html=True)
    
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
                <div class="matrix">
                    <div class="cell"></div>
                    <div class="cell"></div>
                    <div class="cell"></div>
                    <div class="cell"></div>
                    <div class="cell"></div>
                    <div class="cell"></div>
                    <div class="cell"></div>
                    <div class="cell"></div>
                    <div class="cell"></div>
                </div>
                <span class="logo-text">Kaspa Metrics</span>
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
                <div class="matrix">
                    <div class="cell"></div>
                    <div class="cell"></div>
                    <div class="cell"></div>
                    <div class="cell"></div>
                    <div class="cell"></div>
                    <div class="cell"></div>
                    <div class="cell"></div>
                    <div class="cell"></div>
                    <div class="cell"></div>
                </div>
                <span class="logo-text">Kaspa Metrics</span>
            </div>
            <div class="kaspa-user-info">
                <div>Please log in</div>
                <div class="kaspa-user-status guest">👤 GUEST</div>
            </div>
        </div>
        """
    
    st.markdown(header_html, unsafe_allow_html=True)

    # Add home button at top - Material Icon for consistency
    if st.sidebar.button("Home", key="nav_home", use_container_width=True, icon=":material/home:"):
        st.switch_page("Home.py")
    
    # Account buttons right under Home - with Material Icons
    if st.session_state.get('authentication_status'):
        # User is logged in - show Account and Logout side by side
        col1, col2 = st.sidebar.columns(2)
        with col1:
            if st.button("Account", key="nav_account", use_container_width=True, icon=":material/account_circle:"):
                st.switch_page("pages/A_👤_Account.py")
        with col2:
            if st.button("Logout", key="nav_logout", use_container_width=True, icon=":material/logout:"):
                st.session_state.clear()
                st.switch_page("Home.py")
    else:
        # User not logged in - full width with Material Icon
        if st.sidebar.button("Login / Register", key="nav_login", use_container_width=True, icon=":material/login:"):
            st.switch_page("pages/0_🔑_Login.py")
    
    st.sidebar.markdown("---")
    
    # Mining Section - with Material Icons (monochrome)
    with st.sidebar.expander("⛏ Mining", expanded=True):
        if st.button("Hashrate", key="sidebar_hashrate", use_container_width=True, icon=":material/trending_up:"):
            st.switch_page("pages/1_⛏️_Mining_Hashrate.py")
        if st.button("Difficulty", key="sidebar_difficulty", use_container_width=True, icon=":material/settings:"):
            st.switch_page("pages/2_⛏️_Mining_Difficulty.py")
    
    # Spot Section - ADDING MATERIAL ICON TO HEADER
    with st.sidebar.expander("", expanded=True):
        st.markdown("### 📊 Spot Market")  # Using a chart icon that's more monochrome
        if st.button("Price", key="sidebar_price", use_container_width=True, icon=":material/attach_money:"):
            st.switch_page("pages/3_💰_Spot_Price.py")
        if st.button("Volume", key="sidebar_volume", use_container_width=True, icon=":material/bar_chart:"):
            st.switch_page("pages/4_💰_Spot_Volume.py")
        if st.button("Market Cap", key="sidebar_marketcap", use_container_width=True, icon=":material/account_balance:"):
            st.switch_page("pages/5_💰_Spot_Market_Cap.py")
    
    # Social Section - ADDING MATERIAL ICON TO HEADER  
    with st.sidebar.expander("", expanded=True):
        st.markdown("### 👥 Social Data")  # Using people icon that's more monochrome
        if st.button("Social Metrics", key="sidebar_social1", use_container_width=True, icon=":material/analytics:"):
            st.switch_page("pages/6_📱_Social_Metrics.py")
        if st.button("Social Trends", key="sidebar_social2", use_container_width=True, icon=":material/show_chart:"):
            st.switch_page("pages/7_📱_Social_Trends.py")
    
    # Premium Analytics Section - PRESERVED EXACTLY with all access control logic and emoji icons
    if st.session_state.get('authentication_status') and st.session_state.get('is_premium'):
        with st.sidebar.expander("👑 Premium Analytics", expanded=True):
            if st.button("Premium Features", key="sidebar_premium_features", use_container_width=True, icon=":material/star:"):
                st.switch_page("pages/B_👑_Premium_Features.py")
            if st.button("Premium Analytics", key="sidebar_premium1", use_container_width=True, icon=":material/science:"):
                st.switch_page("pages/8_👑_Premium_Analytics.py")
            if st.button("Advanced Metrics", key="sidebar_premium2", use_container_width=True, icon=":material/insights:"):
                st.switch_page("pages/9_👑_Advanced_Metrics.py")
    elif st.session_state.get('authentication_status'):
        with st.sidebar.expander("👑 Premium Analytics", expanded=False):
            # Premium Features accessible to logged-in users (but not paying)
            if st.button("Premium Features", key="sidebar_premium_features_free", use_container_width=True, icon=":material/star:"):
                st.switch_page("pages/B_👑_Premium_Features.py")
            st.warning("Upgrade Required")
            st.write("**Monthly:** $9.99")
            st.write("**Annual:** $99")
            if st.button("Upgrade Now", key="sidebar_upgrade", use_container_width=True, icon=":material/credit_card:"):
                st.switch_page("pages/B_👑_Premium_Features.py")
    else:
        with st.sidebar.expander("👑 Premium Analytics", expanded=False):
            # Premium Features accessible to everyone (including non-logged users)
            if st.button("Premium Features", key="sidebar_premium_features_guest", use_container_width=True, icon=":material/star:"):
                st.switch_page("pages/B_👑_Premium_Features.py")
            st.info("Login Required")
            st.write("Sign in to access premium analytics")
            if st.button("Login", key="sidebar_login_premium", use_container_width=True, icon=":material/login:"):
                st.switch_page("pages/0_🔑_Login.py")
    
    # Removed the status section - no more "ℹ️ Status" display
