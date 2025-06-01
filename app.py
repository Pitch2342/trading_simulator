import streamlit as st
import os
import time
from utils.data_handler import load_data, extract_breakpoints
from components.price_chart import render_progressive_chart
from components.trading_interface import render_trading_interface
from components.portfolio_stats import render_portfolio_stats, render_performance_charts
from components.admin_panel import render_admin_panel
from utils.session_manager import initialize_session_state, reset_simulation_state
from utils.portfolio_manager import initialize_portfolios, update_player_portfolios

# Player colors for consistent visualization
PLAYER_COLORS = {
    1: '#1f77b4',  # Blue
    2: '#ff7f0e',  # Orange
    3: '#2ca02c',  # Green
    4: '#d62728'   # Red
}

# Page configuration
st.set_page_config(
    page_title="Trading Decision Simulator",
    page_icon="📈",
    layout="wide"
)

def handle_ticker_selection():
    """Handle ticker selection and reset simulation state accordingly"""
    available_tickers = [f.replace(".csv", "") for f in os.listdir('data') if f.endswith('.csv')]
    selected_ticker = st.selectbox(
        "Select Ticker",
        options=available_tickers,
        index=available_tickers.index(st.session_state.selected_ticker) if st.session_state.selected_ticker in available_tickers else 0
    )
    
    if selected_ticker != st.session_state.selected_ticker:
        st.session_state.selected_ticker = selected_ticker
        st.session_state.current_day_index = 0
        st.session_state.portfolios = initialize_portfolios(st.session_state.num_players, st.session_state.starting_cash)
        reset_simulation_state()
        st.rerun()

def handle_progress_controls():
    """Handle start/stop buttons"""
    st.markdown("### Progress Control")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Start"):
            st.session_state.auto_progress = True
            st.session_state.waiting_for_trade = False
            st.session_state.trade_made = False
            st.session_state.current_day_index += 1
            st.rerun()
    
    with col2:
        if st.button("Stop"):
            st.session_state.auto_progress = False
            st.rerun()

def render_trading_grid(df, current_day_index, breakpoints):
    """Render the trading decision grid for all players"""
    with st.container():
        # Create a 2x2 grid for trading decisions
        for row in range(2):
            cols = st.columns(2)
            for col in range(2):
                player_num = row * 2 + col + 1
                if player_num <= st.session_state.num_players:
                    with cols[col]:
                        with st.container(border=True):
                            # Trading decision tile
                            if current_day_index in breakpoints:
                                st.session_state.waiting_for_trade = True
                            render_trading_interface(
                                df.iloc[current_day_index]['Price'],
                                st.session_state.portfolios[player_num],
                                player_num,
                                is_breakpoint=current_day_index in breakpoints
                            )

def handle_auto_progress(df):
    """Handle automatic progression logic"""
    if st.session_state.auto_progress and not st.session_state.waiting_for_trade:
        if st.session_state.current_day_index < len(df) - 1:
            sleep_interval = st.session_state.time_to_run_sec / len(df)
            time.sleep(sleep_interval)
            st.session_state.current_day_index += 1
            st.rerun()
        else:
            st.session_state.auto_progress = False
            st.warning("You've reached the end of the simulation!")

def inject_custom_css():
    """Inject custom CSS styling"""
    st.markdown(
        '''
        <style>
        /* Make metric values auto-size and prevent truncation */
        div[data-testid="stMetricValue"] {
            font-size: clamp(1.2rem, 4vw, 2.5rem);
            white-space: nowrap;
            overflow: visible;
            text-overflow: initial;
        }
        </style>
        ''' ,
        unsafe_allow_html=True
    )

def main():
    # Initialize session state
    initialize_session_state()
    
    # Create header with title and progress controls
    header_col1, header_col2 = st.columns([3, 1])
    
    with header_col1:
        st.title("Trading Decision Simulator")
        handle_ticker_selection()
    
    with header_col2:
        handle_progress_controls()
    
    # Load selected ticker data
    ticker_path = os.path.join('data', f"{st.session_state.selected_ticker}.csv")
    df = load_data(ticker_path)
    breakpoints = extract_breakpoints(df)
    
    # Ensure current_day_index is within bounds
    if st.session_state.current_day_index >= len(df):
        st.session_state.current_day_index = len(df) - 1
    
    # Main simulation area
    col1, col2 = st.columns([3, 1])  # 75% for chart, 25% for trading decisions
    
    with col1:
        render_progressive_chart(df, st.session_state.current_day_index, breakpoints)
    
    with col2:
        render_trading_grid(df, st.session_state.current_day_index, breakpoints)

    # Render portfolio statistics
    render_portfolio_stats(df, st.session_state.current_day_index)
    
    # Render performance charts and trading history
    render_performance_charts()

    # Handle auto progress logic
    handle_auto_progress(df)

    # Render admin settings panel
    render_admin_panel(df, breakpoints)

    # Inject custom CSS
    inject_custom_css()

if __name__ == "__main__":
    main()
