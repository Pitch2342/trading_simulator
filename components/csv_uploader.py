import streamlit as st
import pandas as pd
import io
from typing import Optional, Tuple

def validate_csv_format(df: pd.DataFrame) -> Tuple[bool, str]:
    """
    Validate if the uploaded CSV has the correct format.
    
    Args:
        df: DataFrame to validate
        
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    required_columns = ['Date', 'Price', 'Breakpoint']
    
    # Check if all required columns exist
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        return False, f"Missing required columns: {', '.join(missing_columns)}"
    
    # Check if DataFrame is not empty
    if df.empty:
        return False, "CSV file is empty"
    
    # Validate Date column
    try:
        pd.to_datetime(df['Date'])
    except:
        return False, "Date column contains invalid date formats. Use YYYY-MM-DD format"
    
    # Validate Price column
    try:
        pd.to_numeric(df['Price'], errors='raise')
    except:
        return False, "Price column contains non-numeric values"
    
    # Validate Breakpoint column
    if not df['Breakpoint'].isin([0, 1, True, False]).all():
        return False, "Breakpoint column must contain only 0/1 or True/False values"
    
    # Check minimum number of rows
    if len(df) < 5:
        return False, "CSV must contain at least 5 rows of data"
    
    return True, "Valid format"

def render_csv_uploader() -> Optional[pd.DataFrame]:
    """
    Render the CSV upload interface with format validation.
    
    Returns:
        Optional[pd.DataFrame]: Processed DataFrame if upload is successful, None otherwise
    """
    st.markdown("### Upload Custom Data")
    
    # Show format requirements in a simple info box instead of expander
    st.info("""
    **📋 CSV Format Requirements:**
    
    **Required Columns:** `Date` (YYYY-MM-DD), `Price` (numeric), `Breakpoint` (0/1 or True/False)
    
    **Example:** Date,Price,Breakpoint → 2024-01-01,185.25,0
    
    **Notes:** Minimum 5 rows • Data sorted by date • Breakpoints mark trading decisions
    """)
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=['csv'],
        key="csv_uploader",
        help="Upload a CSV file with Date, Price, and Breakpoint columns"
    )
    
    if uploaded_file is not None:
        try:
            # Read the uploaded file
            df = pd.read_csv(uploaded_file)
            
            # Validate format
            is_valid, message = validate_csv_format(df)
            
            if is_valid:
                # Process the data
                df['Date'] = pd.to_datetime(df['Date'])
                df = df.sort_values('Date').reset_index(drop=True)
                df['Price'] = pd.to_numeric(df['Price'])
                df['Breakpoint'] = df['Breakpoint'].astype(bool)
                
                st.success("✅ CSV format is valid!")
                
                # # Show preview
                # st.markdown("**Data Preview:**")
                # st.dataframe(df.head(10), use_container_width=True)
                
                # Show summary stats and download button in 2x2 layout
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Total Rows", len(df))
                with col2:
                    st.metric("Price Range", f"${df['Price'].min():.2f} - ${df['Price'].max():.2f}")
                
                col3, col4 = st.columns(2)
                with col3:
                    st.metric("Breakpoints", df['Breakpoint'].sum())
                with col4:
                    # Convert DataFrame to CSV for download
                    csv_data = df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Current Data",
                        data=csv_data,
                        file_name="current_trading_data.csv",
                        mime="text/csv",
                        help="Download the currently loaded CSV data"
                    )
                
                return df
                
            else:
                st.error(f"❌ Invalid CSV format: {message}")
                return None
                
        except Exception as e:
            st.error(f"❌ Error reading CSV file: {str(e)}")
            return None
    
    return None

def download_sample_csv():
    """
    Provide a sample CSV file for download.
    """
    sample_data = """Date,Price,Breakpoint
2024-01-01,185.25,0
2024-01-02,187.30,0
2024-01-03,186.75,1
2024-01-04,188.20,0
2024-01-05,189.80,0
2024-01-06,188.90,1
2024-01-07,190.40,0
2024-01-08,191.75,0
2024-01-09,192.20,1
2024-01-10,191.50,0
2024-01-11,193.30,0
2024-01-12,194.15,1
2024-01-13,193.80,0
2024-01-14,195.25,0
2024-01-15,196.40,1"""
    
    st.download_button(
        label="📥 Download Sample CSV",
        data=sample_data,
        file_name="sample_trading_data.csv",
        mime="text/csv",
        help="Download a sample CSV file with the correct format"
    ) 