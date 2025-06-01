import streamlit as st
from utils.pnl_calculator import PnLCalculator
from utils.portfolio_manager import initialize_portfolios, initialize_player_names

def initialize_session_state():
    """Initialize all session state variables"""
    if 'current_day_index' not in st.session_state:
        st.session_state.current_day_index = 0
    if 'num_players' not in st.session_state:
        st.session_state.num_players = 1
    if 'starting_cash' not in st.session_state:
        st.session_state.starting_cash = 10000
    if 'time_to_run_sec' not in st.session_state:
        st.session_state.time_to_run_sec = 10
    if 'portfolios' not in st.session_state:
        st.session_state.portfolios = initialize_portfolios(1, 10000)
    if 'player_names' not in st.session_state:
        st.session_state.player_names = initialize_player_names(1)
    if 'auto_progress' not in st.session_state:
        st.session_state.auto_progress = False
    if 'waiting_for_trade' not in st.session_state:
        st.session_state.waiting_for_trade = False
    if 'trade_made' not in st.session_state:
        st.session_state.trade_made = False
    if 'selected_ticker' not in st.session_state:
        st.session_state.selected_ticker = 'SAMPLE_SWINGS'
    if 'uploaded_data' not in st.session_state:
        st.session_state.uploaded_data = None
    if 'data_source' not in st.session_state:
        st.session_state.data_source = 'predefined'  # 'predefined' or 'uploaded'

def reset_simulation_state():
    """Reset simulation-specific state variables"""
    st.session_state.current_day_index = 0
    st.session_state.auto_progress = False
    st.session_state.waiting_for_trade = False
    st.session_state.trade_made = False 