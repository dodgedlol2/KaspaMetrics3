import streamlit as st
# Page config MUST be first!
st.set_page_config(page_title="Mining Hashrate", page_icon="📈", layout="wide")
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import sys
import os
# Add parent directory to path for imports
parent_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(parent_dir)
from database import Database
from auth_handler import AuthHandler
from payment_handler import PaymentHandler
from navigation import add_navigation
# NOW add navigation (after page config)
add_navigation()
# Initialize handlers
@st.cache_resource
def init_handlers():
    db = Database()
    auth_handler = AuthHandler(db)
    payment_handler = PaymentHandler()
    return db, auth_handler, payment_handler
db, auth_handler, payment_handler = init_handlers()

# Main content
st.title("📈 Kaspa Network Hashrate")
st.write("Current network hashrate metrics and mining trends")
# Sample data - replace with real Kaspa API data later
dates = pd.date_range(start='2024-01-01', end='2024-06-01', freq='D')
hashrate_data = np.random.normal(1.2, 0.1, len(dates))  # EH/s
# Current metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Current Hashrate", "1.24 EH/s", "+2.1%")
with col2:
    st.metric("7d Average", "1.18 EH/s", "+0.8%")
with col3:
    st.metric("30d Average", "1.15 EH/s", "+5.2%")
