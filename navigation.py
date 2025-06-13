import streamlit as st
from footer import add_footer

def add_navigation():
    """Add organized navigation to sidebar AND header (shared across all pages)"""
    
    # CRITICAL FIX: Inject CSS IMMEDIATELY to prevent flickering
    # This runs before Streamlit renders its default header
    st.markdown("""
    <style>
        /* CACHE BUSTER - Change this comment to force CSS reload: v2.0 */
        /* Import Inter font like BetterStack */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        /* Import Google Material Symbols */
        @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');
        
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
        
        /* BETTERSTACK-STYLE HEADER */
        .kaspa-header {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            width: 100vw;
            height: 70px;
            z-index: 999997;
            /* BetterStack-style black with transparency */
            background: rgba(10, 10, 10, 0.8);
            backdrop-filter: blur(20px) saturate(180%);
            -webkit-backdrop-filter: blur(20px) saturate(180%);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 2rem;
            /* UPDATED: New house style border color */
            border-bottom: 1px solid #363650;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }
        
        /* PUSH MAIN CONTENT DOWN - Critical for preventing overlap */
        .main .block-container {
            padding-top: 90px !important;
        }
        
        /* UPDATED SIDEBAR WITH NEW HOUSE STYLE COLORS */
        [data-testid="stSidebar"] {
            margin-top: 70px;
            height: calc(100vh - 70px);
            /* UPDATED: Same background as header */
            background: rgba(10, 10, 10, 0.8) !important;
            backdrop-filter: blur(30px) saturate(120%) !important;
            -webkit-backdrop-filter: blur(30px) saturate(120%) !important;
            /* UPDATED: New house style border color */
            border-right: 1px solid #363650 !important;
            box-shadow: 
                2px 0 20px rgba(0, 0, 0, 0.2),
                inset -1px 0 0 rgba(255, 255, 255, 0.03) !important;
        }
        
        /* Style sidebar content container */
        [data-testid="stSidebar"] > div {
            background: transparent !important;
            padding-top: 20px !important;
        }
        
        /* Enhanced sidebar buttons - CLEAN BETTERSTACK STYLE with Inter font */
        [data-testid="stSidebar"] .stButton > button {
            background: transparent !important;
            border: none !important;
            border-radius: 0 !important;
            color: #9CA3AF !important;
            backdrop-filter: none !important;
            transition: all 0.2s ease !important;
            box-shadow: none !important;
            font-weight: 400 !important;
            text-align: left !important;
            justify-content: flex-start !important;
            display: flex !important;
            align-items: center !important;
            font-size: 14px !important;
            position: relative !important;
            overflow: visible !important;
            padding: 8px 12px !important;
            margin: 0 !important;
            font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
        }
        
        /* Button hover state - subtle highlight like BetterStack */
        [data-testid="stSidebar"] .stButton > button:hover {
            background: rgba(255, 255, 255, 0.05) !important;
            border: none !important;
            box-shadow: none !important;
            color: #F3F4F6 !important;
            transform: none !important;
            border-radius: 6px !important;
        }
        
        /* Remove shimmer effect */
        [data-testid="stSidebar"] .stButton > button::before {
            display: none !important;
        }
        
        /* Target button text specifically inside sidebar */
        [data-testid="stSidebar"] .stButton > button span,
        [data-testid="stSidebar"] .stButton > button p,
        [data-testid="stSidebar"] .stButton > button div {
            font-size: 13px !important;
        }
        
        /* Target button text content more specifically */
        [data-testid="stSidebar"] button[kind="secondary"] {
            font-size: 13px !important;
        }
        
        [data-testid="stSidebar"] button[kind="secondary"] span {
            font-size: 13px !important;
        }
        
        /* EXPANDERS - BETTERSTACK CLEAN STYLE with Inter font */
        
        /* Target all expander elements - completely clean */
        [data-testid="stSidebar"] details,
        [data-testid="stSidebar"] details > div,
        [data-testid="stSidebar"] details > div > div,
        [data-testid="stSidebar"] summary,
        [data-testid="stSidebar"] .streamlit-expanderHeader,
        [data-testid="stSidebar"] .streamlit-expanderContent {
            border: none !important;
            outline: none !important;
            background: transparent !important;
            backdrop-filter: none !important;
            box-shadow: none !important;
            border-radius: 0 !important;
            font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
        }
        
        /* Style the summary (clickable header) - BetterStack style */
        [data-testid="stSidebar"] summary {
            color: #9CA3AF !important;
            font-weight: 400 !important;
            cursor: pointer !important;
            padding: 8px 12px !important;
            margin: 0 !important;
            list-style: none !important;
            font-size: 14px !important;
            font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
        }
        
        /* Remove default arrow */
        [data-testid="stSidebar"] summary::-webkit-details-marker {
            display: none !important;
        }
        
        [data-testid="stSidebar"] summary::marker {
            display: none !important;
        }
        
        /* Hover effect for summary - subtle like BetterStack */
        [data-testid="stSidebar"] summary:hover {
            color: #F3F4F6 !important;
            background: rgba(255, 255, 255, 0.05) !important;
            border-radius: 6px !important;
            box-shadow: none !important;
        }
        
        /* Ensure all nested elements are borderless and clean */
        [data-testid="stSidebar"] details *,
        [data-testid="stSidebar"] .streamlit-expanderHeader *,
        [data-testid="stSidebar"] .streamlit-expanderContent * {
            border: none !important;
            box-shadow: none !important;
            background: transparent !important;
        }
        
        /* Style sidebar text - BetterStack soft gray with Inter font */
        [data-testid="stSidebar"] .stMarkdown {
            color: #9CA3AF !important;
            font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
        }
        
        /* Style sidebar general text */
        [data-testid="stSidebar"] p {
            color: #9CA3AF !important;
            font-weight: 400 !important;
            font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
        }
        
        /* Apply Inter font to all sidebar text elements */
        [data-testid="stSidebar"] * {
            font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
        }
        
        /* Enhanced warning/info/success boxes in sidebar with house colors */
        [data-testid="stSidebar"] .stAlert {
            background: linear-gradient(135deg, 
                rgba(54, 54, 80, 0.7) 0%, 
                rgba(31, 31, 58, 0.85) 100%) !important;
            /* UPDATED: New house style border color */
            border: 1px solid #363650 !important;
            border-radius: 8px !important;
            backdrop-filter: blur(10px) !important;
            color: #e2e8f0 !important;
            box-shadow: 
                0 2px 8px rgba(0, 0, 0, 0.1),
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

        /* Expand button when sidebar is COLLAPSED - Clean hamburger only */
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

        /* Add custom hamburger icon - grey by default */
        div[data-testid="stSidebarCollapsedControl"] button::before,
        button[data-testid="collapsedControl"]::before {
            content: "☰" !important;
            font-size: 18px !important;
            color: #9ca3af !important;
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
        
        /* ENHANCED HEADER STYLING WITH DATA MATRIX LOGO */
        .kaspa-logo {
            display: flex;
            align-items: center;
            gap: 12px;
            font-family: Inter, -apple-system, sans-serif;
            font-size: 22px;
            font-weight: 600;
            color: #ffffff;
        }
        
        /* Enhanced matrix with subtle animation */
        .matrix {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 2px;
            width: 29px;
            height: 29px;
            position: relative;
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
            transition: all 0.3s ease;
        }
        
        /* Enhanced active cells with subtle pulse */
        .cell:nth-child(1), 
        .cell:nth-child(3), 
        .cell:nth-child(5), 
        .cell:nth-child(7), 
        .cell:nth-child(9) {
            background: linear-gradient(45deg, #00d4ff, #0ea5e9);
            box-shadow: 
                0 0 12px rgba(0, 212, 255, 0.8), 
                inset 0 1px 1px rgba(255, 255, 255, 0.3);
            animation: cellPulse 3s ease infinite;
        }
        
        /* Stagger the animation */
        .cell:nth-child(1) { animation-delay: 0s; }
        .cell:nth-child(3) { animation-delay: 0.2s; }
        .cell:nth-child(5) { animation-delay: 0.4s; }
        .cell:nth-child(7) { animation-delay: 0.6s; }
        .cell:nth-child(9) { animation-delay: 0.8s; }
        
        @keyframes cellPulse {
            0%, 100% { opacity: 0.5; transform: scale(1); }
            50% { opacity: 1; transform: scale(1.1); }
        }
        
        .cell:nth-child(2) { opacity: 0.9; }
        .cell:nth-child(4) { opacity: 0.8; }
        .cell:nth-child(6) { opacity: 0.8; }
        .cell:nth-child(8) { opacity: 0.9; }
        
        .logo-text { 
            color: #ffffff; 
            letter-spacing: -0.5px;
            font-weight: 600;
        }
        
        /* BetterStack-style user info styling */
        .kaspa-user-info {
            font-family: Inter, -apple-system, sans-serif;
            color: #a3a3a3;
            font-size: 14px;
            text-align: right;
            font-weight: 400;
        }
        
        .kaspa-user-info > div:first-child {
            color: #e2e8f0;
            margin-bottom: 2px;
        }
        
        .kaspa-user-status {
            color: #a3a3a3;
            font-size: 12px;
            font-weight: 500;
            margin-top: 2px;
            letter-spacing: 0.5px;
            display: flex;
            align-items: center;
            justify-content: flex-end;
            gap: 6px;
        }
        
        .kaspa-user-status.premium {
            color: #fbbf24;
            text-shadow: 0 0 10px rgba(251, 191, 36, 0.3);
        }
        
        .kaspa-user-status.free {
            color: #94a3b8;
        }
        
        .kaspa-user-status.guest {
            color: #A0A0B8;
        }
        
        /* Custom guest icon styling */
        .guest-icon {
            font-family: 'Material Symbols Outlined';
            font-weight: normal;
            font-style: normal;
            font-size: 16px;
            line-height: 1;
            letter-spacing: normal;
            text-transform: none;
            display: inline-block;
            white-space: nowrap;
            word-wrap: normal;
            direction: ltr;
            color: #5B6CFF;
            font-variation-settings:
                'FILL' 0,
                'wght' 400,
                'GRAD' 0,
                'opsz' 20;
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
        
        /* FORCE SIDEBAR ICONS TO PURPLE - PRESERVE STREAMLIT ICON FUNCTIONALITY */
        
        /* Target Streamlit's icon elements specifically without breaking functionality */
        [data-testid="stSidebar"] button[data-testid] span[data-testid*="stIcon"],
        [data-testid="stSidebar"] button span[data-testid*="stIcon"] {
            color: #5B6CFF !important;
        }
        
        /* Target Material Icons specifically */
        [data-testid="stSidebar"] span[data-testid*="stIcon"] svg,
        [data-testid="stSidebar"] span[data-testid*="stIcon"] svg path {
            fill: #5B6CFF !important;
            color: #5B6CFF !important;
        }
        
        /* More specific targeting for Streamlit's button icons */
        [data-testid="stSidebar"] .stButton button span[data-testid*="stIcon"],
        [data-testid="stSidebar"] .stButton button span[data-testid*="stIcon"] * {
            color: #5B6CFF !important;
            fill: #5B6CFF !important;
        }
        
        /* Target any remaining icon elements */
        [data-testid="stSidebar"] [data-testid*="stIcon"],
        [data-testid="stSidebar"] [data-testid*="stIcon"] * {
            color: #5B6CFF !important;
            fill: #5B6CFF !important;
        }
        
        /* Icon hover states */
        [data-testid="stSidebar"] .stButton:hover span[data-testid*="stIcon"],
        [data-testid="stSidebar"] .stButton:hover span[data-testid*="stIcon"] *,
        [data-testid="stSidebar"] button:hover span[data-testid*="stIcon"],
        [data-testid="stSidebar"] button:hover span[data-testid*="stIcon"] * {
            color: #6D7DFF !important;
            fill: #6D7DFF !important;
        }
        
        /* Force override any inline styles */
        [data-testid="stSidebar"] * {
            --icon-color: #5B6CFF !important;
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
                <div class="kaspa-user-status guest">
                    <span class="guest-icon">person</span>
                    GUEST
                </div>
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
