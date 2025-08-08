# Product Requirements Document (PRD)
# Trading Decision Simulator v2.0
# Complete Feature and Behavior Specification

## Table of Contents
1. [Executive Summary](#1-executive-summary)
2. [Product Architecture](#2-product-architecture)
3. [Core Features & Behaviors](#3-core-features--behaviors)
4. [User Interface Specifications](#4-user-interface-specifications)
5. [Data Management System](#5-data-management-system)
6. [Trading System](#6-trading-system)
7. [Portfolio Management](#7-portfolio-management)
8. [Performance Analytics](#8-performance-analytics)
9. [Admin Configuration System](#9-admin-configuration-system)
10. [State Management](#10-state-management)
11. [Visual Design System](#11-visual-design-system)
12. [Export & Reporting](#12-export--reporting)
13. [Technical Requirements](#13-technical-requirements)
14. [Detailed Behavioral Specifications](#14-detailed-behavioral-specifications)

---

## 1. Executive Summary

### 1.1 Product Overview
The Trading Decision Simulator is a web-based educational trading game that simulates stock market trading in a progressive, time-based manner. The application prevents future-looking bias by revealing price data day-by-day and allows multiple players (1-4) to compete by making trading decisions at predetermined breakpoints.

### 1.2 Core Concept
- **Progressive Price Revelation**: Price charts reveal data day-by-day, masking future prices
- **Breakpoint Trading**: Players can only execute trades at predefined decision points
- **Multi-Player Competition**: Support for 1-4 simultaneous players with individual portfolios
- **Real-time Analytics**: Live portfolio tracking, PnL calculation, and performance metrics

### 1.3 Key Differentiators
- **No Future Price Visibility**: Simulates real trading conditions by hiding future data
- **Forced Decision Points**: Breakpoint system creates consistent decision moments
- **Educational Focus**: Designed for learning trading psychology and decision-making
- **Flexible Data Input**: Support for custom scenarios via CSV upload

---

## 2. Product Architecture

### 2.1 Application Structure
```
Main Application (app.py)
├── Component Layer
│   ├── Admin Panel (admin_panel.py)
│   ├── CSV Uploader (csv_uploader.py)
│   ├── Portfolio Stats (portfolio_stats.py)
│   ├── Price Chart (price_chart.py)
│   └── Trading Interface (trading_interface.py)
└── Utility Layer
    ├── Data Handler (data_handler.py)
    ├── PnL Calculator (pnl_calculator.py)
    ├── Portfolio Manager (portfolio_manager.py)
    ├── Session Manager (session_manager.py)
    ├── Visual Configs (visual_configs.py)
    └── Visualization (visualization.py)
```

### 2.2 Data Flow Architecture
1. **Data Input**: CSV files (predefined or uploaded) → Data Handler
2. **State Management**: Session Manager maintains all game state
3. **Trading Flow**: Trading Interface → Portfolio Manager → PnL Calculator
4. **Visualization**: Price Chart + Portfolio Stats display current state
5. **Export**: Visualization utility generates summary images

### 2.3 Page Layout Structure
```
┌────────────────────────────────────────────────────────────┐
│  Trading Decision Simulator          [Start] [Stop]        │
├────────────────────────────────────────────────────────────┤
│                    Current Price: ₹XXX.XX                  │
│  ┌────────────────────────────────────────────────────┐   │
│  │              Progressive Price Chart                │   │
│  │  [Chart showing price movement up to current day]  │   │
│  └────────────────────────────────────────────────────┘   │
│                                                            │
│  Main Area (75%)                    Trading Grid (25%)    │
│  ┌─────────────────────┐  ┌─────────────┬─────────────┐  │
│  │                     │  │  Player 1   │  Player 2   │  │
│  │   Chart Area       │  ├─────────────┼─────────────┤  │
│  │                     │  │  Player 3   │  Player 4   │  │
│  └─────────────────────┘  └─────────────┴─────────────┘  │
│                                                            │
│  ┌────────────────────────────────────────────────────┐   │
│  │              Portfolio Summary                      │   │
│  │  [Player statistics in horizontal layout]          │   │
│  └────────────────────────────────────────────────────┘   │
│                                                            │
│  ┌────────────────────────────────────────────────────┐   │
│  │         Portfolio Values Over Time Chart           │   │
│  └────────────────────────────────────────────────────┘   │
│                                                            │
│  ┌────────────────────────────────────────────────────┐   │
│  │  📊 Trading History [Expandable]                   │   │
│  └────────────────────────────────────────────────────┘   │
│                                                            │
│  ┌────────────────────────────────────────────────────┐   │
│  │  ⚙️ Admin Settings [Expandable]                     │   │
│  └────────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────┘
```

---

## 3. Core Features & Behaviors

### 3.1 Progressive Price Display System

#### 3.1.1 Price Chart Behavior
- **Data Masking**: Future prices are set to `None` and not displayed
- **Day-by-Day Progression**: Chart updates to show one additional day at a time
- **Current Day Indicator**: Vertical dashed line marks the current trading day
- **Price Display**: Large centered display showing current price (₹XXX.XX format)

#### 3.1.2 Breakpoint System
- **Definition**: Specific days marked in data where trading is allowed
- **Visual Indicator**: Red diamond markers on past breakpoints
- **Trading Lock**: "Execute Trade" button disabled on non-breakpoint days
- **Auto-Pause**: Simulation automatically pauses at breakpoints

### 3.2 Multi-Player System

#### 3.2.1 Player Configuration
- **Player Count**: Configurable 1-4 players
- **Dynamic Grid**: 2x2 grid layout adjusts based on player count
- **Individual Portfolios**: Each player has separate cash, positions, and history
- **Custom Names**: Editable player names (default: "Player 1", "Player 2", etc.)

#### 3.2.2 Player Colors
- Player 1: Blue (#1f77b4)
- Player 2: Orange (#ff7f0e)
- Player 3: Purple (#9467bd)
- Player 4: Brown (#8c564b)

### 3.3 Simulation Control System

#### 3.3.1 Auto-Progress Feature
- **Start Button**: Initiates automatic progression through days
- **Stop Button**: Pauses automatic progression
- **Speed Control**: Total duration configurable (1-300 seconds)
- **Interval Calculation**: Sleep time = total_duration / number_of_days
- **Breakpoint Behavior**: Auto-progress pauses at breakpoints, resumes after trades

#### 3.3.2 Manual Controls
- **Day Navigation**: Progress only via Start button or after trades
- **Reset Simulation**: Returns to day 1 with fresh portfolios
- **End Detection**: Auto-stop and warning when reaching last day

---

## 4. User Interface Specifications

### 4.1 Trading Interface (Per Player)

#### 4.1.1 Layout Structure
```
┌─────────────────────────┐
│ [Player Name]           │  <- Color-coded player name
│ Action: [Dropdown]      │  <- Buy/Sell/Hold selector
│ Qty [Holding: X]        │  <- Quantity input with holdings display
│ Value: ₹XXX.XX          │  <- Trade value calculation
│ Cash: ₹XXX.XX           │  <- Available cash display
│ [Execute Trade]         │  <- Action button (enabled at breakpoints)
└─────────────────────────┘
```

#### 4.1.2 Interactive Elements
- **Action Dropdown**: Three options - Buy, Sell, Hold
- **Quantity Input**: 
  - Min: 0
  - Max (Buy): floor(cash / current_price)
  - Max (Sell): current positions held
  - Default: 1 (if max > 0), otherwise 0
  - Step: 1
- **Execute Trade Button**: 
  - Disabled state on non-breakpoint days
  - Success message on execution
  - Error message for invalid trades

### 4.2 Portfolio Statistics Display

#### 4.2.1 Metrics Table (Per Player)
| Metric | Description | Format |
|--------|-------------|---------|
| Total Investment | Initial starting cash | ₹X,XXX.XX |
| Current Portfolio Value | Cash + (Positions × Price) | ₹X,XXX.XX |
| PnL | Current Value - Initial Investment | ₹X,XXX.XX |
| Cash in Hand | Available cash | ₹X,XXX.XX |
| Equity in Hand | Positions × Current Price | ₹X,XXX.XX |
| Stock Qty | Number of shares held | X,XXX |
| Total Returns % | ((Current/Initial - 1) × 100) | ±XX.XX% |

#### 4.2.2 Visual Styling
- **Color Coding**: 
  - Green for positive returns/values above initial
  - Red for negative returns/values below initial
- **Number Formatting**: Comma separators, 2 decimal places for currency
- **Hidden Metrics**: Drawdown and Sharpe shown in calculations but not displayed

### 4.3 Performance Charts

#### 4.3.1 Portfolio Values Over Time
- **Chart Type**: Line chart with time series
- **Data Points**: Daily portfolio values for each player
- **Color Scheme**: Uses player-specific colors
- **Interaction**: Hover tooltips with exact values
- **Update Frequency**: Real-time as simulation progresses

#### 4.3.2 Trading History (Expandable Section)
- **Layout**: Horizontal columns, one per player
- **Data Display**: Table format with Date, Action, Qty, Price
- **Color Coding**: 
  - Green for BUY actions
  - Red for SELL actions
  - Gray for HOLD actions
- **Sorting**: Chronological order

---

## 5. Data Management System

### 5.1 Data Sources

#### 5.1.1 Predefined Tickers
- **Location**: `/data` directory
- **Available Files**: All .csv files in directory
- **Auto-Detection**: System scans directory and populates dropdown
- **Format**: Same as uploaded CSV requirements

#### 5.1.2 Custom CSV Upload
- **File Types**: .csv only
- **Size Limit**: Handled by Streamlit defaults
- **Validation**: Real-time format checking
- **Error Handling**: Specific error messages for each validation failure

### 5.2 CSV Data Format

#### 5.2.1 Required Structure
```csv
Date,Price,Breakpoint
2024-01-01,140.50,1
2024-01-02,142.75,0
2024-01-03,138.25,1
```

#### 5.2.2 Column Specifications
- **Date**: 
  - Format: YYYY-MM-DD
  - Type: Valid date string
  - Validation: Must parse to datetime
- **Price**: 
  - Type: Numeric (float or integer)
  - Validation: No null/NaN values allowed
  - Range: Any positive number
- **Breakpoint**: 
  - Type: Binary indicator
  - Valid Values: 0, 1, True, False
  - Purpose: Marks trading decision points

#### 5.2.3 Data Requirements
- **Minimum Rows**: 5
- **Sorting**: Automatically sorted by date ascending
- **Duplicates**: No date validation (assumes unique)

### 5.3 Data Processing

#### 5.3.1 Upload Flow
1. File selection via file uploader widget
2. CSV parsing and validation
3. Data type conversion and sorting
4. Success/error message display
5. Data preview (first 10 rows)
6. Summary statistics display

#### 5.3.2 Validation Messages
- "Missing required columns: [list]"
- "CSV file is empty"
- "Date column contains invalid date formats. Use YYYY-MM-DD format"
- "Price column contains non-numeric values"
- "Breakpoint column must contain only 0/1 or True/False values"
- "CSV must contain at least 5 rows of data"

---

## 6. Trading System

### 6.1 Trading Rules

#### 6.1.1 When Trading is Allowed
- **Breakpoint Days Only**: Trading disabled on non-breakpoint days
- **One Decision Per Breakpoint**: Cannot change decision once executed
- **All Players Must Trade**: Simulation pauses until all players act

#### 6.1.2 Trade Validation
- **Buy Orders**: 
  - Must have sufficient cash
  - Quantity × Price ≤ Available Cash
  - Error: "Insufficient funds"
- **Sell Orders**: 
  - Must have sufficient positions
  - Quantity ≤ Positions Held
  - Error: "Insufficient positions"
- **Hold Orders**: 
  - Always valid
  - Records as 0 quantity trade

### 6.2 Trade Execution

#### 6.2.1 Order Processing
1. Validate trade feasibility
2. Update cash balance
3. Update position count
4. Record in trading history
5. Update PnL calculator
6. Display success message
7. Trigger UI refresh

#### 6.2.2 Trading History Record
```python
{
    'action': 'buy'|'sell'|'hold',
    'price': current_price,
    'quantity': trade_quantity,
    'date': current_date
}
```

### 6.3 Portfolio Updates

#### 6.3.1 Buy Transaction
- Cash = Cash - (Quantity × Price)
- Positions = Positions + Quantity

#### 6.3.2 Sell Transaction
- Cash = Cash + (Quantity × Price)
- Positions = Positions - Quantity

#### 6.3.3 Hold Transaction
- No balance changes
- Record maintained for history

---

## 7. Portfolio Management

### 7.1 Portfolio Structure

#### 7.1.1 Portfolio Object
```python
{
    'cash': float,              # Current cash balance
    'positions': int,           # Number of shares held
    'pnl_calculator': object,   # PnL calculation instance
    'trading_history': list     # List of all trades
}
```

#### 7.1.2 Initial State
- Starting Cash: Configurable (₹1,000 - ₹1,000,000)
- Starting Positions: 0
- Trading History: Empty list

### 7.2 Portfolio Calculations

#### 7.2.1 Portfolio Value
- Formula: Cash + (Positions × Current Price)
- Updated: Every day progression and after trades

#### 7.2.2 Profit/Loss (PnL)
- Formula: Current Portfolio Value - Initial Cash
- Display: Can be positive or negative

#### 7.2.3 Returns Percentage
- Formula: ((Current Value / Initial Cash) - 1) × 100
- Display: With + or - sign

### 7.3 Portfolio State Management

#### 7.3.1 State Persistence
- Maintained in Streamlit session state
- Survives page interactions
- Reset only on explicit reset actions

#### 7.3.2 Multi-Player Handling
- Separate portfolio objects per player
- Simultaneous updates for all players
- Independent trading decisions

---

## 8. Performance Analytics

### 8.1 Real-time Metrics

#### 8.1.1 Daily Metrics Tracking
```python
{
    'date': timestamp,
    'cash': current_cash,
    'portfolio_value': total_value,
    'positions': share_count,
    'pnl': profit_loss,
    'return_pct': return_percentage,
    'drawdown_pct': drawdown_percentage
}
```

#### 8.1.2 Performance Indicators
- **Total Return**: Percentage gain/loss from initial
- **Maximum Drawdown**: Largest peak-to-trough decline
- **Sharpe Ratio**: Risk-adjusted return (risk-free rate = 0)

### 8.2 Analytics Visualization

#### 8.2.1 Portfolio Value Chart
- **Update Frequency**: After each day progression
- **Data Series**: One line per player
- **Features**: 
  - Unified hover mode
  - Color-coded by player
  - Automatic scale adjustment
  - Grid lines for readability

#### 8.2.2 Statistical Calculations
- **Returns**: Daily and cumulative
- **Volatility**: Standard deviation of returns
- **Risk Metrics**: Calculated but not all displayed

---

## 9. Admin Configuration System

### 9.1 Admin Panel Features

#### 9.1.1 Data Source Selection
- **Options**: 
  - Predefined Tickers (dropdown selection)
  - Upload Custom CSV
- **Behavior**: Switching sources resets simulation
- **Default**: Predefined with SAMPLE_SWINGS selected

#### 9.1.2 Simulation Parameters
- **Starting Cash**: 
  - Range: ₹1,000 - ₹1,000,000
  - Step: ₹1,000
  - Apply Button: Resets all portfolios
- **Number of Players**: 
  - Range: 1-4
  - Updates grid layout dynamically
  - Preserves existing player data
- **Simulation Duration**: 
  - Range: 1-300 seconds
  - Controls auto-progress speed
  - Real-time update without reset

#### 9.1.3 Player Configuration
- **Custom Names**: Text input per player
- **Reset Names**: Button to restore defaults
- **Dynamic Display**: Shows inputs for active players only

### 9.2 UI Customization

#### 9.2.1 Chart Settings
- **Hover Font Size**: 
  - Range: 8-24px
  - Default: 16px
  - Applies to all charts immediately

#### 9.2.2 Visual Preferences
- **Currency Symbol**: ₹ (Rupee symbol)
- **Number Formatting**: Comma separators
- **Color Scheme**: Fixed per player

### 9.3 Quick Actions

#### 9.3.1 Reset Options
- **Reset Simulation**: 
  - Returns to day 1
  - Clears all portfolios
  - Maintains settings
- **Reset Player Names**: 
  - Restores "Player X" format
  - Immediate update

#### 9.3.2 Data Preview
- **Toggle Control**: Show/hide full price chart
- **Preview Features**: 
  - Complete price history
  - All breakpoints marked
  - Read-only view

---

## 10. State Management

### 10.1 Session State Variables

#### 10.1.1 Core State
```python
{
    'current_day_index': int,           # Current position in data
    'num_players': int,                 # Active player count (1-4)
    'starting_cash': float,             # Initial cash per player
    'time_to_run_sec': int,            # Total simulation duration
    'portfolios': dict,                # Player portfolio objects
    'player_names': dict,              # Custom player names
    'auto_progress': bool,             # Auto-advance state
    'waiting_for_trade': bool,         # Breakpoint pause state
    'trade_made': bool,                # Trade completion flag
    'selected_ticker': str,            # Current ticker selection
    'uploaded_data': DataFrame,        # Custom uploaded data
    'data_source': str,                # 'predefined' or 'uploaded'
    'chart_hoverlabel_font_size': int # Chart font size setting
}
```

#### 10.1.2 State Initialization
- Occurs on first page load
- Sets all defaults
- Creates initial portfolios

### 10.2 State Transitions

#### 10.2.1 Day Progression
1. Increment current_day_index
2. Update all portfolio values
3. Check for breakpoint
4. Pause if breakpoint found
5. Continue if not

#### 10.2.2 Trade Execution
1. Set waiting_for_trade = True
2. Enable trading interfaces
3. Process trades
4. Set trade_made = True
5. Resume progression

---

## 11. Visual Design System

### 11.1 Color Palette

#### 11.1.1 Player Colors
- Player 1: #1f77b4 (Blue)
- Player 2: #ff7f0e (Orange)
- Player 3: #9467bd (Purple)
- Player 4: #8c564b (Brown)

#### 11.1.2 UI Colors
- Positive Values: Green
- Negative Values: Red
- Neutral/Hold: Gray
- Grid Lines: rgba(211, 211, 211, 0.2)

### 11.2 Typography

#### 11.2.1 Font Hierarchy
- Headers: Bold, larger size
- Price Display: Large, centered
- Metrics: Standard size with color coding
- Labels: Smaller, descriptive text

#### 11.2.2 Number Formatting
- Currency: ₹X,XXX.XX
- Percentages: ±XX.XX%
- Quantities: X,XXX

### 11.3 Layout Principles

#### 11.3.1 Responsive Design
- Container borders for separation
- Flexible column widths
- Automatic text sizing
- Mobile considerations

#### 11.3.2 Visual Hierarchy
1. Current price (most prominent)
2. Price chart (primary focus)
3. Trading controls (action area)
4. Portfolio stats (information)
5. Admin settings (collapsed by default)

---

## 12. Export & Reporting

### 12.1 Summary Image Generation

#### 12.1.1 Image Contents
- **Portfolio Statistics Table**: All players' metrics
- **Portfolio Value Chart**: Historical performance
- **Price Movement Chart**: Stock price with breakpoints
- **Trading Activity Summary**: Trade counts per player

#### 12.1.2 Image Specifications
- Format: PNG
- Resolution: 300 DPI
- Size: 24×12 inches
- Layout: 2×2 grid

### 12.2 Export Features

#### 12.2.1 File Naming
- Pattern: `trading_sim_YYYY-MM-DD-HH:MM:SS_[num_players].png`
- Example: `trading_sim_2024-01-15-14:30:45_4.png`

#### 12.2.2 Download Process
1. Click "Generate Portfolio Summary Image"
2. Processing with matplotlib backend
3. Base64 encoding
4. Download button appears
5. Click to save file

### 12.3 CSV Data Export

#### 12.3.1 Current Data Download
- Available in CSV uploader section
- Exports currently loaded data
- Maintains original format

#### 12.3.2 Sample Data Download
- Pre-formatted example CSV
- 15 rows with 6 breakpoints
- Demonstrates proper format

---

## 13. Technical Requirements

### 13.1 Performance Requirements

#### 13.1.1 Response Times
- Page Load: < 2 seconds
- Trade Execution: < 500ms feedback
- Chart Update: < 1 second
- Data Upload: < 3 seconds for 500 rows

#### 13.1.2 Scalability
- Players: 1-4 concurrent
- Data Size: 10-10000 trading days
- Session Memory: < 1 GB per session

### 13.2 Browser Compatibility

#### 13.2.1 Supported Browsers
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

#### 13.2.2 Display Requirements
- Minimum Resolution: 1280×720
- Recommended: 1920×1080
- Mobile: Responsive but not optimized

### 13.3 Error Handling

#### 13.3.1 Input Validation
- All numeric inputs bounded
- File type restrictions
- Data format validation
- Clear error messages

#### 13.3.2 Recovery Mechanisms
- Session state persistence
- Graceful error displays
- Reset options available
- No data loss on errors

---

## 14. Detailed Behavioral Specifications

### 14.1 Application Start Behavior

#### 14.1.1 Initial Load Sequence
1. Initialize session state with defaults
2. Set page configuration (title, icon, layout)
3. Load predefined ticker data (SAMPLE_SWINGS)
4. Extract breakpoints from data
5. Initialize single player with ₹10,000
6. Display day 1 with price chart
7. Show admin panel collapsed
8. Trading interface disabled (not a breakpoint)

#### 14.1.2 First Breakpoint Behavior
1. Auto-progress reaches breakpoint day
2. Simulation pauses automatically
3. Trading interfaces enable
4. "Execute Trade" buttons activate
5. Wait for all players to act
6. Resume after all trades complete

### 14.2 Data Source Switching

#### 14.2.1 Predefined to Upload
1. Clear current simulation state
2. Reset to day 1
3. Show upload interface
4. Expand admin panel
5. Display upload instructions
6. Hide main simulation area

#### 14.2.2 Upload to Predefined
1. Clear uploaded data
2. Load selected ticker
3. Reset portfolios
4. Start from day 1
5. Collapse admin panel
6. Enable simulation controls

### 14.3 Edge Cases & Special Behaviors

#### 14.3.1 End of Data
- Auto-progress stops
- Warning message displays
- All controls remain active
- Can still view history
- Export functions available

#### 14.3.2 Insufficient Funds/Positions
- Quantity auto-adjusts to maximum
- Error message on execution attempt
- Trade not recorded
- Player must adjust or hold

#### 14.3.3 Player Count Changes
- Existing players preserved
- New players initialized
- Grid layout adjusts
- Names maintain or default

### 14.4 CSS Customizations

#### 14.4.1 Metric Value Sizing
```css
div[data-testid="stMetricValue"] {
    font-size: clamp(1.2rem, 4vw, 2.5rem);
    white-space: nowrap;
    overflow: visible;
}
```

#### 14.4.2 Player Name Styling
```css
.player-[1-4] {
    color: [player-color];
    font-weight: bold;
}
```

#### 14.4.3 Radio Button Spacing
```css
div[data-testid="stRadio"] {
    margin-top: -18px;
    margin-bottom: 0px;
}
```

---

## Document Metadata

- **Version**: 2.0
- **Created**: 2024-12-19
- **Purpose**: Complete specification for development team handoff
- **Coverage**: 100% of current application features and behaviors
- **Validation**: Based on complete codebase analysis

## Implementation Notes

1. **Critical Features**:
   - Progressive price masking is essential
   - Breakpoint-only trading must be enforced
   - Multi-player synchronization required
   - State persistence across interactions

2. **UI/UX Priorities**:
   - Clear visual feedback for all actions
   - Intuitive player differentiation
   - Responsive performance charts
   - Accessible admin controls

3. **Data Integrity**:
   - Strict CSV validation
   - Proper error messaging
   - Graceful degradation
   - State recovery mechanisms

4. **Performance Considerations**:
   - Efficient chart rendering
   - Minimal state updates
   - Optimized calculations
   - Smooth auto-progression

---

**END OF DOCUMENT** 