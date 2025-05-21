import streamlit as st
from typing import Dict

# Player colors for consistent visualization
PLAYER_COLORS = {
    1: '#1f77b4',  # Blue
    2: '#ff7f0e',  # Orange
    3: '#2ca02c',  # Green
    4: '#d62728'   # Red
}

def render_trading_interface(current_price: float, portfolio: Dict, player_num: int) -> None:
    """
    Render trading interface for user decisions.
    
    Args:
        current_price: Current price per share
        portfolio: Current portfolio state
        player_num: Player number (1-4)
    """
    # Add player color styling
    st.markdown(
        f"""
        <style>
        .player-{player_num} {{
            border-left: 4px solid {PLAYER_COLORS[player_num]};
            padding-left: 10px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
    
    with st.container():
        st.markdown(f'<div class="player-{player_num}">', unsafe_allow_html=True)
        st.write(f"Price: ${current_price:.2f}")
        
        # Trading action selection
        action = st.radio(
            "Action",
            ["Buy", "Sell", "Hold"],
            horizontal=True,
            key=f"action_radio_{player_num}"
        )
        
        # Create two columns for quantity and trade value
        qty_col, value_col = st.columns(2)
        
        # Quantity input for buy/sell
        if action != "Hold":
            with qty_col:
                max_quantity = int(portfolio['cash'] / current_price) if action == "Buy" else portfolio['positions']
                quantity = st.number_input(
                    "Qty",
                    min_value=0,
                    max_value=max_quantity,
                    value=0,
                    step=1,
                    key=f"quantity_input_{player_num}"
                )
            
            with value_col:
                # Calculate and display trade impact
                trade_value = quantity * current_price
                st.metric(
                    "Value",
                    f"${trade_value:.2f}",
                    f"Remaining: ${(portfolio['cash'] - trade_value):.2f}" if action == "Buy" else f"Positions: {portfolio['positions'] - quantity}"
                )
        
        # Execute trade button
        if st.button("Execute Trade", key=f"execute_trade_{player_num}"):
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
            
            st.experimental_rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
