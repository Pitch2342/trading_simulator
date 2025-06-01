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
if 'starting_cash' not in st.session_state:
    st.session_state.starting_cash = 10000
if 'time_to_run_sec' not in st.session_state:
    st.session_state.time_to_run_sec = 10
if 'portfolios' not in st.session_state:
    st.session_state.portfolios = {
        1: {'cash': st.session_state.starting_cash, 'positions': 0, 'pnl_calculator': PnLCalculator(), 'trading_history': []}
    }
if 'player_names' not in st.session_state:
    st.session_state.player_names = {
        1: "Player 1"
    }
if 'auto_progress' not in st.session_state:
    st.session_state.auto_progress = False
if 'waiting_for_trade' not in st.session_state:
    st.session_state.waiting_for_trade = False
if 'trade_made' not in st.session_state:
    st.session_state.trade_made = False
if 'selected_ticker' not in st.session_state:
    st.session_state.selected_ticker = 'SAMPLE_SWINGS.csv'

def reset_all_portfolios():
    """Reset all portfolios with the current starting cash amount"""
    for i in range(1, st.session_state.num_players + 1):
        st.session_state.portfolios[i] = {
            'cash': st.session_state.starting_cash, 
            'positions': 0, 
            'pnl_calculator': PnLCalculator(), 
            'trading_history': []
        }

