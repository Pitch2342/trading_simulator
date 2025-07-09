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

# Page configuration
st.set_page_config(
    page_title="Trading Decision Simulator",
    page_icon="📈",
    layout="wide"
)

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
    # Store current date in session state for trading history
    st.session_state.current_date = df.iloc[current_day_index]['Date']
    
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
        # # Display current data source info
        # if st.session_state.data_source == 'uploaded':
        #     if st.session_state.uploaded_data is not None:
        #         st.caption("📊 Using custom uploaded data")
        #     else:
        #         st.caption("📤 Ready to upload custom data - use Admin Settings below")
        # else:
        #     st.caption(f"📈 Current Ticker: {st.session_state.selected_ticker}")
    
    with header_col2:
        # Only show progress controls if we have data to work with
        if st.session_state.data_source == 'predefined' or st.session_state.uploaded_data is not None:
            handle_progress_controls()
    
    # Load data based on selected source
    if st.session_state.data_source == 'uploaded':
        if st.session_state.uploaded_data is not None:
            df = st.session_state.uploaded_data
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
        else:
            # Show upload interface prominently when no data is uploaded
            st.info("🚀 **Ready to upload your custom trading data!** Use the Admin Settings panel below to get started.")
            # Force admin panel to be expanded when no data is uploaded
            df = None
            breakpoints = []
    else:
        # Load predefined ticker data
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

    # Render admin settings panel - force expanded if no uploaded data
    should_expand = st.session_state.data_source == 'uploaded' and st.session_state.uploaded_data is None
    render_admin_panel(df, breakpoints, force_expanded=should_expand)

    # Inject custom CSS
    inject_custom_css()

if __name__ == "__main__":
    main()
