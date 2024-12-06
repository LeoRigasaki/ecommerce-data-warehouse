import pandas as pd
from datetime import datetime, timedelta

def get_date_key(date_str, cursor):
    """
    Gets or creates a date key for the dim_date table.
    
    Args:
        date_str: String representation of date (can be None)
        cursor: Database cursor for executing queries
    
    Returns:
        date_key if date is valid, None otherwise
    """
    if pd.isna(date_str):
        return None
        
    try:
        # Convert string to datetime
        date_actual = pd.to_datetime(date_str).date()
        
        # Check if date exists
        cursor.execute(
            "SELECT date_key FROM dim_date WHERE date_actual = %s",
            (date_actual,)
        )
        result = cursor.fetchone()
        
        if result:
            return result[0]
            
        # If date doesn't exist, create it
        cursor.execute("""
            INSERT INTO dim_date (
                date_actual, year, month, day, 
                quarter, day_of_week, is_weekend
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING date_key
        """, (
            date_actual,
            date_actual.year,
            date_actual.month,
            date_actual.day,
            (date_actual.month - 1) // 3 + 1,
            date_actual.isoweekday(),
            date_actual.isoweekday() >= 6
        ))
        
        return cursor.fetchone()[0]
        
    except (ValueError, TypeError):
        return None