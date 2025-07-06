import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import pandas as pd
import numpy as np
from io import BytesIO
import base64
from utils.visual_configs import PLAYER_COLORS, CURRENCY_INDICATOR

def create_portfolio_summary_image(df, current_day_index, portfolios, player_names, num_players):
    """
    Create a combined image of portfolio stats and performance charts
    Returns a base64 encoded image string
    """
    # Create figure with subplots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(24, 12))
    fig.suptitle('Trading Simulation Summary', fontsize=16, fontweight='bold')
    
    # Portfolio Stats Table (top left)
    ax1.set_title('Portfolio Statistics', fontweight='bold', pad=20)
    ax1.axis('off')
    
    # Create portfolio stats table
    stats_data = []
    headers = [
        'Player',
        'Total\nInvestment',
        'Portfolio\nValue',
        'PnL',
        'Cash\nin Hand',
        'Equity\nin Hand',
        'Stock\nQty',
        'Returns\n%',
        'Drawdown',
        'Sharpe'
    ]
    
    for player_num in range(1, num_players + 1):
        current_price = df.iloc[current_day_index]['Price']
        portfolio = portfolios[player_num]
        pnl_calc = portfolio['pnl_calculator']
        
        pnl_calc.update_portfolio_value(current_price, df.iloc[current_day_index]['Date'])
        portfolio_value = pnl_calc.get_portfolio_value(current_price)
        pnl = pnl_calc.get_current_pnl()
        metrics = pnl_calc.get_performance_metrics()
        
        # Calculate all metrics
        cash_in_hand = portfolio['cash']
        equity_in_hand = portfolio['positions'] * current_price
        stock_qty = portfolio['positions']
        total_investment = pnl_calc.initial_cash
        total_returns_pct = metrics['total_return']
        drawdown = metrics['max_drawdown']
        sharpe = metrics['sharpe_ratio']
        
        stats_data.append([
            player_names[player_num],
            f"{CURRENCY_INDICATOR}{total_investment:,.0f}",
            f"{CURRENCY_INDICATOR}{portfolio_value:,.0f}",
            f"{CURRENCY_INDICATOR}{pnl:,.0f}",
            f"{CURRENCY_INDICATOR}{cash_in_hand:,.0f}",
            f"{CURRENCY_INDICATOR}{equity_in_hand:,.0f}",
            f"{stock_qty:,}",
            f"{total_returns_pct:.1f}%",
            f"{drawdown:.1f}%",
            f"{sharpe:.3f}"
        ])
    
    # Create table
    table = ax1.table(cellText=stats_data, colLabels=headers, 
                     cellLoc='center', loc='center',
                     bbox=[0, 0, 1, 1])
    
    # Style the table
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2)
    
    # Color header row
    for i in range(len(headers)):
        table[(0, i)].set_facecolor('#4CAF50')
        table[(0, i)].set_text_props(weight='bold', color='white')
    
    # Color player rows
    for i, player_num in enumerate(range(1, num_players + 1)):
        color = PLAYER_COLORS[player_num]
        for j in range(len(headers)):
            table[(i+1, j)].set_facecolor(color + '20')  # Add transparency
    
    # Performance Chart (top right)
    ax2.set_title('Portfolio Values Over Time', fontweight='bold', pad=20)
    
    for player_num in range(1, num_players + 1):
        if len(portfolios[player_num]['trading_history']) > 0:
            daily_metrics = portfolios[player_num]['pnl_calculator'].daily_metrics
            if not daily_metrics.empty:
                ax2.plot(daily_metrics['date'], daily_metrics['portfolio_value'], 
                        color=PLAYER_COLORS[player_num], 
                        label=player_names[player_num],
                        linewidth=2)
    
    ax2.set_xlabel('Date')
    ax2.set_ylabel(f'Value ({CURRENCY_INDICATOR})')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Rotate x-axis labels for better readability
    plt.setp(ax2.get_xticklabels(), rotation=45, ha='right')
    
    # Price Chart (bottom left)
    ax3.set_title('Stock Price Movement', fontweight='bold', pad=20)
    
    # Plot price data up to current day
    price_data = df.iloc[:current_day_index + 1]
    ax3.plot(price_data['Date'], price_data['Price'], 
            color='blue', linewidth=2, label='Stock Price')
    
    # Highlight breakpoints
    breakpoints = extract_breakpoints(df)
    for bp in breakpoints:
        if bp <= current_day_index:
            ax3.axvline(x=df.iloc[bp]['Date'], color='red', linestyle='--', alpha=0.7)
    
    ax3.set_xlabel('Date')
    ax3.set_ylabel(f'Price ({CURRENCY_INDICATOR})')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # Rotate x-axis labels
    plt.setp(ax3.get_xticklabels(), rotation=45, ha='right')
    
    # Trading Activity (bottom right)
    ax4.set_title('Trading Activity Summary', fontweight='bold', pad=20)
    ax4.axis('off')
    
    # Count trades per player
    trade_counts = []
    for player_num in range(1, num_players + 1):
        buy_count = sum(1 for trade in portfolios[player_num]['trading_history'] 
                       if trade['action'] == 'buy')
        sell_count = sum(1 for trade in portfolios[player_num]['trading_history'] 
                        if trade['action'] == 'sell')
        trade_counts.append([player_names[player_num], buy_count, sell_count])
    
    if trade_counts:
        trade_headers = ['Player', 'Buy Trades', 'Sell Trades']
        trade_table = ax4.table(cellText=trade_counts, colLabels=trade_headers,
                               cellLoc='center', loc='center',
                               bbox=[0, 0, 1, 1])
        
        trade_table.auto_set_font_size(False)
        trade_table.set_fontsize(10)
        trade_table.scale(1, 2)
        
        # Style trade table
        for i in range(len(trade_headers)):
            trade_table[(0, i)].set_facecolor('#2196F3')
            trade_table[(0, i)].set_text_props(weight='bold', color='white')
        
        for i, player_num in enumerate(range(1, num_players + 1)):
            color = PLAYER_COLORS[player_num]
            for j in range(len(trade_headers)):
                trade_table[(i+1, j)].set_facecolor(color + '20')
    
    # Adjust layout
    plt.tight_layout()
    
    # Convert to base64 string
    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    plt.close()
    
    return image_base64

# Import needed for extract_breakpoints
from utils.data_handler import extract_breakpoints
