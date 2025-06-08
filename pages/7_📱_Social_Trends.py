import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def show():
    st.title("📈 Social Trends")
    st.write("Trending topics and community discussions")
    
    # Trending topics
    st.subheader("Trending Topics")
    topics = ["Mining Updates", "Price Analysis", "Tech Developments", "Community Events"]
    engagement = [1250, 890, 650, 420]
    
    # Trending topics chart
    fig = go.Figure(data=[
        go.Bar(x=topics, y=engagement, marker_color='#bcbd22')
    ])
    
    fig.update_layout(
        title="Topic Engagement (Last 24h)",
        xaxis_title="Topics",
        yaxis_title="Engagement Score",
        height=300
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Recent mentions
    st.subheader("Recent Mentions")
    mentions_data = {
        "Platform": ["Twitter", "Reddit", "Discord", "Telegram"],
        "Mentions": [1540, 820, 450, 320],
        "Sentiment": ["Positive", "Neutral", "Positive", "Positive"]
    }
    
    df = pd.DataFrame(mentions_data)
    st.dataframe(df, use_container_width=True)
