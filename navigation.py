import streamlit as st
from footer import add_footer

def add_navigation():
    """Add organized navigation to sidebar AND header (shared across all pages)"""
    
    # CRITICAL FIX: Inject CSS IMMEDIATELY to prevent flickering
    # This runs before Streamlit renders its default header
    st.markdown("""
    <style>
        /* Import modern fonts - Inter and Space Grotesk */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
        
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
        
        /* LUNARCRUSH-STYLE BLACK HEADER */
        .kaspa-header {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            width: 100vw;
            height: 70px;
            z-index: 999997;
            /* Pure black background with subtle gradient */
            background: linear-gradient(180deg, 
                #000000 0%,
                #000000 85%,
                rgba(0, 0, 0, 0.95) 100%);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 2rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            box-shadow: 
                0 1px 0 rgba(255, 255, 255, 0.05) inset,
                0 -1px 0 rgba(0, 0, 0, 0.2) inset,
                0 2px 24px rgba(0, 0, 0, 0.5);
        }
        
        /* PUSH MAIN CONTENT DOWN - Critical for preventing overlap */
        .main .block-container {
            padding-top: 90px !important;
        }
        
        /* LUNARCRUSH-STYLE BLACK SIDEBAR */
        [data-testid="stSidebar"] {
            margin-top: 70px;
            height: calc(100vh - 70px);
            position: relative !important;
            overflow: hidden !important;
            /* Pure black with subtle depth */
            background: linear-gradient(180deg,
                #000000 0%,
                #050505 50%,
                #000000 100%);
            backdrop-filter: blur(20px) !important;
            -webkit-backdrop-filter: blur(20px) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
            box-shadow: 
                inset 1px 0 0 rgba(255, 255, 255, 0.03),
                2px 0 24px rgba(0, 0, 0, 0.5) !important;
        }
        
        /* Animated accent line */
        [data-testid="stSidebar"]::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 1px;
            height: 100%;
            background: linear-gradient(180deg,
                transparent 0%,
                rgba(0, 212, 255, 0.5) 20%,
                rgba(0, 212, 255, 0.8) 50%,
                rgba(0, 212, 255, 0.5) 80%,
                transparent 100%);
            animation: slideAccent 6s ease-in-out infinite;
        }
        
        @keyframes slideAccent {
            0%, 100% { transform: translateY(-100%); }
            50% { transform: translateY(100%); }
        }
        
        /* Style sidebar content container */
        [data-testid="stSidebar"] > div {
            background: transparent !important;
            padding-top: 20px !important;
        }
        
        /* Modern sidebar buttons */
        [data-testid="stSidebar"] .stButton > button {
            background: rgba(255, 255, 255, 0.03) !important;
            border: 1px solid rgba(255, 255, 255, 0.06) !important;
            border-radius: 8px !important;
            color: #ffffff !important;
            font-family: 'Inter', -apple-system, sans-serif !important;
            font-weight: 500 !important;
            backdrop-filter: blur(10px) !important;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 
                0 1px 2px rgba(0, 0, 0, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.03) !important;
            text-align: left !important;
            justify-content: flex-start !important;
            display: flex !important;
            align-items: center !important;
            font-size: 13px !important;
            letter-spacing: 0.01em !important;
            position: relative !important;
            overflow: hidden !important;
        }
        
        /* Button hover state */
        [data-testid="stSidebar"] .stButton > button:hover {
            background: rgba(0, 212, 255, 0.1) !important;
            border-color: rgba(0, 212, 255, 0.3) !important;
            color: #00d4ff !important;
            transform: translateX(2px) !important;
            box-shadow: 
                0 0 20px rgba(0, 212, 255, 0.2),
                0 2px 8px rgba(0, 0, 0, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.05) !important;
        }
        
        /* Subtle glow effect on hover */
        [data-testid="stSidebar"] .stButton > button::after {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            background: radial-gradient(circle, rgba(0, 212, 255, 0.3) 0%, transparent 70%);
            transform: translate(-50%, -50%);
            transition: width 0.3s ease, height 0.3s ease;
        }
        
        [data-testid="stSidebar"] .stButton > button:hover::after {
            width: 100%;
            height: 100%;
        }
        
        /* Target button text specifically inside sidebar */
        [data-testid="stSidebar"] .stButton > button span,
        [data-testid="stSidebar"] .stButton > button p,
        [data-testid="stSidebar"] .stButton > button div {
            font-size: 13px !important;
            font-family: 'Inter', -apple-system, sans-serif !important;
        }
        
        /* Target button text content more specifically */
        [data-testid="stSidebar"] button[kind="secondary"] {
            font-size: 13px !important;
        }
        
        [data-testid="stSidebar"] button[kind="secondary"] span {
            font-size: 13px !important;
        }
        
        /* Style expanders - COMPLETELY CLEAN, NO BACKGROUNDS */
        
        /* Target details elements (the actual expanders) */
        [data-testid="stSidebar"] details {
            border: none !important;
            outline: none !important;
            background: transparent !important;
            border-radius: 0 !important;
            backdrop-filter: none !important;
            box-shadow: none !important;
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
            border: none !important;
            outline: none !important;
            background: transparent !important;
            color: #ffffff !important;
            font-family: 'Inter', -apple-system, sans-serif !important;
            font-weight: 600 !important;
            font-size: 14px !important;
            letter-spacing: 0.02em !important;
            cursor: pointer !important;
            border-radius: 0 !important;
            padding: 8px 12px !important;
            backdrop-filter: none !important;
            margin: 0 !important;
            transition: all 0.2s ease !important;
        }
        
        /* Hover effect for summary */
        [data-testid="stSidebar"] summary:hover {
            background: transparent !important;
            color: #00d4ff !important;
            box-shadow: none !important;
            transform: translateX(4px) !important;
        }
        
        /* Make sure content area is also transparent */
        [data-testid="stSidebar"] details[open] {
            border: none !important;
            background: transparent !important;
            box-shadow: none !important;
        }
        
        /* Style sidebar text */
        [data-testid="stSidebar"] .stMarkdown {
            color: rgba(255, 255, 255, 0.8) !important;
            font-family: 'Inter', -apple-system, sans-serif !important;
        }
        
        /* Modern warning/info/success boxes in sidebar */
        [data-testid="stSidebar"] .stAlert {
            background: rgba(255, 255, 255, 0.03) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 8px !important;
            backdrop-filter: blur(10px) !important;
            color: rgba(255, 255, 255, 0.9) !important;
            font-family: 'Inter', -apple-system, sans-serif !important;
            box-shadow: 
                0 2px 8px rgba(0, 0, 0, 0.2),
                inset 0 1px 0 rgba(255, 255, 255, 0.03) !important;
        }
        
        /* ENHANCED SIDEBAR CONTROLS - Single functional button */
        
        /* Collapse button when sidebar is OPEN - Make it invisible */
        div[data-testid="stSidebarCollapseButton"] {
            position: fixed !important;
            top: calc(85px - 2cm) !important;
            left: calc(21rem - 2cm) !important;
            z-index: 999999 !important;
            background: transparent !important;
            border: none !important;
            backdrop-filter: none !important;
        }

        /* Make the collapse button completely invisible */
        div[data-testid="stSidebarCollapseButton"] button {
            background: transparent !important;
            border: none !important;
            opacity: 0 !important;
            pointer-events: auto !important;
            cursor: pointer !important;
        }

        /* Expand button when sidebar is COLLAPSED - Modern style */
        div[data-testid="stSidebarCollapsedControl"] {
            position: fixed !important;
            top: 85px !important;
            left: 20px !important;
            z-index: 999998 !important;
            background: transparent !important;
            border: none !important;
            backdrop-filter: none !important;
            box-shadow: none !important;
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
            font-size: 0 !important;
            cursor: pointer !important;
            position: relative !important;
            color: transparent !important;
        }

        /* Add custom hamburger icon - white/grey */
        div[data-testid="stSidebarCollapsedControl"] button::before,
        button[data-testid="collapsedControl"]::before {
            content: "☰" !important;
            font-size: 20px !important;
            color: rgba(255, 255, 255, 0.5) !important;
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
            text-shadow: 0 0 10px rgba(0, 212, 255, 0.8) !important;
            transform: scale(1.1) !important;
        }

        /* Ensure the functional button remains clickable */
        div[data-testid="stSidebarCollapsedControl"] button,
        button[data-testid="collapsedControl"] {
            pointer-events: auto !important;
            cursor: pointer !important;
        }
        
        /* MODERN HEADER STYLING WITH DATA MATRIX LOGO */
        .kaspa-logo {
            display: flex;
            align-items: center;
            gap: 14px;
            font-family: 'Space Grotesk', -apple-system, sans-serif;
            font-size: 24px;
            font-weight: 700;
            color: #ffffff;
        }
        
        /* Enhanced matrix with modern animation */
        .matrix {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 2px;
            width: 32px;
            height: 32px;
            position: relative;
        }
        
        .cell {
            width: 8px;
            height: 8px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 1px;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        /* Active cells with modern glow */
        .cell:nth-child(1), 
        .cell:nth-child(3), 
        .cell:nth-child(5), 
        .cell:nth-child(7), 
        .cell:nth-child(9) {
            background: linear-gradient(135deg, #00d4ff, #0080ff);
            box-shadow: 
                0 0 20px rgba(0, 212, 255, 0.6),
                inset 0 1px 0 rgba(255, 255, 255, 0.3);
            animation: cellPulse 4s ease-in-out infinite;
        }
        
        /* Stagger the animation */
        .cell:nth-child(1) { animation-delay: 0s; }
        .cell:nth-child(3) { animation-delay: 0.3s; }
        .cell:nth-child(5) { animation-delay: 0.6s; }
        .cell:nth-child(7) { animation-delay: 0.9s; }
        .cell:nth-child(9) { animation-delay: 1.2s; }
        
        @keyframes cellPulse {
            0%, 100% { 
                opacity: 0.4; 
                transform: scale(1);
            }
            50% { 
                opacity: 1; 
                transform: scale(1.1);
            }
        }
        
        /* Inactive cells */
        .cell:nth-child(2), 
        .cell:nth-child(4), 
        .cell:nth-child(6), 
        .cell:nth-child(8) {
            background: rgba(255, 255, 255, 0.1);
            opacity: 0.6;
        }
        
        .logo-text { 
            color: #ffffff;
            letter-spacing: -0.02em;
            font-weight: 700;
            text-transform: uppercase;
            font-size: 20px;
        }
        
        .kaspa-user-info {
            color: rgba(255, 255, 255, 0.9);
            font-family: 'Inter', -apple-system, sans-serif;
            font-size: 14px;
            text-align: right;
        }
        
        .kaspa-user-status {
            color: #00d4ff;
            font-size: 11px;
            text-transform: uppercase;
            font-weight: 600;
            margin-top: 3px;
            letter-spacing: 0.05em;
        }
        
        .kaspa-user-status.premium {
            color: #ffd700;
            text-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
        }
        
        .kaspa-user-status.free {
            color: rgba(255, 255, 255, 0.5);
        }
        
        .kaspa-user-status.guest {
            color: rgba(255, 255, 255, 0.3);
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
        
        /* Ensure sidebar content remains visible */
        section[data-testid="stSidebar"] > div {
            display: block !important;
        }
        
        /* PREVENT BODY OVERFLOW DURING TRANSITIONS */
        body {
            overflow-x: hidden;
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
            color: rgba(255, 255, 255, 0.7) !important;
        }
        
        /* Icon color on hover */
        .stButton:hover .material-icons {
            color: #00d4ff !important;
        }
        
        /* Divider styling */
        [data-testid="stSidebar"] hr {
            border: none !important;
            height: 1px !important;
            background: rgba(255, 255, 255, 0.08) !important;
            margin: 16px 0 !important;
        }
        
        @media (max-width: 768px) {
            .kaspa-header {
                padding: 0 1rem;
            }
            
            .kaspa-logo {
                font-size: 18px;
                gap: 10px;
            }
            
            .matrix {
                width: 24px;
                height: 24px;
            }
            
            .cell {
                width: 6px;
                height: 6px;
            }
            
            .logo-text {
                font-size: 16px;
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

    # SIDEBAR NAVIGATION WITH MATERIAL ICONS
    # Add home button at top
    if st.sidebar.button("Home", key="nav_home", use_container_width=True, icon=":material/home:"):
        st.switch_page("Home.py")
    
    # Account buttons right under Home
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
        # User not logged in
        if st.sidebar.button("Login / Register", key="nav_login", use_container_width=True, icon=":material/login:"):
            st.switch_page("pages/0_🔑_Login.py")
    
    st.sidebar.markdown("---")
    
    # Mining Section
    with st.sidebar.expander("⛏ Mining", expanded=True):
        if st.button("Hashrate", key="sidebar_hashrate", use_container_width=True, icon=":material/trending_up:"):
            st.switch_page("pages/1_⛏️_Mining_Hashrate.py")
        if st.button("Difficulty", key="sidebar_difficulty", use_container_width=True, icon=":material/settings:"):
            st.switch_page("pages/2_⛏️_Mining_Difficulty.py")
    
    # Spot Market Section with account_balance icon (same as Market Cap)
    with st.sidebar.expander(":material/account_balance: Spot Market", expanded=True):
        if st.button("Price", key="sidebar_price", use_container_width=True, icon=":material/attach_money:"):
            st.switch_page("pages/3_💰_Spot_Price.py")
        if st.button("Volume", key="sidebar_volume", use_container_width=True, icon=":material/bar_chart:"):
            st.switch_page("pages/4_💰_Spot_Volume.py")
        if st.button("Market Cap", key="sidebar_marketcap", use_container_width=True, icon=":material/account_balance:"):
            st.switch_page("pages/5_💰_Spot_Market_Cap.py")
    
    # Social Data Section with Material Icons - UPDATED
    with st.sidebar.expander(":material/groups: Social Data", expanded=True):
        if st.button("Social Metrics", key="sidebar_social1", use_container_width=True, icon=":material/analytics:"):
            st.switch_page("pages/6_📱_Social_Metrics.py")
        if st.button("Social Trends", key="sidebar_social2", use_container_width=True, icon=":material/show_chart:"):
            st.switch_page("pages/7_📱_Social_Trends.py")
    
    # Premium Analytics Section - PRESERVED EXACTLY with all access control logic
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
