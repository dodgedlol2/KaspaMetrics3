import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def show():
    st.title("📊 Advanced Metrics")
    st.write("Deep dive analytics and custom indicators")
    
    # Advanced metrics grid
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("MVRV Ratio", "1.85", "+0.12")
    with col2:
        st.metric("NVT Ratio", "28.4", "-2.1")
    with col3:
        st.metric("Active Addresses", "12.5K", "+8.2%")
    with col4:
        st.metric("Transaction Count", "45.2K", "+5.7%")
    
    # Correlation matrix
    st.subheader("Correlation Analysis")
    
    # Sample correlation data
    metrics = ['Price', 'Volume', 'Hashrate', 'Active Addresses', 'Transaction Count']
    correlation_matrix = np.random.rand(5, 5)
    correlation_matrix = (correlation_matrix + correlation_matrix.T) / 2  # Make symmetric
    np.fill_diagonal(correlation_matrix, 1)  # Diagonal should be 1
    
    fig = go.Figure(data=go.Heatmap(
        z=correlation_matrix,
        x=metrics,
        y=metrics,
        colorscale='RdBu',
        zmid=0
    ))
    
    fig.update_layout(
        title="Metrics Correlation Matrix",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Custom alerts
    st.subheader("🔔 Custom Alerts")
    
    alert_col1, alert_col2 = st.columns(2)
    with alert_col1:
        st.selectbox("Metric", ["Price", "Volume", "Hashrate"])
        st.selectbox("Condition", ["Above", "Below", "Change %"])
        st.number_input("Threshold", value=0.15)
    
    with alert_col2:
        st.text_input("Alert Name", "Price Alert")
        st.selectbox("Notification", ["Email", "SMS", "Discord"])
        st.button("Create Alert", type="primary")
