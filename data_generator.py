import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_sales_data(num_entries=1000):
    """
    Generate synthetic sales data for New Balance shoes.
    This is only for demonstration purposes of the dashboard UI.
    
    Returns:
        pd.DataFrame: A dataframe with synthetic sales data
    """
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Current date and date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)  # Last year of data
    
    # Generate random dates
    dates = [start_date + timedelta(days=np.random.randint(0, 365)) for _ in range(num_entries)]
    
    # New Balance models with release years and ratings
    model_data = {
        '990v5': {'release_year': 2019, 'avg_rating': 4.7},
        '574': {'release_year': 1988, 'avg_rating': 4.5},
        '997': {'release_year': 1991, 'avg_rating': 4.6},
        '327': {'release_year': 2020, 'avg_rating': 4.4},
        '1080v12': {'release_year': 2022, 'avg_rating': 4.8},
        '550': {'release_year': 2020, 'avg_rating': 4.6},
        '2002R': {'release_year': 2021, 'avg_rating': 4.7},
        'Fresh Foam X': {'release_year': 2022, 'avg_rating': 4.3},
        '993': {'release_year': 2008, 'avg_rating': 4.9},
        '9060': {'release_year': 2022, 'avg_rating': 4.2},
        '530': {'release_year': 1992, 'avg_rating': 4.4},
        '608': {'release_year': 1996, 'avg_rating': 4.1},
        '57/40': {'release_year': 2021, 'avg_rating': 4.3},
        '1500': {'release_year': 1993, 'avg_rating': 4.6},
        '237': {'release_year': 2021, 'avg_rating': 4.2},
        '860v13': {'release_year': 2023, 'avg_rating': 4.5},
        '992': {'release_year': 2006, 'avg_rating': 4.8},
        '1300': {'release_year': 1985, 'avg_rating': 4.7},
        '480': {'release_year': 1988, 'avg_rating': 4.3},
        '5740': {'release_year': 2021, 'avg_rating': 4.4},
        'XC-72': {'release_year': 2021, 'avg_rating': 4.5}
    }
    
    # Models list
    models = list(model_data.keys())
    
    # Categories
    categories = [
        'Running', 'Lifestyle', 'Training', 'Walking', 
        'Hiking', 'Basketball', 'Tennis', 'Made in USA'
    ]
    
    # Regions
    regions = [
        'North America', 'Europe', 'Asia Pacific', 
        'Latin America', 'Middle East', 'Africa'
    ]
    
    # Generate data
    data = {
        'date': dates,
        'model': np.random.choice(models, num_entries),
        'category': np.random.choice(categories, num_entries),
        'region': np.random.choice(regions, num_entries),
        'quantity': np.random.randint(1, 50, num_entries),
        'price': np.random.uniform(60, 250, num_entries).round(2)
    }
    
    # Create dataframe
    df = pd.DataFrame(data)
    
    # Calculate total price
    df['total_price'] = df['quantity'] * df['price']
    
    # Add release year and average rating
    df['release_year'] = df['model'].apply(lambda x: model_data[x]['release_year'])
    df['avg_rating'] = df['model'].apply(lambda x: model_data[x]['avg_rating'])
    
    # Sort by date
    df = df.sort_values('date')
    
    return df
