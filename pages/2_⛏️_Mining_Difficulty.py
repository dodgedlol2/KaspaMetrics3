import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def show():
    st.title("⚙️ Mining Difficulty")
    st.write("Network difficulty adjustments and mining complexity")
    
    # Sample difficulty data
    dates = pd.date_range(start='2024-01-01', end='2024-06-01', freq='D')
    difficulty_data = np.random.normal(15.5e12, 1e12, len(dates))
    
    # Current metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Current Difficulty", "15.8T", "+1.2%")
    with col2:
        st.metric("Next Adjustment", "~2 days", "")
    with col3:
        st.metric("Est. Change", "+0.8%", "")
    
    # Difficulty chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates,
        y=difficulty_data,
        mode='lines',
        name='Difficulty',
        line=dict(color='#ff7f0e', width=2)
    ))
    
    fig.update_layout(
        title="Mining Difficulty Over Time",
        xaxis_title="Date",
        yaxis_title="Difficulty",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
