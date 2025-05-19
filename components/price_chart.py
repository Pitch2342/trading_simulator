import streamlit as st
import plotly.graph_objects as go
from utils.data_handler import mask_future_data

def render_progressive_chart(df, current_day_index: int, breakpoints: list) -> None:
    """
    Render progressive price chart with masked future data.
    
    Args:
        df: DataFrame with price data
        current_day_index: Current day index
        breakpoints: List of breakpoint indices
    """
    # Create masked data for future prices
    masked_df = mask_future_data(df, current_day_index)
    
    # Create figure
    fig = go.Figure()
    
    # Add price line
    fig.add_trace(go.Scatter(
        x=df['Date'],
        y=masked_df['Price'],
        mode='lines',
        name='Price',
        line=dict(color='blue')
    ))
    
    # Add breakpoint markers
    breakpoint_dates = df.loc[breakpoints, 'Date']
    breakpoint_prices = df.loc[breakpoints, 'Price']
    
    fig.add_trace(go.Scatter(
        x=breakpoint_dates,
        y=breakpoint_prices,
        mode='markers',
        name='Breakpoints',
        marker=dict(
            color='red',
            size=10,
            symbol='diamond'
        )
    ))
    
    # Update layout
    fig.update_layout(
        title='Price Movement',
        xaxis_title='Date',
        yaxis_title='Price',
        showlegend=True,
        height=500
    )
    
    # Add vertical line for current day
    fig.add_vline(
        x=df.iloc[current_day_index]['Date'],
        line_dash="dash",
        line_color="gray"
    )
    
    # Display chart
    st.plotly_chart(fig, use_container_width=True) 