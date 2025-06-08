import streamlit as st

# Page config MUST be first!
st.set_page_config(page_title="Premium Features", page_icon="👑", layout="wide")

import sys
import os

# Add parent directory to path for imports
parent_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(parent_dir)

from database import Database
from auth_handler import AuthHandler
from payment_handler import PaymentHandler
from navigation import add_navigation

# Add shared navigation to sidebar
add_navigation()

# Initialize handlers
@st.cache_resource
def init_handlers():
    db = Database()
    auth_handler = AuthHandler(db)
    payment_handler = PaymentHandler()
    return db, auth_handler, payment_handler

db, auth_handler, payment_handler = init_handlers()

# Header
st.title("👑 Premium Features")
st.write("Unlock advanced analytics and insights for serious crypto analysis")

# Check if user has premium
if st.session_state.get('is_premium'):
    st.success("🎉 **You have premium access!** Explore all features below.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔬 Premium Analytics", use_container_width=True):
            st.switch_page("pages/8_👑_Premium_Analytics.py")
    with col2:
        if st.button("📊 Advanced Metrics", use_container_width=True):
            st.switch_page("pages/9_👑_Advanced_Metrics.py")
    
    st.markdown("---")

# Feature comparison
st.subheader("📊 Feature Comparison")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🔓 **Free Features**")
    st.markdown("""
    ✅ **Mining Analytics**
    - Network hashrate tracking
    - Difficulty adjustments
    - Basic mining insights
    
    ✅ **Market Data**
    - Price charts and trends
    - Trading volume analysis
    - Market capitalization tracking
    
    ✅ **Social Metrics**
    - Community sentiment
    - Social media trends
    - Basic engagement metrics
    
    ✅ **Basic Charts**
    - Standard Plotly visualizations
    - Historical data views
    - Simple metrics cards
    """)

with col2:
    st.markdown("### 👑 **Premium Features**")
    st.markdown("""
    🚀 **Advanced Analytics**
    - AI-powered market predictions
    - Custom correlation analysis
    - Advanced technical indicators
    - Multi-timeframe analysis
    
    🔬 **Exclusive Data**
    - Whale activity tracking
    - On-chain flow analysis
    - MVRV and NVT ratios
    - Network health scoring
    
    📊 **Professional Tools**
    - Custom alerts & notifications
    - Data export (CSV, PDF)
    - API access for developers
    - Priority data updates
    
    💎 **Premium Support**
    - Priority customer support
    - Feature request priority
    - Beta feature access
    - Direct analyst contact
    """)

# Detailed feature showcase
st.markdown("---")
st.subheader("🔬 Premium Feature Deep Dive")

# Feature tabs
tab1, tab2, tab3, tab4 = st.tabs(["🤖 AI Analytics", "🐋 Whale Tracking", "📈 Advanced Charts", "🔔 Alerts"])

with tab1:
    st.markdown("### 🤖 AI-Powered Analytics")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **Market Prediction Engine**
        - Machine learning price predictions
        - Sentiment-based market analysis
        - Risk assessment algorithms
        - Volatility forecasting
        
        **Smart Insights**
        - Automated pattern recognition
        - Anomaly detection
        - Market cycle identification
        - Trend strength analysis
        """)
    with col2:
        # Mock AI insight
        st.info("""
        🤖 **AI Market Insight**
        
        "Based on current on-chain metrics and social sentiment, 
        KAS shows strong accumulation patterns similar to previous 
        bull run phases. Confidence: 78%"
        
        *This is a sample of premium AI insights*
        """)

with tab2:
    st.markdown("### 🐋 Whale Activity Tracking")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **Large Holder Monitoring**
        - Real-time whale transactions
        - Accumulation/distribution patterns
        - Exchange flow analysis
        - Dormancy tracking
        
        **Smart Alerts**
        - Large transaction notifications
        - Whale behavior changes
        - Exchange deposit/withdrawal alerts
        - Concentration risk monitoring
        """)
    with col2:
        # Mock whale data
        st.warning("""
        🐋 **Recent Whale Activity**
        
        - Whale #1: +2.5M KAS (Accumulating)
        - Whale #2: -1.8M KAS (Distributing)  
        - Exchange Inflow: +5.2M KAS
        - Risk Level: Medium
        
        *Live whale tracking for premium users*
        """)

with tab3:
    st.markdown("### 📈 Advanced Charting")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **Professional Indicators**
        - MACD, RSI, Bollinger Bands
        - Custom technical overlays
        - Multi-timeframe analysis
        - Volume profile analysis
        
        **Interactive Features**
        - Drawing tools and annotations
        - Custom indicator creation
        - Portfolio overlay analysis
        - Comparative analysis tools
        """)
    with col2:
        st.success("""
        📊 **Chart Features**
        
        • TradingView-style interface
        • 50+ technical indicators
        • Custom timeframes
        • Multiple chart types
        • Export capabilities
        
        *Professional trading tools*
        """)

with tab4:
    st.markdown("### 🔔 Custom Alerts")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **Smart Notifications**
        - Price alerts (above/below/% change)
        - Volume spike notifications
        - Technical indicator alerts
        - On-chain metric triggers
        
        **Delivery Methods**
        - Email notifications
        - SMS alerts (coming soon)
        - Discord webhooks
        - Mobile push notifications
        """)
    with col2:
        st.info("""
        🔔 **Alert Examples**
        
        ✅ KAS price > $0.15
        ✅ Volume > 50M (24h)
        ✅ Whale movement > 1M KAS
        ✅ Hashrate change > 10%
        
        *Set unlimited custom alerts*
        """)

