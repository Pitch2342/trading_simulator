# Trading Simulator Data Format

This directory contains CSV files with predefined ticker data for the Trading Decision Simulator.

## Available Tickers
The following tickers are available for trading:
- `SAMPLE_SWINGS.csv`: Sample ticker for testing

## File Format
Each CSV file follows this format:
- Filename: `{TICKER_SYMBOL}.csv` (e.g., `AAPL.csv`, `GOOGL.csv`)
- Columns:
  - `Date`: Trading date in YYYY-MM-DD format
  - `Price`: Closing price for the day (float)
  - `Breakpoint`: Boolean (1/0) indicating if this is a decision point

## Data Structure
Each ticker file contains:
- 15 days of price data
- 5 breakpoints (days where trading decisions can be made)
- Realistic price movements

## Adding New Tickers
To add a new ticker:
1. Create a new CSV file named `{TICKER_SYMBOL}.csv`
2. Follow the format described above
3. Ensure dates are in chronological order
4. Include at least one breakpoint
5. Place the file in this directory

The simulator will automatically detect and make available any new ticker files added to this directory. 