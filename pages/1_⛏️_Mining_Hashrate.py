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
# Import components properly
import streamlit.components.v1 as components

# Optimized Animated BlockDAG Logo with minimal space
dag_logo_html = """
<div style="display: flex; justify-content: center; align-items: center; padding: 0; margin: 0;">
    <svg width="320" height="80" viewBox="0 0 320 80" style="display: block;">
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
                    font-size: 28px;
                    fill: #2c3e50;
                    letter-spacing: -1px;
                }
                .logo-subtext {
                    font-size: 12px;
                    fill: #7f8c8d;
                    font-weight: normal;
                    letter-spacing: 1.5px;
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
        <rect class="dag-block block1" x="15" y="35" width="10" height="10"/>
        
        <!-- Layer 1 -->
        <rect class="dag-block block2" x="35" y="15" width="10" height="10"/>
        <rect class="dag-block block3" x="35" y="35" width="10" height="10"/>
        <rect class="dag-block block4" x="35" y="55" width="10" height="10"/>
        
        <!-- Layer 2 -->
        <rect class="dag-block block5" x="55" y="25" width="10" height="10"/>
        <rect class="dag-block block6" x="55" y="45" width="10" height="10"/>
        
        <!-- Layer 3 -->
        <rect class="dag-block block7" x="75" y="30" width="10" height="10"/>
        <rect class="dag-block block8" x="75" y="40" width="10" height="10"/>
        
        <!-- Connections -->
        <line class="dag-connection conn1" x1="25" y1="40" x2="35" y2="20"/>
        <line class="dag-connection conn2" x1="25" y1="40" x2="35" y2="40"/>
        <line class="dag-connection conn3" x1="25" y1="40" x2="35" y2="60"/>
        <line class="dag-connection conn4" x1="45" y1="20" x2="55" y2="30"/>
        <line class="dag-connection conn5" x1="45" y1="40" x2="55" y2="30"/>
        <line class="dag-connection conn6" x1="45" y1="40" x2="55" y2="50"/>
        <line class="dag-connection conn7" x1="65" y1="30" x2="75" y2="35"/>
        <line class="dag-connection conn8" x1="65" y1="50" x2="75" y2="45"/>
        
        <!-- Text -->
        <text x="100" y="35" class="logo-text text-reveal">KASPA</text>
        <text x="100" y="52" class="logo-subtext text-reveal">METRICS</text>
    </svg>
</div>
"""

# Use a smaller height to minimize space
components.html(dag_logo_html, height=90)

st.markdown("""
<div style="text-align: center; margin-top: 5px; color: #666;">
    <em>Visualizing Kaspa's BlockDAG structure - where blocks form in parallel rather than a single chain</em>
</div>
""", unsafe_allow_html=True)
