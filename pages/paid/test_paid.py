import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def show():
    st.title("🔒 Premium Analytics")
    st.write("Advanced analytics and insights for premium subscribers")
    
    # Premium metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Whale Activity", "High", "↑15%")
    with col2:
        st.metric("Flow Ratio", "1.24", "+0.08")
    with col3:
        st.metric("Network Value", "$2.8B", "+3.2%")
    
    # Advanced chart with multiple metrics
    dates = pd.date_range(start='2024-01-01', end='2024-06-01', freq='D')
    
    fig = go.Figure()
    
    # Price
    price_data = np.random.normal(0.125, 0.01, len(dates))
    fig.add_trace(go.Scatter(
        x=dates, y=price_data, name='Price', 
        line=dict(color='#1f77b4'), yaxis='y'
    ))
    
    # Volume (secondary y-axis)
    volume_data = np.random.normal(45000000, 10000000, len(dates))
    fig.add_trace(go.Scatter(
        x=dates, y=volume_data, name='Volume',
        line=dict(color='#ff7f0e'), yaxis='y2'
    ))
    
    fig.update_layout(
        title="Premium Multi-Metric Analysis",
        xaxis_title="Date",
        yaxis=dict(title="Price (USD)", side="left"),
        yaxis2=dict(title="Volume (USD)", side="right", overlaying="y"),
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Premium insights
    st.subheader("🎯 AI-Powered Insights")
    st.info("📊 Current market conditions suggest accumulation phase based on on-chain metrics")
    st.success("🚀 Technical indicators show potential breakout in 7-14 days")
    st.warning("⚠️ Whale activity increased by 15% - monitor for potential volatility")
