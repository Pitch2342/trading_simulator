import streamlit as st
from utils.data_handler import load_data, extract_breakpoints
from components.price_chart import render_progressive_chart
from components.trading_interface import render_trading_interface
from utils.pnl_calculator import PnLCalculator
import os
import time
import plotly.graph_objects as go

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

# Initialize session state
if 'current_day_index' not in st.session_state:
    st.session_state.current_day_index = 0
if 'num_players' not in st.session_state:
    st.session_state.num_players = 1
if 'portfolios' not in st.session_state:
    st.session_state.portfolios = {
        1: {'cash': 10000, 'positions': 0, 'pnl_calculator': PnLCalculator(), 'trading_history': []}
    }
if 'auto_progress' not in st.session_state:
    st.session_state.auto_progress = False
if 'waiting_for_trade' not in st.session_state:
    st.session_state.waiting_for_trade = False
if 'trade_made' not in st.session_state:
    st.session_state.trade_made = False
if 'selected_ticker' not in st.session_state:
    st.session_state.selected_ticker = 'SAMPLE_SWINGS.csv'

def main():
    # Create header with title and progress controls
    header_col1, header_col2 = st.columns([3, 1])
    with header_col1:
        st.title("Trading Decision Simulator")
        # Add ticker selection dropdown
        available_tickers = [f.replace(".csv", "") for f in os.listdir('data') if f.endswith('.csv')]
        selected_ticker = st.selectbox(
            "Select Ticker",
            options=available_tickers,
            index=available_tickers.index(st.session_state.selected_ticker) if st.session_state.selected_ticker in available_tickers else 0
        )
        if selected_ticker != st.session_state.selected_ticker:
            st.session_state.selected_ticker = selected_ticker
            st.session_state.current_day_index = 0
            st.session_state.portfolios = {
                i: {'cash': 10000, 'positions': 0, 'pnl_calculator': PnLCalculator(), 'trading_history': []}
                for i in range(1, st.session_state.num_players + 1)
            }
            st.session_state.auto_progress = False
            st.session_state.waiting_for_trade = False
            st.session_state.trade_made = False
            st.experimental_rerun()
    with header_col2:
        st.markdown("### Progress Control")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Start"):
                st.session_state.auto_progress = True
                st.session_state.waiting_for_trade = False
                st.session_state.trade_made = False
                st.session_state.current_day_index += 1
                st.experimental_rerun()
        with col2:
            if st.button("Stop"):
                st.session_state.auto_progress = False
                st.experimental_rerun()
        with col3:
            num_players = st.number_input("Number of Players", min_value=1, max_value=4, value=st.session_state.num_players)
            if num_players != st.session_state.num_players:
                st.session_state.num_players = num_players
                # Initialize new players or remove excess players
                new_portfolios = {}
                for i in range(1, num_players + 1):
                    if i in st.session_state.portfolios:
                        new_portfolios[i] = st.session_state.portfolios[i]
                    else:
                        new_portfolios[i] = {'cash': 10000, 'positions': 0, 'pnl_calculator': PnLCalculator(), 'trading_history': []}
                st.session_state.portfolios = new_portfolios
                st.experimental_rerun()
    
    # Load selected ticker data
    ticker_path = os.path.join('data', f"{st.session_state.selected_ticker}.csv")
    df = load_data(ticker_path)
    breakpoints = extract_breakpoints(df)
    
    # Ensure current_day_index is within bounds
    if st.session_state.current_day_index >= len(df):
        st.session_state.current_day_index = len(df) - 1
    
    # Main simulation area
    col1, col2 = st.columns([3, 1])  # 75% for chart, 25% for tiles
    
    with col1:
        render_progressive_chart(df, st.session_state.current_day_index, breakpoints)
    
    with col2:
        # Create a container for each player
        for player_num in range(1, st.session_state.num_players + 1):
            with st.container(border=True):
                st.markdown(f"#### Player {player_num}")
                # Trading decision tile
                if st.session_state.current_day_index in breakpoints:
                    st.session_state.waiting_for_trade = True
                    render_trading_interface(
                        df.iloc[st.session_state.current_day_index]['Price'],
                        st.session_state.portfolios[player_num],
                        player_num
                    )
                else:
                    st.session_state.waiting_for_trade = False
                    st.info("No trading decision needed", icon="ℹ️")
                
                # Current position tile
                current_price = df.iloc[st.session_state.current_day_index]['Price']
                st.session_state.portfolios[player_num]['pnl_calculator'].update_portfolio_value(current_price)
                portfolio_value = st.session_state.portfolios[player_num]['pnl_calculator'].get_portfolio_value(current_price)
                
                # Display position information in a 2x2 tile layout
                row1_col1, row1_col2 = st.columns(2)
                with row1_col1:
                    st.metric("Cash", f"${st.session_state.portfolios[player_num]['cash']:.2f}")
                with row1_col2:
                    st.metric("Portfolio", f"${portfolio_value:.2f}")

                row2_col1, row2_col2 = st.columns(2)
                with row2_col1:
                    st.metric("Positions", f"{st.session_state.portfolios[player_num]['positions']}")
                with row2_col2:
                    st.metric("PnL", f"${st.session_state.portfolios[player_num]['pnl_calculator'].get_current_pnl():.2f}")

                if st.session_state.current_day_index > 0:
                    metrics = st.session_state.portfolios[player_num]['pnl_calculator'].get_performance_metrics()
                    row3_col1, row3_col2 = st.columns(2)
                    with row3_col1:
                        st.metric(
                            "Total Return",
                            f"{metrics['total_return']:.2f}%",
                            delta=f"{metrics['total_return']:.2f}%"
                        )
                    with row3_col2:
                        st.metric(
                            "Max Drawdown",
                            f"{metrics['max_drawdown']:.2f}%"
                        )
    
    # Performance metrics
    if st.session_state.current_day_index > 0:
        # Create portfolio value chart
        fig = go.Figure()
        
        for player_num in range(1, st.session_state.num_players + 1):
            if len(st.session_state.portfolios[player_num]['trading_history']) > 0:
                daily_metrics = st.session_state.portfolios[player_num]['pnl_calculator'].daily_metrics
                if not daily_metrics.empty:
                    fig.add_trace(go.Scatter(
                        x=daily_metrics['date'],
                        y=daily_metrics['portfolio_value'],
                        mode='lines',
                        name=f'Player {player_num}',
                        line=dict(color=PLAYER_COLORS[player_num])
                    ))
        
        fig.update_layout(
            title='Portfolio Values Over Time',
            xaxis_title='Date',
            yaxis_title='Value ($)',
            showlegend=True,
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Display trading history for all players
        st.subheader("Trading History")
        for player_num in range(1, st.session_state.num_players + 1):
            st.markdown(f"**Player {player_num}**")
            for i, trade in enumerate(st.session_state.portfolios[player_num]['trading_history'], 1):
                st.write(f"Trade {i}: {trade['action'].upper()} {trade['quantity']} @ ${trade['price']:.2f}")

    # Auto progress logic
    if st.session_state.auto_progress and not st.session_state.waiting_for_trade:
        if st.session_state.current_day_index < len(df) - 1:
            time.sleep(1)  # Sleep for 1 second
            st.session_state.current_day_index += 1
            st.experimental_rerun()
        else:
            st.session_state.auto_progress = False
            st.warning("You've reached the end of the simulation!")

    # Inject custom CSS
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

if __name__ == "__main__":
    main()
