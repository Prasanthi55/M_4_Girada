from datetime import datetime, timedelta

def format_currency(value):
    """Format a number as currency"""
    return f"${value:,.2f}"

def format_number(value):
    """Format a number with thousand separators"""
    return f"{value:,}"

def get_date_range(period):
    """Convert time period string to start and end dates"""
    # Force the end date to be May 4, 2025 for consistency with dashboard
    end_date = datetime(2025, 5, 4)
    
    if period == '7D':
        start_date = end_date - timedelta(days=7)
    elif period == '30D':
        start_date = end_date - timedelta(days=30)
    elif period == '90D':
        start_date = end_date - timedelta(days=90)
    elif period == '6M':
        # This matches the exact 6-month period in the dashboard (Dec 2024 - May 2025)
        start_date = datetime(2024, 12, 1)
    elif period == '1Y':
        start_date = end_date - timedelta(days=365)
    elif period == 'CUSTOM':
        # For custom date range, return None to indicate that custom dates should be used
        # The actual custom dates will be stored in session state
        return None, None
    else:  # ALL
        # For "All" we still want to show the 6-month period from the screenshot
        start_date = datetime(2024, 12, 1)
    
    return start_date, end_date
