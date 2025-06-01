# Player colors for consistent visualization
PLAYER_COLORS = {
    1: '#1f77b4',  # Blue
    2: '#ff7f0e',  # Orange
    3: '#9467bd',  # Purple
    4: '#8c564b'   # Brown
}

CURRENCY_INDICATOR = '₹'

def get_hoverlabel_config():
    """Get consistent hoverlabel configuration for all charts"""
    import streamlit as st
    return dict(
        font=dict(size=st.session_state.chart_hoverlabel_font_size)
    )