# Product Requirements Document (PRD)
# Trading Decision Simulator v1.0

## 1. Executive Summary

### 1.1 Product Overview
The Trading Decision Simulator is a web-based educational and competitive trading game built with Python and Streamlit. It simulates progressive stock price movements where multiple players make trading decisions at predefined breakpoints without seeing future price movements. The application emphasizes decision-making under uncertainty and tracks performance metrics to create an engaging competitive environment.

### 1.2 Target Audience
- **Primary**: Trading education enthusiasts, financial literacy educators, investment clubs
- **Secondary**: Corporate training teams, business school instructors, competition organizers
- **Use Cases**: Educational workshops, team building exercises, trading skill assessment

### 1.3 Core Value Proposition
- **Progressive Revelation**: Charts reveal price movements day-by-day, preventing future-looking bias
- **Multi-Player Competition**: Support for up to 4 simultaneous players with real-time performance tracking
- **Flexible Data Input**: Support for both predefined sample data and custom CSV uploads
- **Comprehensive Analytics**: Real-time PnL calculation, performance metrics, and trading history

## 2. Current Product State

### 2.1 Technology Stack
- **Frontend**: Streamlit 1.32.0 (Python web framework)
- **Data Processing**: Pandas 2.2.1, NumPy 1.26.4
- **Visualization**: Plotly 5.19.0
- **Runtime**: Python 3.13
- **Architecture**: Single-page application with modular component design

### 2.2 Core Features Implemented

#### 2.2.1 Data Management
- **Predefined Tickers**: CSV-based sample data with 15-day periods and 5-6 breakpoints
- **Custom Data Upload**: CSV file upload with validation and format checking
- **Data Format**: Date, Price, Breakpoint columns with specific validation rules
- **Sample Data**: SAMPLE_SWINGS.csv and SAMPLE_UPS.csv demonstrating different market patterns

#### 2.2.2 Game Mechanics
- **Progressive Chart Display**: Price chart reveals historical data up to current day only
- **Breakpoint System**: Trading decisions only allowed at predefined breakpoints (marked in data)
- **Player Management**: 1-4 players with customizable names and individual portfolios
- **Trading Actions**: Buy, Sell, Hold with quantity selection and validation
- **Cash Management**: Starting cash configuration ($1,000 - $1,000,000) with insufficient funds protection

#### 2.2.3 Portfolio Management
- **Individual Portfolios**: Separate cash, positions, and trading history per player
- **Real-time PnL Calculation**: Continuous portfolio value updates based on current price
- **Performance Metrics**: Total return, maximum drawdown, Sharpe ratio calculations
- **Trading History**: Complete record of all trades with timestamps and execution details

#### 2.2.4 User Interface
- **Admin Panel**: Comprehensive configuration interface for simulation parameters
- **2x2 Player Grid**: Visual trading interface for up to 4 players simultaneously
- **Progress Controls**: Start/Stop automation with configurable simulation duration (1-300 seconds)
- **Real-time Metrics**: Live portfolio statistics and performance visualization
- **Responsive Design**: Optimized for different screen sizes with custom CSS styling

#### 2.2.5 Automation Features
- **Auto-progression**: Automatic time-based progression through price data
- **Breakpoint Pausing**: Automatic pause at trading decision points
- **Configurable Speed**: Simulation duration controls overall progression speed
- **Manual Override**: Manual start/stop controls for instructor-led sessions

### 2.3 Data Architecture

#### 2.3.1 Session State Management
```python
# Core session variables
- current_day_index: Current position in price data
- portfolios: Dict of player portfolios with PnL calculators
- player_names: Customizable player identifiers
- auto_progress: Automation state control
- waiting_for_trade: Breakpoint pause state
- data_source: 'predefined' or 'uploaded'
- uploaded_data: Custom CSV data storage
```

#### 2.3.2 Portfolio Structure
```python
# Per-player portfolio object
{
    'cash': float,
    'positions': int,
    'pnl_calculator': PnLCalculator instance,
    'trading_history': List[Dict]
}
```

#### 2.3.3 Trading Data Format
```csv
Date,Price,Breakpoint
2024-01-01,140,1
2024-01-02,150,0
2024-01-03,130,1
```

## 3. Functional Requirements

### 3.1 Data Management Requirements
- **REQ-DM-001**: System shall support CSV upload with Date, Price, Breakpoint columns
- **REQ-DM-002**: System shall validate uploaded data format and provide error messages
- **REQ-DM-003**: System shall provide downloadable sample CSV templates
- **REQ-DM-004**: System shall support predefined ticker data stored in /data directory
- **REQ-DM-005**: System shall auto-detect available ticker files and populate selection dropdown

