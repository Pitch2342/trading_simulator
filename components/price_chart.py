import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from utils.data_handler import mask_future_data
from utils.visual_configs import CURRENCY_INDICATOR, get_hoverlabel_config

def build_progressive_figure(df, current_day_index: int, breakpoints: list) -> go.Figure:
    """
    Build the progressive price chart figure (without rendering) for a given index.

    Returns:
        go.Figure: Configured Plotly figure for current state
    """
    # Create masked data for future prices and slice to reduce payload
    masked_df = mask_future_data(df, current_day_index)
    visible_df = masked_df.iloc[: current_day_index + 1]

    # Create figure
    fig = go.Figure()

    # Add price line (use WebGL for smoother rendering on large datasets)
    fig.add_trace(go.Scattergl(
        x=visible_df['Date'],
        y=visible_df['Price'],
        mode='lines',
        name='Price',
        line=dict(color='blue')
    ))

    # Only show breakpoints that have already occurred
    past_breakpoints = [bp for bp in breakpoints if bp <= current_day_index]
    if past_breakpoints:
        breakpoint_dates = df.loc[past_breakpoints, 'Date']
        breakpoint_prices = df.loc[past_breakpoints, 'Price']

        fig.add_trace(go.Scattergl(
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

    # Pre-compute fixed X range (entire dataset) to keep suspense
    x_min = df['Date'].min()
    x_max = df['Date'].max()
    x_range = x_max - x_min
    # 2.5% padding on both sides; fallback to 1 day if all dates equal
    x_pad = x_range * 0.025 if x_range.value != 0 else pd.Timedelta(days=1)
    # Compute dynamic Y range from visible data slice
    y_min_vis = float(visible_df['Price'].min())
    y_max_vis = float(visible_df['Price'].max())
    y_pad_vis = max(1e-9, (y_max_vis - y_min_vis) * 0.05)
    dynamic_y_range = [y_min_vis - y_pad_vis, y_max_vis + y_pad_vis]

    # Update layout with improved styling and stable UI between updates
    fig.update_layout(
        title='Price Movement',
        xaxis_title='Date',
        yaxis_title='Price',
        showlegend=True,
        height=600,
        uirevision='price_chart',  # keep UI state (zoom, pan) to avoid flicker
        transition={"duration": 0},  # disable plotly transitions
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(211, 211, 211, 0.2)',
            gridwidth=1,
            autorange=False,
            range=[x_min - x_pad, x_max + x_pad]
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(211, 211, 211, 0.2)',
            gridwidth=1,
            autorange=True
        ),
        hoverlabel=get_hoverlabel_config()
    )

    # Add a 'current day' vertical line as a trace to avoid layout shape churn
    current_date = df.iloc[current_day_index]['Date']
    fig.add_trace(
        go.Scattergl(
            x=[current_date, current_date],
            y=[dynamic_y_range[0], dynamic_y_range[1]],
            mode='lines',
            line=dict(color='gray', width=2, dash='dash'),
            hoverinfo='skip',
            name='Current Day',
            showlegend=False
        )
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