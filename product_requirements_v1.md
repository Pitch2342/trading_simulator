# Trading Decision Simulator PRD

## Overview
A real-time trading simulation platform that allows multiple players to make trading decisions at predefined price breakpoints. The system supports multiple tickers, real-time PnL tracking, and performance visualization.

## Core Features

### Multi-Player Support
- Support for 1-4 players simultaneously
- Individual portfolio tracking for each player
- Color-coded visualization for different players
- Independent trading decisions for each player

### Trading Interface
- Real-time price display
- Buy/Sell decision interface at breakpoints
- Position quantity input
- Current portfolio value display
- Cash balance tracking
- Real-time PnL calculation

### Visualization
- Progressive price chart showing historical data
- Portfolio value over time chart
- Performance metrics display
- Trading history log
- Color-coded player performance tracking

### Data Management
- Support for multiple ticker files
- CSV-based price data
- Breakpoint identification
- Historical data tracking

## Technical Requirements

### Data Format
- CSV files with columns:
  - Date
  - Price
  - Breakpoint indicator
- Files stored in `data/` directory
- Support for multiple ticker files

### Performance Metrics
- Total Return
- Maximum Drawdown
- Current PnL
- Portfolio Value
- Cash Balance
- Position Count

### User Interface
- Clean, modern Streamlit interface
- Responsive layout
- Real-time updates
- Clear player separation
- Intuitive trading controls

## Current Implementation Status

### Implemented Features
- Multi-player support (1-4 players)
- Real-time PnL tracking
- Progressive price chart
- Trading interface at breakpoints
- Performance metrics
- Multiple ticker support
- Portfolio value tracking
- Trading history logging

### Pending Features
- Save/Load game state
- Custom breakpoint definition
- Strategy comparison tools
- Export functionality
- Advanced analytics
- AI-assisted trading suggestions

## System Architecture

### Core Components
1. Main Application (`app.py`)
   - Game state management
   - Player management
   - UI layout
   - Progress control

2. Trading Interface (`components/trading_interface.py`)
   - Buy/Sell controls
   - Position management
   - Portfolio display

3. Price Chart (`components/price_chart.py`)
   - Progressive visualization
   - Breakpoint highlighting
   - Historical data display

4. PnL Calculator (`utils/pnl_calculator.py`)
   - Position value calculation
   - Performance metrics
   - Portfolio tracking

5. Data Handler (`utils/data_handler.py`)
   - CSV loading
   - Breakpoint extraction
   - Data validation

## Future Enhancements

### Short Term
1. Game state persistence
2. Custom breakpoint definition
3. Enhanced performance analytics
4. Export functionality

### Long Term
1. AI trading suggestions
2. Strategy comparison tools
3. Multi-timeframe support
4. Advanced risk metrics
5. Social features (leaderboards, sharing)

## Technical Dependencies
- Streamlit
- Plotly
- Pandas
- Python 3.x

## Performance Requirements
- Real-time updates
- Smooth chart rendering
- Responsive UI
- Efficient data handling
- Support for large datasets

## User Experience Goals
- Intuitive trading interface
- Clear performance visualization
- Easy player management
- Smooth game progression
- Informative metrics display 