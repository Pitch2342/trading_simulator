import streamlit as st
from utils.pnl_calculator import PnLCalculator

def reset_all_portfolios():
    """Reset all portfolios with the current starting cash amount"""
    for i in range(1, st.session_state.num_players + 1):
        st.session_state.portfolios[i] = {
            'cash': st.session_state.starting_cash,
            'positions': 0,
            'pnl_calculator': PnLCalculator(initial_cash=st.session_state.starting_cash),
            'trading_history': []
        }

def initialize_portfolios(num_players: int, starting_cash: float):
    """Initialize portfolios for all players"""
    portfolios = {}
    for i in range(1, num_players + 1):
        portfolios[i] = {
            'cash': starting_cash,
            'positions': 0,
            'pnl_calculator': PnLCalculator(initial_cash=starting_cash),
            'trading_history': []
        }
    return portfolios

def initialize_player_names(num_players: int):
    """Initialize default player names"""
    return {i: f"Player {i}" for i in range(1, num_players + 1)}

def update_player_portfolios(num_players: int):
    """Update portfolios when number of players changes"""
    new_portfolios = {}
    new_player_names = {}
    
    for i in range(1, num_players + 1):
        if i in st.session_state.portfolios:
            new_portfolios[i] = st.session_state.portfolios[i]
            new_player_names[i] = st.session_state.player_names[i]
        else:
            new_portfolios[i] = {
                'cash': st.session_state.starting_cash,
                'positions': 0,
                'pnl_calculator': PnLCalculator(initial_cash=st.session_state.starting_cash),
                'trading_history': []
            }
            new_player_names[i] = f"Player {i}"
    
    return new_portfolios, new_player_names 