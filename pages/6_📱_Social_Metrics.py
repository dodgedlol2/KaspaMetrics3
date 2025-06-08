import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def show():
    st.title("📱 Social Metrics")
    st.write("Kaspa community engagement and social sentiment")
    
    # Social metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Twitter Followers", "285K", "+1.2%")
    with col2:
        st.metric("Reddit Members", "42K", "+2.8%")
    with col3:
        st.metric("Discord Members", "18K", "+0.5%")
    with col4:
        st.metric("Social Score", "8.2/10", "+0.1")
    
    # Sample sentiment data
    dates = pd.date_range(start='2024-05-01', end='2024-06-01', freq='D')
    sentiment_data = np.random.normal(0.65, 0.15, len(dates))
    
    # Sentiment chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates,
        y=sentiment_data,
        mode='lines+markers',
        name='Sentiment Score',
        line=dict(color='#17becf', width=2)
    ))
    
    fig.update_layout(
        title="Social Sentiment Trend",
        xaxis_title="Date",
        yaxis_title="Sentiment Score",
        height=300
    )
    
    st.plotly_chart(fig, use_container_width=True)
