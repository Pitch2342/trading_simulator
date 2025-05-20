import streamlit as st
from typing import Dict

def render_trading_interface(current_price: float, portfolio: Dict) -> None:
    """
    Render trading interface for user decisions.
    
    Args:
        current_price: Current price per share
        portfolio: Current portfolio state
    """
    st.write(f"Price: ${current_price:.2f}")
    
    # Trading action selection
    action = st.radio(
        "Action",
        ["Buy", "Sell", "Hold"],
        horizontal=True
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
                step=1
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
    if st.button("Execute Trade"):
        if action == "Hold":
            st.success("Holding position")
            st.session_state.trading_history.append({
                'action': 'hold',
                'price': current_price,
                'quantity': 0
            })
            st.session_state.trade_made = True
        else:
            try:
                st.session_state.pnl_calculator.execute_trade(
                    action.lower(),
                    quantity,
                    current_price
                )
                # Update session state portfolio to match PnL calculator
                st.session_state.portfolio['cash'] = st.session_state.pnl_calculator.cash
                st.session_state.portfolio['positions'] = st.session_state.pnl_calculator.positions
                st.success(f"{action} order executed successfully")
                st.session_state.trading_history.append({
                    'action': action.lower(),
                    'price': current_price,
                    'quantity': quantity
                })
                st.session_state.trade_made = True
            except ValueError as e:
                st.error(str(e))
        
        st.experimental_rerun()
