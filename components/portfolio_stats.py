import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from utils.visual_configs import PLAYER_COLORS
from utils.visual_configs import CURRENCY_INDICATOR

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
            yaxis_title='Value ({CURRENCY_INDICATOR})',
            showlegend=True,
            height=300,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # # Display trading history for all players
        # st.subheader("Trading History")
        # for player_num in range(1, st.session_state.num_players + 1):
        #     st.markdown(f"**{st.session_state.player_names[player_num]}**")
        #     for i, trade in enumerate(st.session_state.portfolios[player_num]['trading_history'], 1):
        #         st.write(f"Trade {i}: {trade['action'].upper()} {trade['quantity']} @ {CURRENCY_INDICATOR}{trade['price']:.2f}") 