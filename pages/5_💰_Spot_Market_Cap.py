import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def show():
    st.title("🏦 Market Capitalization")
    st.write("Kaspa market cap and ranking metrics")
    
    # Sample market cap data
    dates = pd.date_range(start='2024-01-01', end='2024-06-01', freq='D')
    mcap_data = np.random.normal(3100000000, 200000000, len(dates))
    
    # Current metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Market Cap", "$3.14B", "+1.8%")
    with col2:
        st.metric("Rank", "#32", "↑2")
    with col3:
        st.metric("Circulating Supply", "25.2B KAS", "")
    with col4:
        st.metric("Max Supply", "28.7B KAS", "")
    
    # Market cap chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates,
        y=mcap_data,
        mode='lines',
        name='Market Cap',
        line=dict(color='#9467bd', width=2),
        fill='tonexty'
    ))
    
    fig.update_layout(
        title="Market Capitalization Over Time",
        xaxis_title="Date",
        yaxis_title="Market Cap (USD)",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