# Pricing section
if not st.session_state.get('is_premium'):
    st.markdown("---")
    st.subheader("💳 Premium Pricing")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Pricing cards
        pricing_col1, pricing_col2 = st.columns(2)
        
        with pricing_col1:
            st.markdown("""
            <div style="border: 2px solid #28a745; border-radius: 10px; padding: 20px; text-align: center; background-color: #f8f9fa;">
                <h3>💎 Monthly Plan</h3>
                <h2 style="color: #28a745;">$9.99/month</h2>
                <p>• All premium features</p>
                <p>• Cancel anytime</p>
                <p>• Instant access</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("💳 Subscribe Monthly", key="pricing_monthly", use_container_width=True):
                if st.session_state.get('authentication_status'):
                    st.session_state['selected_plan'] = {'amount': 999, 'interval': 'month'}
                    payment_url = payment_handler.create_checkout_session(st.session_state['username'])
                    if payment_url:
                        st.markdown(f"[💳 Complete Payment]({payment_url})")
                else:
                    st.warning("Please login first")
                    if st.button("🔑 Login", key="login_monthly"):
                        st.switch_page("pages/0_🔑_Login.py")
        
        with pricing_col2:
            st.markdown("""
            <div style="border: 3px solid #ffc107; border-radius: 10px; padding: 20px; text-align: center; background-color: #fff3cd;">
                <h3>🏆 Annual Plan</h3>
                <h2 style="color: #ffc107;">$99/year</h2>
                <p><strong>Save 17%!</strong></p>
                <p>• All premium features</p>
                <p>• 2 months free</p>
                <p>• Best value</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("💳 Subscribe Annually", key="pricing_annual", use_container_width=True):
                if st.session_state.get('authentication_status'):
                    st.session_state['selected_plan'] = {'amount': 9900, 'interval': 'year'}
                    payment_url = payment_handler.create_checkout_session(st.session_state['username'])
                    if payment_url:
                        st.markdown(f"[💳 Complete Payment]({payment_url})")
                else:
                    st.warning("Please login first")
                    if st.button("🔑 Login", key="login_annual"):
                        st.switch_page("pages/0_🔑_Login.py")

# Testimonials section
st.markdown("---")
st.subheader("💬 What Users Say")

col1, col2, col3 = st.columns(3)
with col1:
    st.info("""
    ⭐⭐⭐⭐⭐
    
    *"The AI insights have completely changed how I analyze KAS. The whale tracking caught a major move before anyone else noticed!"*
    
    **- Alex, Crypto Trader**
    """)

with col2:
    st.success("""
    ⭐⭐⭐⭐⭐
    
    *"Premium alerts saved me from a major loss. The correlation analysis is incredibly detailed and accurate."*
    
    **- Sarah, Portfolio Manager**
    """)

with col3:
    st.info("""
    ⭐⭐⭐⭐⭐
    
    *"Best Kaspa analytics platform I've used. The data export feature is perfect for my research reports."*
    
    **- Mike, Blockchain Analyst**
    """)

# FAQ section
st.markdown("---")
st.subheader("❓ Frequently Asked Questions")

with st.expander("💳 How does billing work?"):
    st.write("""
    - **Monthly**: Billed $9.99 every month
    - **Annual**: Billed $99 once per year (save 17%)
    - Secure payments processed by Stripe
    - Cancel anytime with no fees
    - Instant access after payment
    """)

with st.expander("🔄 Can I cancel anytime?"):
    st.write("""
    Yes! You can cancel your subscription anytime:
    - Access continues until end of billing period
    - No cancellation fees
    - Easy cancellation through your account
    - Reactivate anytime
    """)

with st.expander("📊 What data sources do you use?"):
    st.write("""
    We aggregate data from multiple sources:
    - Kaspa blockchain (direct node access)
    - Major exchanges (price/volume data)
    - Social media platforms (sentiment)
    - On-chain analytics providers
    - Real-time network statistics
    """)

with st.expander("🔔 How do alerts work?"):
    st.write("""
    Premium users can set unlimited custom alerts:
    - Price thresholds (above/below specific values)
    - Volume spikes and unusual activity
    - Technical indicator triggers
    - On-chain metric changes
    - Delivered via email, SMS, or Discord
    """)

# Call to action
if not st.session_state.get('authentication_status'):
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.success("Ready to get started? Create your account today!")
        if st.button("🔑 Sign Up Now", use_container_width=True):
            st.switch_page("pages/0_🔑_Login.py")

# Navigation
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("Home.py")
with col2:
    if st.button("🔑 Login", use_container_width=True):
        st.switch_page("pages/0_🔑_Login.py")
with col3:
    if st.button("📊 Free Analytics", use_container_width=True):
        st.switch_page("pages/1_⛏️_Mining_Hashrate.py")
