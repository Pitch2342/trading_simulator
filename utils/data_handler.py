import pandas as pd
from typing import List, Tuple, Union
import os

def load_data(file: Union[str, any]) -> pd.DataFrame:
    """
    Load and validate CSV data from file path or uploaded file.
    
    Args:
        file: File path (string) or uploaded file object
        
    Returns:
        pd.DataFrame: Processed DataFrame with validated data
    """
    try:
        # Handle both file paths and uploaded file objects
        if isinstance(file, str):
            # File path - existing functionality
            df = pd.read_csv(file)
        else:
            # Uploaded file object
            df = pd.read_csv(file)
        
        # Validate required columns
        required_columns = ['Date', 'Price', 'Breakpoint']
        if not all(col in df.columns for col in required_columns):
            raise ValueError("CSV must contain Date, Price, and Breakpoint columns")
        
        # Convert date column to datetime
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Sort by date
        df = df.sort_values('Date').reset_index(drop=True)
        
        # Validate price data
        if not df['Price'].dtype in ['float64', 'int64']:
            df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
        
        # Handle any NaN values in price
        if df['Price'].isna().any():
            raise ValueError("Price column contains invalid numeric values")
        
        # Validate breakpoint data
        df['Breakpoint'] = df['Breakpoint'].astype(bool)
        
        return df
    
    except Exception as e:
        raise ValueError(f"Error loading data: {str(e)}")

def extract_breakpoints(df: pd.DataFrame) -> List[int]:
    """
    Extract indices where breakpoints occur.
    
    Args:
        df: DataFrame with price data
        
    Returns:
        List[int]: List of indices where breakpoints occur
    """
    return df[df['Breakpoint']].index.tolist()

def mask_future_data(df: pd.DataFrame, current_day_index: int) -> pd.DataFrame:
    """
    Create a copy of DataFrame with future data masked.
    
    Args:
        df: Original DataFrame
        current_day_index: Current day index
        
    Returns:
        pd.DataFrame: DataFrame with future data masked
    """
    masked_df = df.copy()
    masked_df.loc[current_day_index + 1:, 'Price'] = None
    return masked_df