### 3.2 Game Flow Requirements
- **REQ-GF-001**: System shall progress through price data day-by-day in chronological order
- **REQ-GF-002**: System shall pause automatically at breakpoints for trading decisions
- **REQ-GF-003**: System shall prevent trading actions on non-breakpoint days
- **REQ-GF-004**: System shall validate trade feasibility (sufficient cash/positions)
- **REQ-GF-005**: System shall support manual and automated progression modes

### 3.3 Multi-Player Requirements
- **REQ-MP-001**: System shall support 1-4 simultaneous players
- **REQ-MP-002**: System shall maintain separate portfolios for each player
- **REQ-MP-003**: System shall allow customizable player names
- **REQ-MP-004**: System shall display all players in a 2x2 grid interface
- **REQ-MP-005**: System shall update all portfolios simultaneously with price changes

### 3.4 Trading Requirements
- **REQ-TR-001**: System shall support Buy, Sell, Hold actions
- **REQ-TR-002**: System shall validate quantity against available cash/positions
- **REQ-TR-003**: System shall update portfolio state immediately after trade execution
- **REQ-TR-004**: System shall record complete trading history with timestamps
- **REQ-TR-005**: System shall calculate trade impact before execution

### 3.5 Analytics Requirements
- **REQ-AN-001**: System shall calculate real-time portfolio values
- **REQ-AN-002**: System shall compute total return percentage
- **REQ-AN-003**: System shall track maximum drawdown
- **REQ-AN-004**: System shall calculate Sharpe ratio (risk-free rate = 0)
- **REQ-AN-005**: System shall maintain daily metrics history

## 4. Non-Functional Requirements

### 4.1 Performance Requirements
- **REQ-PF-001**: System shall support real-time updates for 4 concurrent players
- **REQ-PF-002**: Chart rendering shall complete within 2 seconds for datasets up to 500 days
- **REQ-PF-003**: Trade execution shall provide immediate feedback (< 500ms)
- **REQ-PF-004**: Auto-progression shall maintain consistent timing intervals

### 4.2 Usability Requirements
- **REQ-US-001**: Interface shall be operable without training for basic trading functions
- **REQ-US-002**: Admin panel shall provide clear configuration options with help text
- **REQ-US-003**: Error messages shall be specific and actionable
- **REQ-US-004**: System shall provide visual feedback for all user actions

### 4.3 Reliability Requirements
- **REQ-RL-001**: System shall handle file upload errors gracefully
- **REQ-RL-002**: System shall maintain session state across page interactions
- **REQ-RL-003**: System shall prevent data loss during simulation resets
- **REQ-RL-004**: System shall validate all numerical inputs and provide bounds checking

## 5. User Interface Design

### 5.1 Layout Structure
```
┌─────────────────────────────────────────┬──────────────┐
│ Trading Decision Simulator              │ Start | Stop │
├─────────────────────────────────────────┴──────────────┤
│                                                        │
│ ┌─────────────────────────────────────────────────────┐│
│ │           Progressive Price Chart                   ││
│ │  ████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  ││
│ │                                                     ││
│ └─────────────────────────────────────────────────────┘│
│                                                        │
│ ┌──────────────────┬──────────────────┐ ┌──────────────┐│
│ │ Player 1         │ Player 2         │ │ Player 3     ││
│ │ Action: [Buy▼]   │ Action: [Sell▼]  │ │ Action: [▼]  ││
│ │ Qty: [100]       │ Qty: [50]        │ │ Qty: [0]     ││
│ │ Value: $1,000    │ Value: $500      │ │ Value: $0    ││
│ │ [Execute Trade]  │ [Execute Trade]  │ │ [Execute]    ││
│ └──────────────────┴──────────────────┘ └──────────────┘│
│                                                        │
│ ┌─────────────────────────────────────────────────────┐│
│ │              Portfolio Statistics                   ││
│ │ Player 1: $12,500 (+25%) | Player 2: $9,800 (-2%)  ││
│ └─────────────────────────────────────────────────────┘│
│                                                        │
│ ┌─────────────────────────────────────────────────────┐│
│ │               ⚙️ Admin Settings                      ││
│ │ [Data Source] [Starting Cash] [Players] [Duration]  ││
│ └─────────────────────────────────────────────────────┘│
└────────────────────────────────────────────────────────┘
```

### 5.2 Component Specifications

