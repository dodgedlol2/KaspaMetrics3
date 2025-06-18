import streamlit as st
import streamlit.components.v1 as components
from footer import add_footer

def sidebar_toggle_button():
    """Create a unified sidebar toggle button using Streamlit components"""
    
    # HTML and JavaScript for the sidebar toggle button
    component_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { margin: 0; padding: 0; background: transparent; }
        </style>
    </head>
    <body>
        <script>
            console.log('Sidebar toggle component loaded!');
            
            function createSidebarToggle() {
                console.log('Creating sidebar toggle button...');
                
                // Remove any existing toggle button
                const existing = window.parent.document.getElementById('unified-sidebar-toggle');
                if (existing) {
                    existing.remove();
                }
                
                // Create the toggle button
                const toggleButton = window.parent.document.createElement('button');
                toggleButton.id = 'unified-sidebar-toggle';
                toggleButton.innerHTML = '☰';
                
                // Style the button
                toggleButton.style.cssText = `
                    position: fixed !important;
                    top: 11px !important;
                    left: 20px !important;
                    width: 40px !important;
                    height: 40px !important;
                    background: rgba(54, 54, 80, 0.8) !important;
                    border: 1px solid #363650 !important;
                    border-radius: 8px !important;
                    backdrop-filter: blur(10px) !important;
                    z-index: 999999 !important;
                    font-size: 18px !important;
                    color: #f1f5f9 !important;
                    cursor: pointer !important;
                    display: flex !important;
                    align-items: center !important;
                    justify-content: center !important;
                    font-family: Arial, sans-serif !important;
                    transition: all 0.3s ease !important;
                `;
                
                // Add hover effects
                toggleButton.addEventListener('mouseenter', function() {
                    this.style.background = 'rgba(91, 108, 255, 0.15)';
                    this.style.borderColor = 'rgba(91, 108, 255, 0.4)';
                    this.style.color = '#8b9aff';
                    this.style.transform = 'scale(1.05)';
                });
                
                toggleButton.addEventListener('mouseleave', function() {
                    this.style.background = 'rgba(54, 54, 80, 0.8)';
                    this.style.borderColor = '#363650';
                    this.style.color = '#f1f5f9';
                    this.style.transform = 'scale(1)';
                });
                
                // Add click functionality
                toggleButton.addEventListener('click', function() {
                    console.log('Sidebar toggle clicked!');
                    
                    const parentDoc = window.parent.document;
                    const sidebar = parentDoc.querySelector('[data-testid="stSidebar"]');
                    const isCollapsed = sidebar && sidebar.getAttribute('aria-expanded') === 'false';
                    
                    if (isCollapsed) {
                        this.innerHTML = '✕';
                        const expandBtn = parentDoc.querySelector('[data-testid="stExpandSidebarButton"]');
                        if (expandBtn) expandBtn.click();
                    } else {
                        this.innerHTML = '☰';
                        const collapseBtn = parentDoc.querySelector('[data-testid="stSidebarCollapseButton"] button');
                        if (collapseBtn) collapseBtn.click();
                    }
                });
                
                // Monitor sidebar changes
                const updateIcon = () => {
                    const sidebar = window.parent.document.querySelector('[data-testid="stSidebar"]');
                    const isCollapsed = sidebar && sidebar.getAttribute('aria-expanded') === 'false';
                    toggleButton.innerHTML = isCollapsed ? '☰' : '✕';
                };
                
                const sidebar = window.parent.document.querySelector('[data-testid="stSidebar"]');
                if (sidebar) {
                    const observer = new MutationObserver(updateIcon);
                    observer.observe(sidebar, { attributes: true, attributeFilter: ['aria-expanded'] });
                }
                
                // Add to parent document
                window.parent.document.body.appendChild(toggleButton);
                console.log('Sidebar toggle button created successfully!');
                updateIcon();
            }
            
            // Create button with multiple attempts
            setTimeout(createSidebarToggle, 100);
            setTimeout(createSidebarToggle, 500);
            setTimeout(createSidebarToggle, 1000);
            
        </script>
    </body>
    </html>
    """
    
    # Create the component (invisible iframe)
    components.html(component_html, height=0, width=0)

def add_navigation():
    """Add organized navigation to sidebar AND header (shared across all pages)"""
    
    # CRITICAL FIX: Inject CSS IMMEDIATELY to prevent flickering
    # This runs before Streamlit renders its default header
    st.markdown("""
    <style>
        /* CACHE BUSTER - Change this comment to force CSS reload: v2.2 */
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
        
        /* BETTERSTACK-STYLE HEADER - RESTORED */
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
        
        /* PUSH MAIN CONTENT DOWN - Back to normal */
        .main .block-container {
            padding-top: 90px !important;
        }
        
        /* SIDEBAR CONTROLS - TARGET BOTH BUTTONS CORRECTLY */
        
        /* Collapse button (<<) - When sidebar is open */
        div[data-testid="stSidebarCollapseButton"] {
            position: fixed !important;
            top: 185px !important;
            left: 180px !important; /* Position when sidebar is open */
            z-index: 999999 !important;
            display: block !important;
            visibility: visible !important;
            opacity: 1 !important;
            background: rgba(54, 54, 80, 0.8) !important;
            border: 1px solid #363650 !important;
            border-radius: 8px !important;
            backdrop-filter: blur(10px) !important;
            width: 40px !important;
            height: 40px !important;
        }

        /* Expand button (>>) - MAXIMUM SPECIFICITY APPROACH */
        html body .stApp button[data-testid="stExpandSidebarButton"],
        button[data-testid="stExpandSidebarButton"].st-emotion-cache-1drv5uj,
        button[data-testid="stExpandSidebarButton"][class*="st-emotion-cache"],
        .st-emotion-cache-1drv5uj[data-testid="stExpandSidebarButton"] {
            position: fixed !important;
            top: 185px !important;
            left: 20px !important;
            z-index: 999999 !important;
            display: block !important;
            visibility: visible !important;
            opacity: 1 !important;
            background: red !important;
            border: 3px solid yellow !important;
            border-radius: 8px !important;
            width: 40px !important;
            height: 40px !important;
            transform: none !important;
            margin: 0 !important;
            right: auto !important;
            bottom: auto !important;
        }

        /* Style both buttons */
        div[data-testid="stSidebarCollapseButton"] button,
        button[data-testid="stExpandSidebarButton"] {
            background: transparent !important;
            border: none !important;
            color: #f1f5f9 !important;
            width: 100% !important;
            height: 100% !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            cursor: pointer !important;
            pointer-events: auto !important;
        }

        /* Force icon visibility */
        div[data-testid="stSidebarCollapseButton"] [data-testid="stIconMaterial"],
        button[data-testid="stExpandSidebarButton"] [data-testid="stIconMaterial"] {
            color: #f1f5f9 !important;
            opacity: 1 !important;
            display: block !important;
            visibility: visible !important;
            font-size: 18px !important;
        }

        /* Hover effects */
        div[data-testid="stSidebarCollapseButton"]:hover,
        button[data-testid="stExpandSidebarButton"]:hover {
            background: rgba(91, 108, 255, 0.15) !important;
            border-color: rgba(91, 108, 255, 0.4) !important;
            box-shadow: 0 4px 16px rgba(91, 108, 255, 0.15) !important;
        }

        /* Hover icon effects */
        div[data-testid="stSidebarCollapseButton"]:hover [data-testid="stIconMaterial"],
        button[data-testid="stExpandSidebarButton"]:hover [data-testid="stIconMaterial"] {
            color: #8b9aff !important;
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
        
        /* Enhanced sidebar buttons with subtle gradient using house colors - REVERTED TEXT SIZE */
        [data-testid="stSidebar"] .stButton > button {
            background: linear-gradient(135deg, 
                rgba(54, 54, 80, 0.6) 0%, 
                rgba(31, 31, 58, 0.8) 100%) !important;
            /* UPDATED: New house style border color */
            border: 1px solid #363650 !important;
            border-radius: 12px !important;
            color: #f1f5f9 !important;
            backdrop-filter: blur(10px) !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 
                0 2px 8px rgba(0, 0, 0, 0.1),
                inset 0 1px 0 rgba(255, 255, 255, 0.03) !important;
            font-weight: 600 !important;
            text-align: left !important;
            justify-content: flex-start !important;
            display: flex !important;
            align-items: center !important;
            font-size: 13px !important;
            position: relative !important;
            overflow: hidden !important;
        }
        
        /* Button hover state with enhanced effect - UPDATED TO PURPLE THEME */
        [data-testid="stSidebar"] .stButton > button:hover {
            background: linear-gradient(135deg, 
                rgba(91, 108, 255, 0.15) 0%, 
                rgba(54, 54, 80, 0.9) 100%) !important;
            border-color: rgba(91, 108, 255, 0.4) !important;
            box-shadow: 
                0 4px 16px rgba(91, 108, 255, 0.15), 
                0 0 0 1px rgba(91, 108, 255, 0.2),
                inset 0 1px 0 rgba(255, 255, 255, 0.05) !important;
            transform: translateY(-1px) !important;
        }
        
        /* Subtle shimmer effect on hover */
        [data-testid="stSidebar"] .stButton > button::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, 
                transparent 0%, 
                rgba(255, 255, 255, 0.05) 50%, 
                transparent 100%);
            transition: left 0.5s ease;
        }
        
        [data-testid="stSidebar"] .stButton > button:hover::before {
            left: 100%;
        }
        
        /* Target button text specifically inside sidebar - REVERTED TO 13px */
        [data-testid="stSidebar"] .stButton > button span,
        [data-testid="stSidebar"] .stButton > button p,
        [data-testid="stSidebar"] .stButton > button div {
            font-size: 13px !important;
        }
        
        /* Target button text content more specifically - REVERTED TO 13px */
        [data-testid="stSidebar"] button[kind="secondary"] {
            font-size: 13px !important;
        }
        
        [data-testid="stSidebar"] button[kind="secondary"] span {
            font-size: 13px !important;
        }
        
        /* EXPANDERS - COMPLETELY INVISIBLE BACKGROUNDS AND BORDERS - ENHANCED */
        
        /* Target ALL expander-related elements and make them completely transparent */
        [data-testid="stSidebar"] details,
        [data-testid="stSidebar"] details > div,
        [data-testid="stSidebar"] details > div > div,
        [data-testid="stSidebar"] details > div > div > div,
        [data-testid="stSidebar"] summary,
        [data-testid="stSidebar"] .streamlit-expanderHeader,
        [data-testid="stSidebar"] .streamlit-expanderContent,
        [data-testid="stSidebar"] .stExpander,
        [data-testid="stSidebar"] [data-testid*="stExpander"],
        [data-testid="stSidebar"] [data-testid="stExpanderToggleIcon"],
        [data-testid="stSidebar"] [data-testid="stExpanderDetails"] {
            border: none !important;
            outline: none !important;
            background: transparent !important;
            background-color: transparent !important;
            backdrop-filter: none !important;
            box-shadow: none !important;
            border-radius: 0 !important;
            padding: 0 !important;
            margin: 0 !important;
        }
        
        /* Target the expander header/summary specifically - remove all backgrounds */
        [data-testid="stSidebar"] summary,
        [data-testid="stSidebar"] details > summary,
        [data-testid="stSidebar"] .streamlit-expanderHeader {
            color: #e2e8f0 !important;
            font-weight: 600 !important;
            cursor: pointer !important;
            padding: 8px 12px !important;
            margin: 0 !important;
            background: transparent !important;
            background-color: transparent !important;
            border: none !important;
            box-shadow: none !important;
            transition: color 0.2s ease !important;
        }
        
        /* Remove any hover backgrounds on summary - updated to purple theme */
        [data-testid="stSidebar"] summary:hover,
        [data-testid="stSidebar"] details > summary:hover {
            color: #8b9aff !important;
            background: transparent !important;
            background-color: transparent !important;
            border: none !important;
            box-shadow: none !important;
        }
        
        /* Hide default dropdown arrows and replace with custom ones */
        [data-testid="stSidebar"] summary::marker,
        [data-testid="stSidebar"] summary::-webkit-details-marker,
        [data-testid="stSidebar"] details > summary::marker,
        [data-testid="stSidebar"] details > summary::-webkit-details-marker {
            display: none !important;
            content: "" !important;
        }
        
        /* Hide Streamlit-generated dropdown icons */
        [data-testid="stSidebar"] [data-testid="stExpanderToggleIcon"],
        [data-testid="stSidebar"] .streamlit-expanderHeader svg,
        [data-testid="stSidebar"] summary svg,
        [data-testid="stSidebar"] details svg {
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
        }
        
        /* Add custom dropdown arrow with clean styling */
        [data-testid="stSidebar"] summary {
            position: relative !important;
            display: flex !important;
            align-items: center !important;
            justify-content: space-between !important;
        }
        
        /* Custom arrow - right-pointing by default */
        [data-testid="stSidebar"] summary::after {
            content: "▶" !important;
            font-size: 10px !important;
            color: #64748b !important;
            transition: all 0.2s ease !important;
            transform-origin: center !important;
            margin-left: auto !important;
            opacity: 0.7 !important;
        }
        
        /* Arrow points down when expanded */
        [data-testid="stSidebar"] details[open] > summary::after {
            transform: rotate(90deg) !important;
            color: #5B6CFF !important;
            opacity: 1 !important;
        }
        
        /* Arrow hover effect - updated to purple theme */
        [data-testid="stSidebar"] summary:hover::after {
            color: #8b9aff !important;
            opacity: 1 !important;
        }
        
        /* Ensure all nested expander elements are completely borderless */
        [data-testid="stSidebar"] details *,
        [data-testid="stSidebar"] .streamlit-expanderHeader *,
        [data-testid="stSidebar"] .streamlit-expanderContent *,
        [data-testid="stSidebar"] .stExpander *,
        [data-testid="stSidebar"] [data-testid*="stExpander"] * {
            border: none !important;
            box-shadow: none !important;
            background: transparent !important;
            background-color: transparent !important;
        }
        
        /* Override any possible container backgrounds */
        [data-testid="stSidebar"] .element-container,
        [data-testid="stSidebar"] .stExpander > .element-container,
        [data-testid="stSidebar"] [data-testid*="stExpander"] > .element-container {
            background: transparent !important;
            background-color: transparent !important;
        }
        
        /* Force override any Streamlit expander container styling */
        [data-testid="stSidebar"] div[data-testid*="column"] > div,
        [data-testid="stSidebar"] .stExpander-content,
        [data-testid="stSidebar"] .streamlit-expander {
            background: transparent !important;
            background-color: transparent !important;
            border: none !important;
            padding: 0 !important;
        }
        
        /* Style sidebar text content inside expanders */
        [data-testid="stSidebar"] .stMarkdown {
            color: #cbd5e1 !important;
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
        
        /* FORCE ALL SIDEBAR ICONS TO BE #5B6CFF - COMPREHENSIVE TARGETING */
        
        /* Target all possible icon containers in sidebar */
        [data-testid="stSidebar"] .material-icons,
        [data-testid="stSidebar"] button .material-icons,
        [data-testid="stSidebar"] .stButton .material-icons,
        [data-testid="stSidebar"] button[kind="secondary"] .material-icons,
        [data-testid="stSidebar"] span[data-testid*="material"],
        [data-testid="stSidebar"] div[data-testid*="material"],
        [data-testid="stSidebar"] .material-symbols-outlined,
        [data-testid="stSidebar"] span.material-symbols-outlined,
        [data-testid="stSidebar"] i[class*="material"],
        [data-testid="stSidebar"] span[class*="material"],
        [data-testid="stSidebar"] .stButton span[data-testid],
        [data-testid="stSidebar"] button span[data-testid],
        [data-testid="stSidebar"] span[data-testid*="Icon"],
        [data-testid="stSidebar"] span[data-testid*="icon"] {
            color: #5B6CFF !important;
            fill: #5B6CFF !important;
        }
        
        /* Target Streamlit's internal icon structure */
        [data-testid="stSidebar"] button > div > span,
        [data-testid="stSidebar"] .stButton > button > div > span {
            color: #5B6CFF !important;
        }
        
        /* Target any SVG icons */
        [data-testid="stSidebar"] svg,
        [data-testid="stSidebar"] svg *,
        [data-testid="stSidebar"] button svg,
        [data-testid="stSidebar"] button svg * {
            fill: #5B6CFF !important;
            color: #5B6CFF !important;
        }
        
        /* Icon color on hover - purple theme with smaller hover scale */
        [data-testid="stSidebar"] .stButton:hover .material-icons,
        [data-testid="stSidebar"] .stButton:hover span[data-testid],
        [data-testid="stSidebar"] .stButton:hover svg,
        [data-testid="stSidebar"] .stButton:hover svg *,
        [data-testid="stSidebar"] button:hover .material-icons,
        [data-testid="stSidebar"] button:hover span[data-testid],
        [data-testid="stSidebar"] button:hover svg,
        [data-testid="stSidebar"] button:hover svg * {
            color: #8b9aff !important;
            fill: #8b9aff !important;
            transform: scale(1.1) !important;
            transition: all 0.2s ease !important;
        }
        
        /* Force override any inline styles */
        [data-testid="stSidebar"] * {
            --icon-color: #5B6CFF !important;
        }
        
        /* OVERRIDE SPECIFICALLY FOR LOGIN REQUIRED BUTTON - FORCE #6366F1 STYLING */
        [data-testid="stSidebar"] .stButton > button[aria-label*="Login Required"],
        [data-testid="stSidebar"] button[data-testid*="sidebar_login_premium_custom"],
        [data-testid="stSidebar"] .stButton:has(button[data-testid*="sidebar_login_premium_custom"]) > button {
            background: #6366F1 !important;
            border: 2px solid #6366F1 !important;
            color: #ffffff !important;
            font-weight: 700 !important;
            border-radius: 8px !important;
            box-shadow: 
                0 4px 16px rgba(99, 102, 241, 0.8),
                0 0 24px rgba(99, 102, 241, 0.6) !important;
            text-align: center !important;
            justify-content: center !important;
        }
        
        /* OVERRIDE HOVER FOR LOGIN REQUIRED BUTTON ONLY */
        [data-testid="stSidebar"] .stButton > button[aria-label*="Login Required"]:hover,
        [data-testid="stSidebar"] button[data-testid*="sidebar_login_premium_custom"]:hover,
        [data-testid="stSidebar"] .stButton:has(button[data-testid*="sidebar_login_premium_custom"]) > button:hover {
            background: #7c3aed !important;
            border-color: #8b5cf6 !important;
            box-shadow: 
                0 8px 32px rgba(99, 102, 241, 1.0), 
                0 0 40px rgba(139, 92, 246, 0.8) !important;
            transform: translateY(-2px) !important;
            color: #ffffff !important;
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
    
    <script>
        // Simplified JavaScript for logo functionality only
        document.addEventListener('DOMContentLoaded', function() {
            console.log('Logo JavaScript loaded');
            
            function handleLogoClick(event) {
                event.preventDefault();
                event.stopPropagation();
                window.location.href = 'https://kaspametrics3test1.streamlit.app';
            }
            
            function addLogoClickHandler() {
                const logo = document.querySelector('.kaspa-logo');
                if (logo) {
                    logo.addEventListener('click', handleLogoClick, true);
                    logo.style.pointerEvents = 'auto';
                    return true;
                }
                return false;
            }
            
            // Try to add logo handler
            if (!addLogoClickHandler()) {
                let attempts = 0;
                const retryInterval = setInterval(() => {
                    attempts++;
                    if (addLogoClickHandler() || attempts > 50) {
                        clearInterval(retryInterval);
                    }
                }, 100);
            }
        });
    </script>
    
    <!-- SIDEBAR TOGGLE COMPONENT -->
    """, unsafe_allow_html=True)
    
    # Add the sidebar toggle component
    sidebar_toggle_button()
    
    # Continue with header generation
    if 'logo_clicked' in st.session_state or st.query_params.get('logo_clicked') == 'true':
        st.session_state.pop('logo_clicked', None)
        st.switch_page("Home.py")
    
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
            <a href="https://kaspametrics3test1.streamlit.app" class="kaspa-logo-link" style="text-decoration: none; color: inherit;">
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
            </a>
            <div class="kaspa-user-info">
                <div>Welcome, {user_name}</div>
                <div class="kaspa-user-status {status_class}">{status_text}</div>
            </div>
        </div>
        """
    else:
        header_html = """
        <div class="kaspa-header">
            <a href="https://kaspametrics3test1.streamlit.app" class="kaspa-logo-link" style="text-decoration: none; color: inherit;">
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
            </a>
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
        with st.sidebar.expander(":material/crown: Premium Analytics", expanded=True):
            if st.button("Premium Features", key="sidebar_premium_features", use_container_width=True, icon=":material/star:"):
                st.switch_page("pages/B_👑_Premium_Features.py")
            if st.button("Premium Analytics", key="sidebar_premium1", use_container_width=True, icon=":material/science:"):
                st.switch_page("pages/8_👑_Premium_Analytics.py")
            if st.button("Advanced Metrics", key="sidebar_premium2", use_container_width=True, icon=":material/insights:"):
                st.switch_page("pages/9_👑_Advanced_Metrics.py")
    elif st.session_state.get('authentication_status'):
        with st.sidebar.expander(":material/crown: Premium Analytics", expanded=False):
            # Premium Features accessible to logged-in users (but not paying)
            if st.button("Premium Features", key="sidebar_premium_features_free", use_container_width=True, icon=":material/star:"):
                st.switch_page("pages/B_👑_Premium_Features.py")
            st.warning("Upgrade Required")
            st.write("**Monthly:** $9.99")
            st.write("**Annual:** $99")
            if st.button("Upgrade Now", key="sidebar_upgrade", use_container_width=True, icon=":material/credit_card:"):
                st.switch_page("pages/B_👑_Premium_Features.py")
    else:
        with st.sidebar.expander(":material/crown: Premium Analytics", expanded=False):
            # Premium Features accessible to everyone (including non-logged users)
            if st.button("Premium Features", key="sidebar_premium_features_guest", use_container_width=True, icon=":material/star:"):
                st.switch_page("pages/B_👑_Premium_Features.py")
            # Custom login button with new color and material icon only
            if st.button("Login Required", key="sidebar_login_premium_custom", use_container_width=True, icon=":material/login:"):
                st.switch_page("pages/0_🔑_Login.py")
