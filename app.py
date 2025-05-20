import streamlit as st
from utils.data_handler import load_data, extract_breakpoints
from components.price_chart import render_progressive_chart
from components.trading_interface import render_trading_interface
from components.performance_metrics import render_performance_metrics
from utils.pnl_calculator import PnLCalculator
import os
import time

# Page configuration
st.set_page_config(
    page_title="Trading Decision Simulator",
    page_icon="📈",
    layout="wide"
)

# Initialize session state
if 'current_day_index' not in st.session_state:
    st.session_state.current_day_index = 0
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = {'cash': 10000, 'positions': 0}
if 'pnl_calculator' not in st.session_state:
    st.session_state.pnl_calculator = PnLCalculator()
if 'trading_history' not in st.session_state:
    st.session_state.trading_history = []
if 'auto_progress' not in st.session_state:
    st.session_state.auto_progress = False
if 'waiting_for_trade' not in st.session_state:
    st.session_state.waiting_for_trade = False
if 'trade_made' not in st.session_state:
    st.session_state.trade_made = False

def main():
    st.title("Trading Decision Simulator")
    
    # Load predefined AAPL ticker data
    ticker_path = os.path.join('data', 'AAPL.csv')
    df = load_data(ticker_path)
    breakpoints = extract_breakpoints(df)
    
    # Ensure current_day_index is within bounds
    if st.session_state.current_day_index >= len(df):
        st.session_state.current_day_index = len(df) - 1
    
    # Main simulation area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Render progressive chart
        render_progressive_chart(df, st.session_state.current_day_index, breakpoints)
        
        # Display current position and PnL
        st.subheader("Current Position")
        current_price = df.iloc[st.session_state.current_day_index]['Price']
        st.session_state.pnl_calculator.update_portfolio_value(current_price)
        portfolio_value = st.session_state.pnl_calculator.get_portfolio_value(current_price)
        
        st.write(f"Cash: ${st.session_state.portfolio['cash']:.2f}")
        st.write(f"Positions: {st.session_state.portfolio['positions']}")
        st.write(f"Current Price: ${current_price:.2f}")
        st.write(f"Total Portfolio Value: ${portfolio_value:.2f}")
        st.write(f"Current PnL: ${st.session_state.pnl_calculator.get_current_pnl():.2f}")
    
    with col2:
        # Trading interface
        if st.session_state.current_day_index in breakpoints:
            st.session_state.waiting_for_trade = True
            render_trading_interface(
                df.iloc[st.session_state.current_day_index]['Price'],
                st.session_state.portfolio
            )
            
            # Show Continue button after trade is made
            if st.session_state.trade_made:
                if st.button("Continue"):
                    st.session_state.waiting_for_trade = False
                    st.session_state.trade_made = False
                    st.session_state.current_day_index += 1
                    st.experimental_rerun()
        else:
            st.session_state.waiting_for_trade = False
        
        # Progress control - only show if not at a breakpoint
        if not st.session_state.waiting_for_trade:
            if st.button("Start Auto Progress"):
                st.session_state.auto_progress = True
                st.experimental_rerun()
            
            if st.button("Stop Auto Progress"):
                st.session_state.auto_progress = False
                st.experimental_rerun()
    
    # Performance metrics
    if st.session_state.current_day_index > 0:
        render_performance_metrics(st.session_state.trading_history)
    
    # Auto progress logic
    if st.session_state.auto_progress and not st.session_state.waiting_for_trade:
        if st.session_state.current_day_index < len(df) - 1:
            time.sleep(1)  # Sleep for 1 second
            st.session_state.current_day_index += 1
            st.experimental_rerun()
        else:
            st.session_state.auto_progress = False
            st.warning("You've reached the end of the simulation!")

if __name__ == "__main__":
    main()
