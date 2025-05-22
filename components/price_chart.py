import streamlit as st
import plotly.graph_objects as go
from utils.data_handler import mask_future_data

def render_progressive_chart(df, current_day_index: int, breakpoints: list) -> None:
    """
    Render progressive price chart with masked future data and expanding window.
    
    Args:
        df: DataFrame with price data
        current_day_index: Current day index
        breakpoints: List of breakpoint indices
    """
    # Display current price in a prominent ticker
    current_price = df.iloc[current_day_index]['Price']
    st.markdown(
        f"""
        <div style='text-align: center; padding: 10px; margin-bottom: 5px;'>
            <h3 style='margin: 0; color: white; font-weight: 500;'>${current_price:.2f}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    
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
    
    # Only show breakpoints that have already occurred
    past_breakpoints = [bp for bp in breakpoints if bp <= current_day_index]
    if past_breakpoints:
        breakpoint_dates = df.loc[past_breakpoints, 'Date']
        breakpoint_prices = df.loc[past_breakpoints, 'Price']
        
        fig.add_trace(go.Scatter(
            x=breakpoint_dates,
            y=breakpoint_prices,
            mode='markers',
            name='Decision Points',
            marker=dict(
                color='red',
                size=10,
                symbol='diamond'
            )
        ))
    
    # Update layout with improved styling
    fig.update_layout(
        title='Price Movement',
        xaxis_title='Date',
        yaxis_title='Price',
        showlegend=True,
        height=500,
        # Add a subtle grid
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(211, 211, 211, 0.2)',  # lightgray with 20% opacity
            gridwidth=1
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(211, 211, 211, 0.2)',  # lightgray with 20% opacity
            gridwidth=1
        )
    )
    
    # Add vertical line for current day with improved styling
    current_date = df.iloc[current_day_index]['Date']
    fig.add_shape(
        type="line",
        x0=current_date,
        x1=current_date,
        y0=0,
        y1=1,
        yref="paper",
        line=dict(
            color="gray",
            width=2,
            dash="dash"
        )
    )
    
    # Add annotation for current day
    fig.add_annotation(
        x=current_date,
        y=1,
        yref="paper",
        text="Current Day",
        showarrow=False,
        yshift=10,
        xshift=10
    )
    
    # Display chart
    st.plotly_chart(fig, use_container_width=True) 