#### 5.2.1 Progressive Price Chart
- **Chart Type**: Plotly line chart with time series data
- **Visibility**: Shows historical data up to current day only
- **Breakpoints**: Highlighted markers for trading decision points
- **Styling**: Color-coded for different market patterns
- **Interactivity**: Hover tooltips showing exact price values

#### 5.2.2 Trading Interface Grid
- **Layout**: 2x2 grid for up to 4 players
- **Player Cards**: Individual trading controls per player
- **Color Coding**: Distinct colors per player for visual separation
- **Real-time Updates**: Immediate portfolio value updates
- **Validation**: Live feedback on trade feasibility

#### 5.2.3 Admin Panel
- **Expandable**: Collapsible interface to save screen space
- **Configuration Sections**: Data source, simulation parameters, player settings
- **Quick Actions**: Reset buttons and validation controls
- **Preview Mode**: Optional full chart preview for instructors

## 6. Data Requirements

### 6.1 Input Data Specifications
- **File Format**: CSV with UTF-8 encoding
- **Required Columns**: Date (YYYY-MM-DD), Price (float), Breakpoint (0/1)
- **Data Volume**: Optimized for 15-500 trading days
- **Breakpoint Density**: Recommended 5-10 decision points per dataset
- **Price Patterns**: Support for trending, volatile, and stable market conditions

### 6.2 Session Data Management
- **State Persistence**: Maintain portfolios and progress across page interactions
- **Memory Usage**: Efficient storage for multi-player session data
- **Data Validation**: Input sanitization and type checking
- **Error Recovery**: Graceful handling of malformed data

## 7. Integration Requirements

### 7.1 File System Integration
- **Data Directory**: Read access to /data folder for predefined tickers
- **Upload Processing**: Temporary file handling for CSV uploads
- **Sample Downloads**: Serve sample CSV files to users

### 7.2 External Dependencies
- **Streamlit Framework**: Web application framework
- **Pandas/NumPy**: Data processing and numerical computations
- **Plotly**: Interactive chart generation
- **Python Standard Library**: File I/O and data validation

## 8. Security Considerations

### 8.1 Data Security
- **File Upload Validation**: Restrict file types and size limits
- **Input Sanitization**: Prevent malicious data injection
- **Session Isolation**: Ensure user session data privacy

### 8.2 Application Security
- **No Authentication**: Current design for local/trusted environments
- **Data Persistence**: No permanent data storage (session-only)
- **File Access**: Restricted to designated data directories

## 9. Deployment Requirements

### 9.1 Local Deployment
- **Python Environment**: Python 3.13+ with pip package management
- **Dependencies**: Install via requirements.txt
- **Launch Command**: `streamlit run app.py`
- **Port Configuration**: Default Streamlit port 8501

### 9.2 Hosting Considerations
- **Streamlit Cloud**: Compatible with Streamlit sharing platform
- **Docker**: Containerization support available
- **Resource Requirements**: Minimal CPU/memory for up to 4 concurrent players

## 10. Success Metrics

### 10.1 Functional Metrics
- **Trade Execution Success Rate**: >99% successful trade executions
- **Data Upload Success Rate**: >95% valid CSV file processing
- **Session Stability**: Zero data loss during normal operation
- **Multi-player Synchronization**: All players see identical price progression

### 10.2 User Experience Metrics
- **Interface Responsiveness**: <2 second page load times
- **Trading Decision Time**: Support for quick decision-making workflows
- **Error Recovery**: Clear error messages and recovery paths
- **Learning Curve**: Usable without training for basic functions

## 11. Future Enhancement Opportunities

### 11.1 Potential Features
- **Advanced Charting**: Technical indicators, volume data, candlestick charts
- **Enhanced Analytics**: Risk metrics, sector performance, benchmark comparison
- **Multiplayer Enhancements**: Team mode, tournaments, leaderboards
- **Data Sources**: Real-time market data integration, multiple asset classes
- **Educational Tools**: Tutorials, strategy guides, performance analysis

### 11.2 Technical Improvements
- **Database Integration**: Persistent storage for historical results
- **User Authentication**: User accounts and progress tracking
- **Mobile Optimization**: Responsive design for tablet/phone usage
- **API Development**: RESTful API for external integrations
- **Performance Optimization**: Handling larger datasets and more concurrent users

---

## Document Information
- **Version**: 1.0
- **Last Updated**: 2024-12-19
- **Document Type**: Product Requirements Document
- **Status**: Current Implementation Analysis
- **Next Review**: Upon feature completion or major changes
