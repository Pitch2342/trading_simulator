import streamlit as st
import plotly.graph_objects as go

# Player colors for consistent visualization
PLAYER_COLORS = {
    1: '#1f77b4',  # Blue
    2: '#ff7f0e',  # Orange
    3: '#2ca02c',  # Green
    4: '#d62728'   # Red
}

def render_portfolio_stats(df, current_day_index):
    """Render portfolio statistics for all players"""
    st.markdown("### Portfolio Stats")
    # Create a horizontal layout for stats
    cols = st.columns(st.session_state.num_players)
    
    for player_num in range(1, st.session_state.num_players + 1):
        with cols[player_num - 1]:
            with st.container(border=True):
                st.markdown(f"#### {st.session_state.player_names[player_num]}")
                
                # Current position tile
                current_price = df.iloc[current_day_index]['Price']
                current_date = df.iloc[current_day_index]['Date']
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