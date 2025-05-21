from typing import Dict, List
import pandas as pd

class PnLCalculator:
    def __init__(self):
        self.initial_cash = 10000
        self.cash = self.initial_cash
        self.positions = 0
        self.trades: List[Dict] = []
        self.portfolio_values: List[float] = [self.initial_cash]
        self.current_price: float = 0.0
        
        # Initialize daily metrics DataFrame
        self.daily_metrics = pd.DataFrame(columns=[
            'date',
            'cash',
            'portfolio_value',
            'positions',
            'pnl',
            'return_pct',
            'drawdown_pct'
        ])
    
    def update_daily_metrics(self, date: pd.Timestamp) -> None:
        """
        Update daily metrics DataFrame with current portfolio state.
        
        Args:
            date: Current date for the metrics
        """
        portfolio_value = self.get_portfolio_value(self.current_price)
        pnl = self.get_current_pnl()
        return_pct = (portfolio_value / self.initial_cash - 1) * 100
        
        # Calculate drawdown
        if len(self.portfolio_values) > 0:
            peak = max(self.portfolio_values)
            drawdown_pct = ((peak - portfolio_value) / peak * 100) if peak > 0 else 0
        else:
            drawdown_pct = 0
            
        new_row = pd.DataFrame([{
            'date': date,
            'cash': self.cash,
            'portfolio_value': portfolio_value,
            'positions': self.positions,
            'pnl': pnl,
            'return_pct': return_pct,
            'drawdown_pct': drawdown_pct
        }])
        
        self.daily_metrics = pd.concat([self.daily_metrics, new_row], ignore_index=True)
    
    def update_portfolio_value(self, current_price: float, date: pd.Timestamp = None) -> None:
        """
        Update portfolio value with current price and daily metrics.
        
        Args:
            current_price: Current price per share
            date: Current date for metrics (defaults to current timestamp)
        """
        self.current_price = current_price
        current_value = self.get_portfolio_value(current_price)
        self.portfolio_values.append(current_value)
        
        if date is None:
            date = pd.Timestamp.now()
        self.update_daily_metrics(date)
    
    def execute_trade(self, action: str, quantity: int, price: float) -> None:
        """
        Execute a trade and update portfolio.
        
        Args:
            action: 'buy' or 'sell'
            quantity: Number of shares
            price: Price per share
        """
        if action == 'buy':
            cost = quantity * price
            if cost > self.cash:
                raise ValueError("Insufficient funds")
            self.cash -= cost
            self.positions += quantity
        elif action == 'sell':
            if quantity > self.positions:
                raise ValueError("Insufficient positions")
            self.cash += quantity * price
            self.positions -= quantity
        
        self.trades.append({
            'action': action,
            'quantity': quantity,
            'price': price,
            'timestamp': pd.Timestamp.now()
        })
    
    def get_current_pnl(self) -> float:
        """
        Calculate current PnL.
        
        Returns:
            float: Current profit/loss
        """
        return self.get_portfolio_value(self.current_price) - self.initial_cash
    
    def get_portfolio_value(self, current_price: float) -> float:
        """
        Calculate current portfolio value.
        
        Args:
            current_price: Current price per share
            
        Returns:
            float: Total portfolio value
        """
        return self.cash + (self.positions * current_price)
    
    def get_performance_metrics(self) -> Dict:
        """
        Calculate performance metrics.
        
        Returns:
            Dict: Dictionary containing performance metrics
        """
        if not self.portfolio_values or len(self.portfolio_values) < 2:
            return {
                'total_return': 0,
                'max_drawdown': 0,
                'sharpe_ratio': 0
            }
        
        returns = pd.Series(self.portfolio_values).pct_change().dropna()
        
        total_return = (self.portfolio_values[-1] / self.initial_cash - 1) * 100
        
        # Calculate max drawdown safely
        try:
            cumulative_max = pd.Series(self.portfolio_values).cummax()
            drawdowns = (cumulative_max - self.portfolio_values) / cumulative_max * 100
            max_drawdown = drawdowns.max()
        except (ZeroDivisionError, ValueError):
            max_drawdown = 0
        
        # Simple Sharpe ratio calculation (assuming risk-free rate of 0)
        try:
            sharpe_ratio = returns.mean() / returns.std() if len(returns) > 1 and returns.std() != 0 else 0
        except (ZeroDivisionError, ValueError):
            sharpe_ratio = 0
        
        return {
            'total_return': total_return,
            'max_drawdown': max_drawdown,
            'sharpe_ratio': sharpe_ratio
        }
