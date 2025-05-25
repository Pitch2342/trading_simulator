import streamlit as st
from typing import Dict

# Player colors for consistent visualization
PLAYER_COLORS = {
    1: '#1f77b4',  # Blue
    2: '#ff7f0e',  # Orange
    3: '#2ca02c',  # Green
    4: '#d62728'   # Red
}

def render_trading_interface(current_price: float, portfolio: Dict, player_num: int, is_breakpoint: bool = False) -> None:
    """
    Render trading interface for user decisions.
    
    Args:
        current_price: Current price per share
        portfolio: Current portfolio state
        player_num: Player number (1-4)
        is_breakpoint: Whether the current day is a breakpoint
    """
    # Add player color styling
    st.markdown(
        f"""
        <style>
        .player-{player_num} {{
            color: {PLAYER_COLORS[player_num]};
            font-weight: bold;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
    
    with st.container():
        # Player name and Action radio button should be close together
        st.markdown(f'<div class="player-{player_num}">{f"Player {player_num}"}</div>', unsafe_allow_html=True)
        # Custom CSS to reduce space above the radio button
        st.markdown(
            """
            <style>
            div[data-testid="stRadio"] { margin-top: -18px; margin-bottom: 0px; }
            </style>
            """,
            unsafe_allow_html=True
        )
        # Trading action selection
        action = st.radio(
            "Action",
            ["Buy", "Sell", "Hold"],
            horizontal=True,
            key=f"action_radio_{player_num}"
        )
        
        # Use a single row layout instead of columns
        max_quantity = int(portfolio['cash'] / current_price) if action == "Buy" else portfolio['positions']
        quantity = st.number_input(
            "Qty",
            min_value=0,
            max_value=max_quantity,
            value=0 if max_quantity == 0 else 1,
            step=1,
            key=f"quantity_input_{player_num}"
        )
        
        # Calculate and display trade impact
        trade_value = quantity * current_price
        st.metric(
            "Value",
            f"${trade_value:.2f}",
            f"Remaining: ${(portfolio['cash'] - trade_value):.2f}" if action == "Buy" else f"Positions: {portfolio['positions'] - quantity}"
        )
        
        # Execute trade button
        if st.button("Execute Trade", key=f"execute_trade_{player_num}", disabled=not is_breakpoint):
            if action == "Hold":
                st.success("Holding position")
                portfolio['trading_history'].append({
                    'action': 'hold',
                    'price': current_price,
                    'quantity': 0
                })
                st.session_state.trade_made = True
            else:
                try:
                    portfolio['pnl_calculator'].execute_trade(
                        action.lower(),
                        quantity,
                        current_price
                    )
                    # Update portfolio to match PnL calculator
                    portfolio['cash'] = portfolio['pnl_calculator'].cash
                    portfolio['positions'] = portfolio['pnl_calculator'].positions
                    st.success(f"{action} order executed successfully")
                    portfolio['trading_history'].append({
                        'action': action.lower(),
                        'price': current_price,
                        'quantity': quantity
                    })
                    st.session_state.trade_made = True
                except ValueError as e:
                    st.error(str(e))
            
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
