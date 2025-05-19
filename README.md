# Trading Decision Simulator

A Streamlit-based application that simulates trading decisions at predefined price breakpoints. Users can make buy/sell decisions without seeing future price movements, and track their performance over time.

## Features

- Progressive price chart that reveals only past price movements
- Trading decision interface at each breakpoint
- Real-time PnL calculation and visualization
- Performance metrics including total return, max drawdown, and Sharpe ratio
- Trading history tracking
- Portfolio value visualization

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
streamlit run app.py
```

## Data Format

The application expects CSV files with the following columns:
- `Date`: Date in YYYY-MM-DD format
- `Price`: Price value (float)
- `Breakpoint`: Boolean indicating if this is a trading decision point

A sample data file is provided in `data/sample_ticker.csv`.

## Usage

1. Upload a CSV file with ticker data using the file uploader
2. The application will automatically progress through price movements day by day
3. At each breakpoint, make your trading decision:
   - Buy: Purchase shares at the current price
   - Sell: Sell shares at the current price
   - Hold: Maintain current position
4. Track your performance using the metrics and charts
5. Review your trading history at any time

## Project Structure

```
trading_simulator/
├── app.py                     # Main Streamlit application
├── data/                      # Predefined ticker data
│   └── sample_ticker.csv      # Sample ticker data
├── utils/
│   ├── data_handler.py        # Data loading and processing
│   └── pnl_calculator.py      # PnL calculation logic
├── components/
│   ├── price_chart.py         # Progressive chart component
│   ├── trading_interface.py   # Buy/sell decision interface
│   └── performance_metrics.py # PnL and metrics display
└── requirements.txt           # Dependencies
```

## Contributing

Feel free to submit issues and enhancement requests! 