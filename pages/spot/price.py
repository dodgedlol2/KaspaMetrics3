import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def show():
    st.title("💰 Kaspa Price")
    st.write("Real-time price data and market trends")
    
    # Sample price data
    dates = pd.date_range(start='2024-01-01', end='2024-06-01', freq='H')
    price_data = np.random.normal(0.125, 0.01, len(dates))
    
    # Current metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Current Price", "$0.1247", "+2.4%")
    with col2:
        st.metric("24h High", "$0.1289", "")
    with col3:
        st.metric("24h Low", "$0.1205", "")
    with col4:
        st.metric("24h Change", "+$0.0029", "+2.4%")
    
    # Price chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates[-168:],  # Last 7 days
        y=price_data[-168:],
        mode='lines',
        name='KAS/USD',
        line=dict(color='#2ca02c', width=2)
    ))
    
    fig.update_layout(
        title="KAS/USD Price (7 Days)",
        xaxis_title="Time",
        yaxis_title="Price (USD)",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
