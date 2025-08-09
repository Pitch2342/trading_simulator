import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from utils.visual_configs import PLAYER_COLORS
from utils.visual_configs import CURRENCY_INDICATOR, get_hoverlabel_config

def render_portfolio_stats(df, current_day_index):
    """Render portfolio statistics for all players"""
    st.markdown("### Portfolio Summary")

    # Add all styles in one block for player names
    st.markdown(
        f"""
        <style>
        {"".join([f".player-{i} {{ color: {PLAYER_COLORS[i]}; font-weight: bold; }}" for i in range(1, st.session_state.num_players + 1)])}
        </style>
        """,
        unsafe_allow_html=True
    )

    # Create a horizontal layout for stats
    cols = st.columns(st.session_state.num_players)
    
    for player_num in range(1, st.session_state.num_players + 1):
        with cols[player_num - 1]:
            with st.container(border=True):
                # Use HTML markdown to apply color and bold styling
                st.markdown(f'<div class="player-{player_num}">{st.session_state.player_names[player_num]}</div>', unsafe_allow_html=True)
                
                # Current position calculations
                current_price = df.iloc[current_day_index]['Price']
                current_date = df.iloc[current_day_index]['Date']
                portfolio = st.session_state.portfolios[player_num]
                pnl_calc = portfolio['pnl_calculator']
                
                pnl_calc.update_portfolio_value(current_price, current_date)
                portfolio_value = pnl_calc.get_portfolio_value(current_price)
                pnl = pnl_calc.get_current_pnl()
                metrics = pnl_calc.get_performance_metrics()
                
                # Calculate additional metrics
                cash_in_hand = portfolio['cash']
                equity_in_hand = portfolio['positions'] * current_price
                stock_qty = portfolio['positions']
                total_investment = pnl_calc.initial_cash
                total_returns_pct = metrics['total_return']
                drawdown = metrics['max_drawdown']
                sharpe = metrics['sharpe_ratio']
                
                # Create a 2-column table display
                metrics_data = {
                    'Metric': [
                        'Total Investment',
                        'Current Portfolio Value',
                        'PnL',
                        'Cash in Hand',
                        'Equity in Hand',
                        'Stock Qty',
                        'Total Returns %',
                        'Drawdown',
                        'Sharpe'
                    ],
                    'Value': [
                        f"{CURRENCY_INDICATOR}{total_investment:,.2f}",
                        f"{CURRENCY_INDICATOR}{portfolio_value:,.2f}",
                        f"{CURRENCY_INDICATOR}{pnl:,.2f}",
                        f"{CURRENCY_INDICATOR}{cash_in_hand:,.2f}",
                        f"{CURRENCY_INDICATOR}{equity_in_hand:,.2f}",
                        f"{stock_qty:,}",
                        f"{total_returns_pct:.2f}%",
                        f"{drawdown:.2f}%",
                        f"{sharpe:.3f}"
                    ]
                }
                hidden_metrics = ['Drawdown','Sharpe']
                metrics_df = pd.DataFrame(metrics_data)
                filtered_df = metrics_df[~metrics_df['Metric'].isin(hidden_metrics)]
                
                # Apply conditional styling for Total Returns % and Current Portfolio Value
                def color_returns(row):
                    if row['Metric'] == 'Total Returns %':
                        if total_returns_pct > 0:
                            return ['', 'color: green']
                        else:
                            return ['', 'color: red']
                    elif row['Metric'] == 'Current Portfolio Value':
                        if portfolio_value > total_investment:
                            return ['', 'color: green']
                        else:
                            return ['', 'color: red']
                    return ['', '']
                
                styled_df = filtered_df.style.apply(color_returns, axis=1)
                st.dataframe(styled_df, hide_index=True, use_container_width=True)

def render_performance_charts():
    """Render performance charts and trading history"""
    # Create portfolio value chart if any player has metrics
    fig = go.Figure()
    has_any_metrics = False

    for player_num in range(1, st.session_state.num_players + 1):
        daily_metrics = st.session_state.portfolios[player_num]['pnl_calculator'].daily_metrics
        if not daily_metrics.empty:
            fig.add_trace(go.Scatter(
                x=daily_metrics['date'],
                y=daily_metrics['portfolio_value'],
                mode='lines',
                name=st.session_state.player_names[player_num],
                line=dict(color=PLAYER_COLORS[player_num])
            ))
            has_any_metrics = True

    if has_any_metrics:
        fig.update_layout(
            title='Portfolio Values Over Time',
            xaxis_title='Date',
            yaxis_title=f'Value ({CURRENCY_INDICATOR})',
            showlegend=True,
            height=300,
            hovermode='x unified',
            hoverlabel=get_hoverlabel_config()
        )
        st.plotly_chart(fig, use_container_width=True)

    # Display trading history for all players in collapsible section (always visible)
    with st.expander("📊 Trading History", expanded=False):
        # Create a horizontal layout for trading history
        cols = st.columns(st.session_state.num_players)

        for player_num in range(1, st.session_state.num_players + 1):
            with cols[player_num - 1]:
                with st.container(border=True):
                    # Use HTML markdown to apply color and bold styling
                    st.markdown(f'<div class="player-{player_num}">{st.session_state.player_names[player_num]}</div>', unsafe_allow_html=True)

                    trading_history = st.session_state.portfolios[player_num]['trading_history']

                    if trading_history:
                        # Create trading history data
                        trade_data = []
                        for i, trade in enumerate(trading_history, 1):
                            # Format date if available, otherwise show trade number
                            date_str = trade.get('date', f"Trade {i}")
                            if hasattr(date_str, 'strftime'):
                                date_str = date_str.strftime('%m/%d/%Y')

                            trade_data.append({
                                'Date': date_str,
                                'Action': trade['action'].upper(),
                                'Qty': trade['quantity'],
                                'Price': f"{CURRENCY_INDICATOR}{trade['price']:.2f}"
                            })

                        # Display as a styled dataframe
                        trade_df = pd.DataFrame(trade_data)

                        # Apply conditional styling for buy/sell actions
                        def color_trades(row):
                            if row['Action'] == 'BUY':
                                return ['', 'color: green', '', '']
                            elif row['Action'] == 'SELL':
                                return ['', 'color: red', '', '']
                            else:  # HOLD
                                return ['', 'color: gray', '', '']

                        styled_trade_df = trade_df.style.apply(color_trades, axis=1)
                        st.dataframe(styled_trade_df, hide_index=True, use_container_width=True)
                    else:
                        st.write("No trades yet")