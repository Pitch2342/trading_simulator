import pandas as pd
from typing import List, Tuple

def load_data(file) -> pd.DataFrame:
    """
    Load and validate CSV data from uploaded file.
    
    Args:
        file: Uploaded CSV file object
        
    Returns:
        pd.DataFrame: Processed DataFrame with validated data
    """
    try:
        df = pd.read_csv(file)
        
        # Validate required columns
        required_columns = ['Date', 'Price', 'Breakpoint']
        if not all(col in df.columns for col in required_columns):
            raise ValueError("CSV must contain Date, Price, and Breakpoint columns")
        
        # Convert date column to datetime
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Sort by date
        df = df.sort_values('Date')
        
        # Validate price data
        if not df['Price'].dtype in ['float64', 'int64']:
            df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
        
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
