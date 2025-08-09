import streamlit as st
import plotly.graph_objects as go
from utils.data_handler import mask_future_data
from utils.visual_configs import CURRENCY_INDICATOR, get_hoverlabel_config

def build_progressive_figure(df, current_day_index: int, breakpoints: list) -> go.Figure:
    """
    Build the progressive price chart figure (without rendering) for a given index.

    Returns:
        go.Figure: Configured Plotly figure for current state
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
        height=600,
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(211, 211, 211, 0.2)',
            gridwidth=1
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(211, 211, 211, 0.2)',
            gridwidth=1
        ),
        hoverlabel=get_hoverlabel_config()
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

    return fig

def render_progressive_chart(df, current_day_index: int, breakpoints: list) -> None:
    """
    Render progressive price chart with masked future data and expanding window.
    """
    # Display current price in a prominent ticker
    current_price = df.iloc[current_day_index]['Price']
    st.markdown(
        f"""
        <div style='text-align: center; padding: 10px; margin-bottom: 5px;'>
            <h3 style='margin: 0; color: white; font-weight: 500;'>{CURRENCY_INDICATOR}{current_price:.2f}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Build figure and render
    fig = build_progressive_figure(df, current_day_index, breakpoints)
    st.plotly_chart(fig, use_container_width=True)

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
        ),
        hoverlabel=get_hoverlabel_config()
    )
    
    return fig 