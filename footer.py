import streamlit as st
import streamlit.components.v1 as components

def add_footer():
    """Add consistent footer with animated DAG logo to all pages"""
    
    # Add animated DAG logo section
    st.markdown("---")
    
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
