import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
from data_generator import generate_sales_data
from utils import format_currency, format_number
from components import (
    display_kpi_metrics,
    display_filters,
    display_regional_sales,
    display_time_series_chart,
    display_top_performers,
    display_price_distribution,
    display_sales_trends
)

# Page configuration
st.set_page_config(
    page_title="New Balance Performance Hub",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for enhanced styling
st.markdown("""
<style>
    /* Google Font - Import Poppins for a modern look */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* Main container styling */
    .main {
        background-color: #F0F7FF;
        padding: 0 !important;
        font-family: 'Poppins', sans-serif;
    }
    
    /* Header styling */
    .dashboard-header {
        background-color: white;
        padding: 15px 30px;
        border-bottom: 1px solid #E1EFFF;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .dashboard-title {
        color: #2C82E5;
        font-weight: 700;
        font-size: 32px;
        margin: 0;
        font-family: 'Poppins', sans-serif;
        letter-spacing: -0.5px;
    }
    
    .tagline {
        font-family: 'Poppins', sans-serif;
        font-weight: 400;
        color: #3D5A80;
        font-size: 16px;
    }
    
    .date-display {
        color: #3D5A80;
        font-size: 14px;
        margin-top: 5px;
        font-family: 'Poppins', sans-serif;
    }
    
    /* Filter section styling */
    .filter-container {
        background-color: white;
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        margin-top: 20px;
        padding: 20px;
        border-left: 4px solid #2C82E5;
        font-family: 'Poppins', sans-serif;
    }
    
    .filter-title {
        color: #2C82E5;
        font-weight: 600;
        font-size: 18px;
        margin-bottom: 15px;
        font-family: 'Poppins', sans-serif;
    }
    
    /* Section headers */
    .section-header {
        color: #2C82E5;
        font-weight: 600;
        font-size: 22px;
        margin: 25px 0 15px 0;
        padding-bottom: 10px;
        border-bottom: 2px solid #98C1D9;
        font-family: 'Poppins', sans-serif;
    }
    
    /* Streamlit elements overrides */
    .stExpander {
        border: none !important;
        box-shadow: none !important;
    }
</style>
""", unsafe_allow_html=True)

# Dashboard header with logo and title
st.markdown(
    """
    <div class="dashboard-header">
        <div>
            <svg width="170" height="70" viewBox="0 0 170 70" xmlns="http://www.w3.org/2000/svg">
                <!-- Larger PR Logo -->
                <circle cx="35" cy="35" r="28" fill="#2C82E5"/>
                <text x="19" y="44" fill="white" style="font-weight:bold; font-size:28px; font-family:'Poppins',sans-serif;">PR</text>
                <path d="M70 21 L70 49 L84 35 Z" fill="#3D5A80"/>
                <circle cx="98" cy="35" r="7" fill="#3D5A80"/>
            </svg>
        </div>
        <div style="text-align: center;">
            <h1 class="dashboard-title">
                New Balance Performance Hub
            </h1>
            <div class="tagline">Tracking Sales & Market Trends for Top PR Footwear Models</div>
            <div class="subtitle" style="font-size: 14px; color: #555;">Premium Running (PR) - The Leader in Athletic Footwear</div>
        </div>
        <div></div>
    </div>
    """,
    unsafe_allow_html=True
)

# Generate sample data
if 'sales_data' not in st.session_state:
    st.session_state.sales_data = generate_sales_data()

# Initialize session state for filters
if 'time_period' not in st.session_state:
    st.session_state.time_period = '30D'
if 'selected_categories' not in st.session_state:
    st.session_state.selected_categories = []
if 'price_range' not in st.session_state:
    st.session_state.price_range = [0, 300]
if 'selected_regions' not in st.session_state:
    st.session_state.selected_regions = []
if 'custom_start_date' not in st.session_state:
    st.session_state.custom_start_date = datetime(2025, 4, 1)  # Default to 1 month before end date
if 'custom_end_date' not in st.session_state:
    st.session_state.custom_end_date = datetime(2025, 5, 4)  # Default to today

# Main container
main_container = st.container()

with main_container:
    # Filters section
    st.markdown('<div class="filter-container"><div class="filter-title">Filters</div>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        time_periods = {
            '7D': '7 Days',
            '30D': '30 Days',
            '90D': '90 Days',
            '6M': '6 Months',
            '1Y': '1 Year',
            'ALL': 'All Time',
            'CUSTOM': 'Custom Range'
        }
        selected_period = st.selectbox(
            "Time Period", 
            options=list(time_periods.keys()),
            format_func=lambda x: time_periods[x],
            index=list(time_periods.keys()).index(st.session_state.time_period)
        )
        
        # Show date pickers if custom range is selected
        if selected_period == 'CUSTOM':
            col1_left, col1_right = st.columns(2)
            with col1_left:
                new_start_date = st.date_input(
                    "Start Date",
                    value=st.session_state.custom_start_date,
                    min_value=datetime(2024, 1, 1),
                    max_value=st.session_state.custom_end_date,
                    format="MM/DD/YYYY"
                )
                # Convert to datetime at midnight
                new_start_datetime = datetime.combine(new_start_date, datetime.min.time())
                if new_start_datetime != st.session_state.custom_start_date:
                    st.session_state.custom_start_date = new_start_datetime
                    
            with col1_right:
                new_end_date = st.date_input(
                    "End Date",
                    value=st.session_state.custom_end_date,
                    min_value=new_start_date,
                    max_value=datetime(2025, 5, 4),
                    format="MM/DD/YYYY"
                )
                # Convert to datetime at midnight
                new_end_datetime = datetime.combine(new_end_date, datetime.min.time())
                if new_end_datetime != st.session_state.custom_end_date:
                    st.session_state.custom_end_date = new_end_datetime
        
        if selected_period != st.session_state.time_period:
            st.session_state.time_period = selected_period
            st.rerun()
    
    # Apply filters to the data
    filtered_data = display_filters(st.session_state.sales_data, col2, col3, col4)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Calculate metrics for display
    total_sales = filtered_data['total_price'].sum()
    avg_price = filtered_data['price'].mean()
    total_units = filtered_data['quantity'].sum()
    top_model = filtered_data.groupby('model')['total_price'].sum().sort_values(ascending=False).index[0]

    # KPI metrics row
    st.markdown('<div class="section-header">Key Performance Indicators</div>', unsafe_allow_html=True)
    display_kpi_metrics(total_sales, avg_price, total_units, top_model)
    
    # Charts row
    st.markdown('<div class="section-header">Sales Performance</div>', unsafe_allow_html=True)
    
    # Display the new time series chart that adapts to the time period filter
    display_time_series_chart(filtered_data)
    
    # Display the regional sales chart
    display_regional_sales(filtered_data)
    
    # Product performance row
    st.markdown('<div class="section-header">Product Performance</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        display_top_performers(filtered_data)
    
    with col2:
        display_price_distribution(filtered_data)
    
    # Detailed data table
    st.markdown('<div class="section-header">Detailed Sales Data</div>', unsafe_allow_html=True)
    
    detailed_data = filtered_data.copy()
    detailed_data['date'] = detailed_data['date'].dt.date
    detailed_data['price'] = detailed_data['price'].apply(format_currency)
    detailed_data['total_price'] = detailed_data['total_price'].apply(format_currency)
    
    st.dataframe(
        detailed_data[['date', 'model', 'category', 'region', 'quantity', 'price', 'total_price']],
        use_container_width=True,
        column_config={
            "date": "Date",
            "model": "Model",
            "category": "Category",
            "region": "Region",
            "quantity": "Units Sold",
            "price": "Unit Price",
            "total_price": "Total Sales"
        }
    )

# Footer
st.markdown("""
<div style="background-color: #2C82E5; color: white; padding: 15px 0; margin-top: 40px; text-align: center; border-top: 3px solid #98C1D9; font-size: 13px;">
    <div style="display: flex; justify-content: center; align-items: center; gap: 20px;">
        <div>© New Balance Performance Hub</div>
        <div>|</div>
        <div>Last Updated: {}</div>
        <div>|</div>
        <div>Internal Use Only</div>
    </div>
</div>
""".format(datetime.now().strftime("%B %d, %Y")), unsafe_allow_html=True)
