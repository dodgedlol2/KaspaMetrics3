import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def show():
    st.title("🔨 test Kaspa Hashrate")
    st.write("Current network hashrate metrics and trends")
    
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
        title="Kaspa Network Hashrate",
        xaxis_title="Date",
        yaxis_title="Hashrate (EH/s)",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
