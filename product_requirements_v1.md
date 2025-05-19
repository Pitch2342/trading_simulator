# Trading Decision Simulator PRD

## Overview
This Trading Decision Simulator allows users to make buy/sell decisions at predefined price breakpoints without seeing future price movements. The system uses a predefined ticker (AAPL) and calculates profit/loss (PnL) based on these decisions and visualizes the results in a progressive chart that reveals price movements day by day.

## User Experience

### Core Flow
1. System loads the predefined AAPL ticker data
2. System presents the initial price point
3. System automatically progresses through price movements day by day
4. System pauses at each breakpoint for user trading decisions (buy/sell/hold + quantity)
5. System continues automatic progression after each decision
6. System calculates and displays running PnL
7. At completion, system shows final performance metrics and full price chart

### Key Features
- Progressive price chart that reveals only past price movements
- Trading decision interface at each breakpoint
- Real-time PnL calculation and visualization
- Performance summary at the end of the simulation
- Persistent display box showing current position and running PnL throughout the simulation
- Automatic day-by-day price progression with pauses at breakpoints for trading decisions

## Technical Specifications

### Data Requirements
- **Data Folder**: Contains predefined CSV files with ticker data
  - Currently using AAPL.csv as the default ticker
  - Files are named with the ticker symbol (e.g., `AAPL.csv`, `GOOGL.csv`)
- **Price Data CSV Format**: 
  - Date (YYYY-MM-DD)
  - Price (Float)
  - Breakpoint (Boolean or 1/0)
- **Breakpoint Definition**: Special price points where user makes trading decisions

### System Architecture

#### File Structure
```
trading_simulator/
├── app.py                     # Main Streamlit application
├── data/                      # Predefined ticker data
│   ├── sample_ticker.csv      # Sample ticker data
│   └── README.md             # Documentation for data format
├── utils/
│   ├── __init__.py
│   ├── data_handler.py        # Data loading and processing
│   ├── visualization.py       # Chart generation
│   └── pnl_calculator.py      # PnL calculation logic
├── components/
│   ├── __init__.py
│   ├── price_chart.py         # Progressive chart component
│   ├── trading_interface.py   # Buy/sell decision interface
│   └── performance_metrics.py # PnL and metrics display
├── pages/
│   ├── __init__.py
│   ├── home.py                # Landing page
│   ├── simulation.py          # Main simulation page
│   └── results.py             # Final results page
└── requirements.txt           # Dependencies
```

#### Technology Stack
- **Framework**: Streamlit for rapid UI development
- **Data Processing**: Pandas for CSV handling
- **Visualization**: Plotly for interactive charts
- **State Management**: Streamlit session state

## Detailed Implementation

### Data Handler Module
- Load and validate CSV data
- Extract breakpoints
- Prepare data for progressive display
- Store simulation state

### Visualization Module
- Create progressive price chart with masked future data
- Highlight breakpoints on the chart
- Generate PnL visualization
- Provide portfolio value chart

### Trading Interface Component
- Display current price and historical context
- Accept buy/sell decisions with quantity input
- Show current portfolio status (cash, positions)
- Display running PnL
- Persistent position and PnL summary box that updates in real-time

### PnL Calculator Module
- Calculate position values based on user decisions
- Track cash balance
- Compute realized and unrealized gains/losses
- Calculate performance metrics (return %, drawdown, etc.)

## Implementation Steps

### Phase 1: Core Functionality
1. Set up basic Streamlit app structure
2. Implement data loading and validation
3. Create progressive chart with hidden future data
4. Build basic trading interface for breakpoints
5. Implement PnL calculation logic

### Phase 2: Enhanced Features
1. Add performance metrics and analytics
2. Improve visualization with portfolio value chart
3. Implement position tracking and management
4. Add flexible breakpoint definitions

### Phase 3: Polish and Optimization
1. Improve UI/UX with clearer instructions
2. Add error handling and data validation
3. Optimize performance for larger datasets
4. Implement save/load functionality for sessions

## API and Component Interfaces

### Data Handler
```python
def load_data(csv_file):
    # Returns DataFrame with validated price data

def extract_breakpoints(df):
    # Returns list of dates/indices where breakpoints occur

def mask_future_data(df, current_day_index):
    # Returns DataFrame with data past current_day_index masked
```

### Trading Interface
```python
def render_trading_interface(price, portfolio, cash_balance):
    # Renders trading decision interface
    # Returns action (buy/sell/hold) and quantity

def update_portfolio(portfolio, action, quantity, price):
    # Updates portfolio based on trading decision
    # Returns updated portfolio
```

### Visualization
```python
def render_progressive_chart(df, current_day_index, breakpoints):
    # Renders chart showing data up to current_day_index
    # Highlights breakpoints

def render_pnl_chart(portfolio_history):
    # Renders PnL chart based on portfolio history
```

## Performance Considerations
- Use efficient data structures for large datasets
- Implement lazy loading for long time series
- Cache chart generation to improve responsiveness
- Optimize state management for smooth progression

## Future Enhancements
- Multiple ticker support
- Custom breakpoint definition interface
- Strategy comparison mode
- AI-assisted trading suggestions
- Export of simulation results and decisions
- Replay mode for reviewing decisions

## Testing Plan
- Test with various CSV formats and sizes
- Verify PnL calculations with known examples
- Test edge cases (zero quantity, all buys, all sells)
- Validate performance with large datasets

This PRD outlines the complete system for a Trading Decision Simulator that allows users to make trading decisions at predefined breakpoints and see their performance over time. The Streamlit implementation provides a balance of rapid development and interactive capabilities needed for such a simulation tool.