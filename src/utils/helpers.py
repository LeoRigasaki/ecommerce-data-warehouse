import pandas as pd
from datetime import datetime

def clean_string(s):
    """Clean and standardize string values"""
    return str(s).strip().lower() if pd.notna(s) else None

def parse_date(date_str):
    """Parse date string to datetime"""
    try:
        return pd.to_datetime(date_str) if pd.notna(date_str) else None
    except:
        return None

def generate_date_dimensions(date_obj):
    """Generate date dimension attributes"""
    if date_obj is None:
        return None
    
    return {
        'date_actual': date_obj.date(),
        'year': date_obj.year,
        'month': date_obj.month,
        'day': date_obj.day,
        'quarter': (date_obj.month - 1) // 3 + 1,
        'day_of_week': date_obj.weekday(),
        'is_weekend': date_obj.weekday() >= 5
    }

def get_or_create_date_key(cursor, date_obj):
    """Get existing date_key or create new one"""
    if date_obj is None:
        return None
        
    date_actual = date_obj.date()
    
    # Check if exists
    cursor.execute(
        "SELECT date_key FROM dim_date WHERE date_actual = %s",
        (date_actual,)
    )
    result = cursor.fetchone()
    
    if result:
        return result[0]
    
    # Create new
    date_dims = generate_date_dimensions(date_obj)
    cursor.execute("""
        INSERT INTO dim_date (
            date_actual, year, month, day,
            quarter, day_of_week, is_weekend
        ) VALUES (
            %(date_actual)s, %(year)s, %(month)s,
            %(day)s, %(quarter)s, %(day_of_week)s,
            %(is_weekend)s
        ) RETURNING date_key
    """, date_dims)
    
    return cursor.fetchone()[0]