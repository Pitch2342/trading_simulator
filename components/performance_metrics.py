import streamlit as st
import plotly.graph_objects as go
from typing import List, Dict

def render_performance_metrics(trading_history: List[Dict]) -> None:
    """
    Render performance metrics and charts.
    
    Args:
        trading_history: List of trading decisions
    """
    st.subheader("Performance Metrics")
    
    # Get metrics from PnL calculator
    metrics = st.session_state.pnl_calculator.get_performance_metrics()
    
    # Display key metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Total Return",
            f"{metrics['total_return']:.2f}%",
            delta=f"{metrics['total_return']:.2f}%"
        )
    
    with col2:
        st.metric(
            "Max Drawdown",
            f"{metrics['max_drawdown']:.2f}%"
        )
    
    with col3:
        st.metric(
            "Sharpe Ratio",
            f"{metrics['sharpe_ratio']:.2f}" if metrics['sharpe_ratio'] is not None else "0.00"
        )
    
    # Create portfolio value chart
    if len(trading_history) > 0:
        portfolio_values = st.session_state.pnl_calculator.portfolio_values
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            y=portfolio_values,
            mode='lines',
            name='Portfolio Value',
            line=dict(color='green')
        ))
        
        fig.update_layout(
            title='Portfolio Value Over Time',
            xaxis_title='Trading Day',
            yaxis_title='Value ($)',
            showlegend=True,
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Display trading history
        st.subheader("Trading History")
        for i, trade in enumerate(trading_history, 1):
            st.write(f"Trade {i}: {trade['action'].upper()} {trade['quantity']} @ ${trade['price']:.2f}")
