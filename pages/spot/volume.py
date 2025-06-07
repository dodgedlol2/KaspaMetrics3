import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def show():
    st.title("📊 Trading Volume")
    st.write("24h trading volume across exchanges")
    
    # Sample volume data
    dates = pd.date_range(start='2024-01-01', end='2024-06-01', freq='D')
    volume_data = np.random.normal(45000000, 10000000, len(dates))
    
    # Current metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("24h Volume", "$42.8M", "-5.2%")
    with col2:
        st.metric("7d Average", "$47.2M", "+2.1%")
    with col3:
        st.metric("Volume Rank", "#45", "")
    
    # Volume chart
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=dates[-30:],  # Last 30 days
        y=volume_data[-30:],
        name='Volume (USD)',
        marker_color='#d62728'
    ))
    
    fig.update_layout(
        title="Daily Trading Volume (30 Days)",
        xaxis_title="Date",
        yaxis_title="Volume (USD)",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