def render_full_price_preview(df, breakpoints):
    """
    Render full price chart preview with all breakpoints marked
    """
    fig = go.Figure()
    
    # Add price line
    fig.add_trace(go.Scatter(
        x=df['Date'],
        y=df['Price'],
        mode='lines',
        name='Price',
        line=dict(color='blue', width=2)
    ))
    
    # Add vertical lines for all breakpoints
    for bp in breakpoints:
        fig.add_shape(
            type="line",
            x0=df.iloc[bp]['Date'],
            x1=df.iloc[bp]['Date'],
            y0=df['Price'].min(),
            y1=df['Price'].max(),
            line=dict(
                color="red",
                width=2,
                dash="solid"
            )
        )
    
    # Add breakpoint markers
    if breakpoints:
        breakpoint_dates = df.loc[breakpoints, 'Date']
        breakpoint_prices = df.loc[breakpoints, 'Price']
        
        fig.add_trace(go.Scatter(
            x=breakpoint_dates,
            y=breakpoint_prices,
            mode='markers',
            name='Decision Points',
            marker=dict(
                color='red',
                size=8,
                symbol='diamond'
            )
        ))
    
    # Update layout
    fig.update_layout(
        title=f'Full Price Chart Preview - {st.session_state.selected_ticker}',
        xaxis_title='Date',
        yaxis_title='Price',
        showlegend=True,
        height=400,
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(211, 211, 211, 0.2)',
            gridwidth=1
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(211, 211, 211, 0.2)',
            gridwidth=1
        )
    )
    
    return fig

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
                i: {'cash': st.session_state.starting_cash, 'positions': 0, 'pnl_calculator': PnLCalculator(), 'trading_history': []}
                for i in range(1, st.session_state.num_players + 1)
            }
            st.session_state.auto_progress = False
            st.session_state.waiting_for_trade = False
            st.session_state.trade_made = False
            st.rerun()
    with header_col2:
        st.markdown("### Progress Control")
        col1, col2, col3 = st.columns(3)
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
        with col3:
            num_players = st.number_input("Number of Players", min_value=1, max_value=4, value=st.session_state.num_players)
            if num_players != st.session_state.num_players:
                st.session_state.num_players = num_players
                # Initialize new players or remove excess players
                new_portfolios = {}
                new_player_names = {}
                for i in range(1, num_players + 1):
                    if i in st.session_state.portfolios:
                        new_portfolios[i] = st.session_state.portfolios[i]
                        new_player_names[i] = st.session_state.player_names[i]
                    else:
                        new_portfolios[i] = {'cash': st.session_state.starting_cash, 'positions': 0, 'pnl_calculator': PnLCalculator(), 'trading_history': []}
                        new_player_names[i] = f"Player {i}"
                st.session_state.portfolios = new_portfolios
                st.session_state.player_names = new_player_names
                st.rerun()
    
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
        # Create a container for trading decisions
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
                                if st.session_state.current_day_index in breakpoints:
                                    st.session_state.waiting_for_trade = True
                                render_trading_interface(
                                    df.iloc[st.session_state.current_day_index]['Price'],
                                    st.session_state.portfolios[player_num],
                                    player_num,
                                    is_breakpoint=st.session_state.current_day_index in breakpoints
                                )

    # Stats tiles below the price chart
    st.markdown("### Portfolio Stats")
    # Create a horizontal layout for stats
    cols = st.columns(st.session_state.num_players)
    for player_num in range(1, st.session_state.num_players + 1):
        with cols[player_num - 1]:
            with st.container(border=True):
                # Add player name input
                player_name = st.text_input(
                    "Player Name",
                    value=st.session_state.player_names[player_num],
                    key=f"player_name_{player_num}"
                )
                if player_name != st.session_state.player_names[player_num]:
                    st.session_state.player_names[player_num] = player_name
                    st.rerun()
                
                st.markdown(f"#### {st.session_state.player_names[player_num]}")
                
                # Current position tile
                current_price = df.iloc[st.session_state.current_day_index]['Price']
                current_date = df.iloc[st.session_state.current_day_index]['Date']
                st.session_state.portfolios[player_num]['pnl_calculator'].update_portfolio_value(current_price, current_date)
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

                # Always show performance metrics
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
                        name=st.session_state.player_names[player_num],
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
            st.markdown(f"**{st.session_state.player_names[player_num]}**")
            for i, trade in enumerate(st.session_state.portfolios[player_num]['trading_history'], 1):
                st.write(f"Trade {i}: {trade['action'].upper()} {trade['quantity']} @ ${trade['price']:.2f}")

    # Auto progress logic
    if st.session_state.auto_progress and not st.session_state.waiting_for_trade:
        if st.session_state.current_day_index < len(df) - 1:
            sleep_interval = st.session_state.time_to_run_sec / len(df)
            time.sleep(sleep_interval)
            st.session_state.current_day_index += 1
            st.rerun()
        else:
            st.session_state.auto_progress = False
            st.warning("You've reached the end of the simulation!")

    # Admin Settings Section
    with st.expander("⚙️ Admin Settings", expanded=False):
        st.markdown("### Simulation Configuration")
        
        admin_col1, admin_col2, admin_col3 = st.columns(3)
        
        with admin_col1:
            # Starting cash setting
            new_starting_cash = st.number_input(
                "Starting Cash ($)",
                min_value=1000,
                max_value=1000000,
                value=st.session_state.starting_cash,
                step=1000,
                help="Set the starting cash amount for all players"
            )
            
            if new_starting_cash != st.session_state.starting_cash:
                st.session_state.starting_cash = new_starting_cash
                
            if st.button("Apply Starting Cash", help="Apply new starting cash to all players (resets portfolios)"):
                reset_all_portfolios()
                st.success(f"All portfolios reset with ${st.session_state.starting_cash:,.2f} starting cash")
                st.rerun()
        
        with admin_col2:
            # Time to run setting
            new_time_to_run = st.number_input(
                "Simulation Duration (seconds)",
                min_value=1,
                max_value=300,
                value=st.session_state.time_to_run_sec,
                step=1,
                help="Total time for the simulation to run from start to finish"
            )
            
            if new_time_to_run != st.session_state.time_to_run_sec:
                st.session_state.time_to_run_sec = new_time_to_run
                st.success(f"Simulation duration set to {st.session_state.time_to_run_sec} seconds")
        
        with admin_col3:
            # Reset simulation button
            st.markdown("### Quick Actions")
            if st.button("🔄 Reset Simulation", help="Reset simulation to beginning with current settings"):
                st.session_state.current_day_index = 0
                st.session_state.auto_progress = False
                st.session_state.waiting_for_trade = False
                st.session_state.trade_made = False
                reset_all_portfolios()
                st.success("Simulation reset to beginning")
                st.rerun()
        
        # Add price chart preview section
        st.markdown("---")
        st.markdown("### Price Chart Preview")
        st.markdown(f"**{len(breakpoints)} decision points** identified in the data")
        
        # Render the full price chart preview
        preview_fig = render_full_price_preview(df, breakpoints)
        st.plotly_chart(preview_fig, use_container_width=True)
        
        # Display current settings
        st.markdown("---")
        st.markdown("### Current Settings")
        settings_col1, settings_col2, settings_col3 = st.columns(3)
        with settings_col1:
            st.metric("Starting Cash", f"${st.session_state.starting_cash:,.2f}")
        with settings_col2:
            st.metric("Simulation Duration", f"{st.session_state.time_to_run_sec}s")
        with settings_col3:
            st.metric("Players", st.session_state.num_players)

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