# Hashrate chart
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=dates,
    y=hashrate_data,
    mode='lines',
    name='Hashrate (EH/s)',
    line=dict(color='#1f77b4', width=2)
))
fig.update_layout(
    title="Kaspa Network Hashrate Over Time",
    xaxis_title="Date",
    yaxis_title="Hashrate (EH/s)",
    height=400,
    template="plotly_white"
)
st.plotly_chart(fig, use_container_width=True)
# Additional insights
st.subheader("📊 Hashrate Analysis")
col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    **Key Insights:**
    - Network hashrate has grown 15% over the past month
    - Mining difficulty adjustment maintains ~1 block per second
    - Increased hashrate indicates growing miner confidence
    - Current hashrate suggests strong network security
    """)
with col2:
    # Mini chart for recent trends
    recent_dates = dates[-30:]
    recent_data = hashrate_data[-30:]
    
    mini_fig = go.Figure()
    mini_fig.add_trace(go.Scatter(
        x=recent_dates,
        y=recent_data,
        mode='lines+markers',
        name='30-Day Trend',
        line=dict(color='#ff7f0e', width=3)
    ))
    
    mini_fig.update_layout(
        title="30-Day Hashrate Trend",
        height=250,
        template="plotly_white",
        showlegend=False
    )
    
    st.plotly_chart(mini_fig, use_container_width=True)

# Add animated DAG logo section
st.markdown("---")
st.subheader("🔗 Kaspa BlockDAG Network")

# Import components properly
import streamlit.components.v1 as components

# Animated BlockDAG Logo
dag_logo_html = """
<div style="display: flex; justify-content: center; align-items: center; padding: 20px; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 15px; margin: 20px 0;">
    <svg width="400" height="120" viewBox="0 0 400 120">
        <defs>
            <marker id="arrowhead" markerWidth="10" markerHeight="7" 
                    refX="9" refY="3.5" orient="auto">
                <polygon points="0 0, 10 3.5, 0 7" fill="#49d49d"/>
            </marker>
            <style>
                .dag-block {
                    fill: #49d49d;
                    opacity: 0;
                    rx: 3;
                }
                .dag-connection {
                    stroke: #49d49d;
                    stroke-width: 2;
                    opacity: 0;
                    marker-end: url(#arrowhead);
                }
                .logo-text {
                    font-family: 'Arial', sans-serif;
                    font-weight: bold;
                    font-size: 32px;
                    fill: #2c3e50;
                    letter-spacing: -1px;
                }
                .logo-subtext {
                    font-size: 14px;
                    fill: #7f8c8d;
                    font-weight: normal;
                    letter-spacing: 2px;
                }
                .block1 { animation: block-appear 6s ease-in-out infinite; }
                .block2 { animation: block-appear 6s ease-in-out infinite 0.4s; }
                .block3 { animation: block-appear 6s ease-in-out infinite 0.8s; }
                .block4 { animation: block-appear 6s ease-in-out infinite 1.2s; }
                .block5 { animation: block-appear 6s ease-in-out infinite 1.6s; }
                .block6 { animation: block-appear 6s ease-in-out infinite 2s; }
                .block7 { animation: block-appear 6s ease-in-out infinite 2.4s; }
                .block8 { animation: block-appear 6s ease-in-out infinite 2.8s; }
                
                .conn1 { animation: connection-appear 6s ease-in-out infinite 0.6s; }
                .conn2 { animation: connection-appear 6s ease-in-out infinite 1s; }
                .conn3 { animation: connection-appear 6s ease-in-out infinite 1.4s; }
                .conn4 { animation: connection-appear 6s ease-in-out infinite 1.8s; }
                .conn5 { animation: connection-appear 6s ease-in-out infinite 2.2s; }
                .conn6 { animation: connection-appear 6s ease-in-out infinite 2.6s; }
                .conn7 { animation: connection-appear 6s ease-in-out infinite 3s; }
                .conn8 { animation: connection-appear 6s ease-in-out infinite 3.4s; }
                
                @keyframes block-appear {
                    0%, 15% { opacity: 0; transform: scale(0); }
                    20%, 85% { opacity: 0.8; transform: scale(1); }
                    100% { opacity: 0.8; transform: scale(1); }
                }
                @keyframes connection-appear {
                    0%, 10% { opacity: 0; }
                    15%, 85% { opacity: 0.6; }
                    100% { opacity: 0.6; }
                }
                .text-reveal {
                    opacity: 0;
                    animation: text-fade-in 2s ease-out 1s forwards;
                }
                @keyframes text-fade-in {
                    0% { opacity: 0; transform: translateY(10px); }
                    100% { opacity: 1; transform: translateY(0); }
                }
            </style>
        </defs>
        
        <!-- BlockDAG Structure -->
        <!-- Genesis block -->
        <rect class="dag-block block1" x="15" y="55" width="12" height="12"/>
        
        <!-- Layer 1 -->
        <rect class="dag-block block2" x="40" y="30" width="12" height="12"/>
        <rect class="dag-block block3" x="40" y="55" width="12" height="12"/>
        <rect class="dag-block block4" x="40" y="80" width="12" height="12"/>
        
        <!-- Layer 2 -->
        <rect class="dag-block block5" x="65" y="40" width="12" height="12"/>
        <rect class="dag-block block6" x="65" y="70" width="12" height="12"/>
        
        <!-- Layer 3 -->
        <rect class="dag-block block7" x="90" y="45" width="12" height="12"/>
        <rect class="dag-block block8" x="90" y="65" width="12" height="12"/>
        
        <!-- Connections -->
        <line class="dag-connection conn1" x1="27" y1="61" x2="40" y2="36"/>
        <line class="dag-connection conn2" x1="27" y1="61" x2="40" y2="61"/>
        <line class="dag-connection conn3" x1="27" y1="61" x2="40" y2="86"/>
        <line class="dag-connection conn4" x1="52" y1="36" x2="65" y2="46"/>
        <line class="dag-connection conn5" x1="52" y1="61" x2="65" y2="46"/>
        <line class="dag-connection conn6" x1="52" y1="61" x2="65" y2="76"/>
        <line class="dag-connection conn7" x1="77" y1="46" x2="90" y2="51"/>
        <line class="dag-connection conn8" x1="77" y1="76" x2="90" y2="71"/>
        
        <!-- Text -->
        <text x="120" y="50" class="logo-text text-reveal">KASPA</text>
        <text x="120" y="75" class="logo-subtext text-reveal">METRICS</text>
    </svg>
</div>
"""

components.html(dag_logo_html, height=160)

st.markdown("""
<div style="text-align: center; margin-top: 10px; color: #666;">
    <em>Visualizing Kaspa's BlockDAG structure - where blocks form in parallel rather than a single chain</em>
</div>
""", unsafe_allow_html=True)

# Navigation
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("⚙️ Mining Difficulty", use_container_width=True):
        st.switch_page("pages/2_⛏️_Mining_Difficulty.py")
with col2:
    if st.button("💰 Price Data", use_container_width=True):
        st.switch_page("pages/3_💰_Spot_Price.py")
with col3:
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("Home.py")
