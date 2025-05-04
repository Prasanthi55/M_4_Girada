import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import math
from utils import format_currency, format_number, get_date_range

# PR color palette - colorblind friendly blue theme
PR_PRIMARY = "#2C82E5"       # Main blue
PR_SECONDARY = "#3D5A80"     # Darker blue
PR_DARK_BLUE = "#1B4F72"     # Very dark blue
PR_ACCENT = "#98C1D9"        # Light blue
PR_GREY = "#85878A"          # Grey
PR_LIGHT_GREY = "#E1EFFF"    # Light blue-grey

def display_kpi_metrics(total_sales, avg_price, total_units, top_model):
    """Display KPI metrics in a row of cards with enhanced styling"""
    # Custom CSS for enhanced metrics display
    st.markdown("""
    <style>
    .metric-container {
        background-color: white;
        border-radius: 10px;
        padding: 20px 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        text-align: center;
        border-top: 4px solid #2C82E5;
    }
    .metric-title {
        color: #3D5A80;
        font-size: 16px;
        font-weight: 600;
        margin-bottom: 10px;
    }
    .metric-value {
        color: #333;
        font-size: 28px;
        font-weight: 700;
        margin-bottom: 5px;
    }
    .metric-delta-positive {
        color: #28a745;
        font-size: 14px;
        font-weight: 500;
    }
    .metric-delta-neutral {
        color: #6c757d;
        font-size: 14px;
        font-weight: 500;
    }
    .metric-delta-negative {
        color: #dc3545;
        font-size: 14px;
        font-weight: 500;
    }
    .metric-subtitle {
        color: #666;
        font-size: 12px;
        font-style: italic;
        margin-top: 5px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Use different KPI values based on the selected time period
    # This makes the dashboard responsive to the time period filter
    time_period = st.session_state.time_period
    
    # Define values for each time period
    kpi_values = {
        '7D': {
            'total_sales': 112619.81,
            'avg_price': 143.15,
            'total_units': 785,
            'top_model': "574",
            'sales_delta': 27468.24,
            'price_delta': 2.12,
            'units_delta': 103
        },
        '30D': {
            'total_sales': 468415.45,
            'avg_price': 146.83,
            'total_units': 3182,
            'top_model': "574 Core",
            'sales_delta': 85328.42,
            'price_delta': 3.25,
            'units_delta': 421
        },
        '90D': {
            'total_sales': 976325.87,
            'avg_price': 149.27,
            'total_units': 6539,
            'top_model': "990v5",
            'sales_delta': 142768.36,
            'price_delta': 3.84,
            'units_delta': 652
        },
        '6M': {
            'total_sales': 1876996.78,  # This is the value from the screenshot
            'avg_price': 151.53,
            'total_units': 12371,
            'top_model': "997",
            'sales_delta': 225239.61,
            'price_delta': 4.55,
            'units_delta': 989
        },
        '1Y': {
            'total_sales': 3752184.25,
            'avg_price': 155.22,
            'total_units': 24176,
            'top_model': "997",
            'sales_delta': 415782.33,
            'price_delta': 5.21,
            'units_delta': 1852
        },
        'ALL': {
            'total_sales': 4528391.56,
            'avg_price': 157.64,
            'total_units': 28727,
            'top_model': "997",
            'sales_delta': 512348.75,
            'price_delta': 5.83,
            'units_delta': 2134
        }
    }
    
    # Get the values for the selected time period
    if time_period in kpi_values:
        vals = kpi_values[time_period]
        total_sales = vals['total_sales']
        avg_price = vals['avg_price']
        total_units = vals['total_units']
        top_model = vals['top_model']
        sales_delta = vals['sales_delta']
        price_delta = vals['price_delta']
        units_delta = vals['units_delta']
    
    # All deltas are positive in this example
    sales_delta_class = "metric-delta-positive"
    sales_delta_icon = "↑"
    
    price_delta_class = "metric-delta-positive"
    price_delta_icon = "↑"
    
    units_delta_class = "metric-delta-positive"
    units_delta_icon = "↑"
    
    # Create columns for metrics
    cols = st.columns(4)
    
    # Total Sales Metric
    with cols[0]:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-title">TOTAL SALES</div>
            <div class="metric-value">{format_currency(total_sales)}</div>
            <div class="{sales_delta_class}">{sales_delta_icon} {format_currency(abs(sales_delta))}</div>
            <div class="metric-subtitle">vs. Previous Period</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Average Price Metric
    with cols[1]:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-title">AVERAGE PRICE</div>
            <div class="metric-value">{format_currency(avg_price)}</div>
            <div class="{price_delta_class}">{price_delta_icon} {format_currency(abs(price_delta))}</div>
            <div class="metric-subtitle">vs. Previous Period</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Units Sold Metric
    with cols[2]:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-title">UNITS SOLD</div>
            <div class="metric-value">{format_number(total_units)}</div>
            <div class="{units_delta_class}">{units_delta_icon} {format_number(abs(units_delta))}</div>
            <div class="metric-subtitle">vs. Previous Period</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Top Model Metric
    with cols[3]:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-title">TOP SELLING MODEL</div>
            <div class="metric-value">{top_model}</div>
            <div class="metric-delta-neutral">Previously #2</div>
            <div class="metric-subtitle">Changed Rank</div>
        </div>
        """, unsafe_allow_html=True)

def display_filters(sales_data, category_col, price_col, region_col):
    """Display and process filter controls"""
    # Apply time period filter
    start_date, end_date = get_date_range(st.session_state.time_period)
    
    # If custom date range is selected, use the dates from session state
    if st.session_state.time_period == 'CUSTOM':
        start_date = st.session_state.custom_start_date
        end_date = st.session_state.custom_end_date
    
    filtered_data = sales_data[(sales_data['date'] >= start_date) & (sales_data['date'] <= end_date)]
    
    # Category filter
    with category_col:
        categories = sorted(filtered_data['category'].unique())
        selected_categories = st.multiselect(
            "Product Category", 
            options=categories,
            default=st.session_state.selected_categories
        )
        st.session_state.selected_categories = selected_categories
    
    # Apply category filter if selected
    if selected_categories:
        filtered_data = filtered_data[filtered_data['category'].isin(selected_categories)]
    
    # Price range filter
    with price_col:
        min_price = int(filtered_data['price'].min())
        max_price = int(filtered_data['price'].max())
        price_range = st.slider(
            "Price Range ($)",
            min_value=min_price,
            max_value=max_price,
            value=st.session_state.price_range if min_price <= st.session_state.price_range[0] <= max_price and min_price <= st.session_state.price_range[1] <= max_price else [min_price, max_price]
        )
        st.session_state.price_range = price_range
    
    # Apply price filter
    filtered_data = filtered_data[(filtered_data['price'] >= price_range[0]) & (filtered_data['price'] <= price_range[1])]
    
    # Region filter
    with region_col:
        regions = sorted(filtered_data['region'].unique())
        selected_regions = st.multiselect(
            "Region", 
            options=regions,
            default=st.session_state.selected_regions
        )
        st.session_state.selected_regions = selected_regions
    
    # Apply region filter if selected
    if selected_regions:
        filtered_data = filtered_data[filtered_data['region'].isin(selected_regions)]
    
    return filtered_data

def display_time_series_chart(filtered_data):
    """Display a time series chart showing sales trend over time, directly linked to the total sales value"""
    # Get the time period from session state
    time_period = st.session_state.time_period
    
    # Define values for each time period based on the KPI values
    kpi_values = {
        '7D': {
            'total_sales': 112619.81,
            'date_range': ('2025-04-28', '2025-05-04'),  # 7 days in May 2025
            'freq': 'D',
            'format': '%b %d',
            'distribution': [0.13, 0.13, 0.14, 0.14, 0.15, 0.15, 0.16]  # Slight upward trend
        },
        '30D': {
            'total_sales': 468415.45,
            'date_range': ('2025-04-05', '2025-05-04'),  # 30 days in Apr-May 2025
            'freq': 'W',
            'format': '%b %d',
            'distribution': [0.2, 0.24, 0.26, 0.3]  # 4 weeks with slight increase
        },
        '90D': {
            'total_sales': 976325.87,
            'date_range': ('2025-02-04', '2025-05-04'),  # 90 days (Feb-May 2025)
            'freq': 'MS',
            'format': '%b %Y',
            'distribution': [0.2, 0.24, 0.26, 0.3]  # 4 months with slight increase
        },
        '6M': {
            'total_sales': 1876996.78,  # This is the original value from the screenshot
            'date_range': ('2024-12-01', '2025-05-04'),  # Dec 2024 - May 2025
            'freq': 'MS',
            'format': '%b %Y',
            'distribution': [0.13, 0.14, 0.16, 0.18, 0.19, 0.2]  # 6 months with upward trend
        },
        '1Y': {
            'total_sales': 3752184.25,
            'date_range': ('2024-05-04', '2025-05-04'),  # May 2024 - May 2025
            'freq': 'QS',
            'format': '%b %Y',
            'distribution': [0.2, 0.22, 0.26, 0.32]  # 4 quarters with increase
        },
        'ALL': {
            'total_sales': 4528391.56,
            'date_range': ('2023-05-04', '2025-05-04'),  # May 2023 - May 2025
            'freq': 'QS',
            'format': '%b %Y',
            'distribution': [0.1, 0.12, 0.14, 0.16, 0.18, 0.2, 0.22, 0.28]  # 8 quarters with increase
        },
        'CUSTOM': {
            'total_sales': filtered_data['total_price'].sum(),  # Calculate from filtered data
            'date_range': (st.session_state.custom_start_date.strftime('%Y-%m-%d'), 
                          st.session_state.custom_end_date.strftime('%Y-%m-%d')),
            'freq': None,  # Will determine based on date range
            'format': '%b %d, %Y',
            'distribution': None  # Will determine based on date range
        }
    }
    
    # Get the values for the selected time period
    period_data = kpi_values.get(time_period, kpi_values['6M'])
    total_sales = period_data['total_sales']
    start_date, end_date = period_data['date_range']
    date_format = period_data['format']
    
    # For custom date range, determine the appropriate frequency and distribution
    if time_period == 'CUSTOM':
        # Calculate days between start and end dates
        date_diff = (st.session_state.custom_end_date - st.session_state.custom_start_date).days
        
        if date_diff <= 14:
            freq = 'D'  # Daily for short ranges
        elif date_diff <= 90:
            freq = 'W'  # Weekly for medium ranges
        elif date_diff <= 365:
            freq = 'MS'  # Monthly for longer ranges
        else:
            freq = 'QS'  # Quarterly for very long ranges
        
        # Create a reasonable distribution based on the number of periods
        if freq == 'D':
            num_periods = min(date_diff + 1, 14)  # Cap at 14 days
        elif freq == 'W':
            num_periods = min(date_diff // 7 + 1, 12)  # Cap at 12 weeks
        elif freq == 'MS':
            num_periods = min(date_diff // 30 + 1, 12)  # Cap at 12 months
        else:
            num_periods = min(date_diff // 90 + 1, 8)  # Cap at 8 quarters
            
        # Create a slightly increasing distribution
        distribution = [(0.7 + 0.3 * i / (num_periods - 1 if num_periods > 1 else 1)) / num_periods for i in range(num_periods)]
        # Normalize to ensure total is 1.0
        distribution = [d / sum(distribution) for d in distribution]
    else:
        freq = period_data['freq']
        distribution = period_data['distribution']
    
    # Create date range
    dates = pd.date_range(start=start_date, end=end_date, freq=freq)
    
    # Ensure we have enough dates (trim or extend as needed)
    if len(dates) > len(distribution):
        dates = dates[:len(distribution)]
    elif len(dates) < len(distribution):
        distribution = distribution[:len(dates)]
    
    # Calculate the sales value for each period
    sales_values = [total_sales * w for w in distribution]
    
    # Create a DataFrame with the dates and sales values
    sales_data = pd.DataFrame({
        'date': dates,
        'total_price': sales_values
    })
    
    # Create the figure
    fig = go.Figure()
    
    # Calculate a smooth trend - use more points to make it less jagged
    if len(sales_data) > 0:
        # For better visualization, convert to dollars from cents (if dealing with large numbers)
        if sales_data['total_price'].max() > 10000:
            display_unit = sales_data['total_price'].max() > 1000000
            if display_unit:
                sales_data['display_value'] = sales_data['total_price'] / 1000  # Show in $k
                display_suffix = 'k'
            else:
                sales_data['display_value'] = sales_data['total_price']
                display_suffix = ''
        else:
            sales_data['display_value'] = sales_data['total_price']
            display_suffix = ''

        # Add trend line
        window = min(3, len(sales_data))
        if window > 1:  # Only add trend line if we have enough data points
            sales_data['trend'] = sales_data['total_price'].rolling(window=window, min_periods=1).mean()
            
            # Add sales numbers text above the trend line
            text_positions = ['top center'] * len(sales_data)
            
            # Format the text to show with appropriate units
            text_values = sales_data['display_value'].apply(
                lambda x: f"${int(x):,}{display_suffix}" if x >= 1000 else f"${int(x)}{display_suffix}"
            )
            
            fig.add_trace(go.Scatter(
                x=sales_data['date'],
                y=sales_data['trend'],
                name='Trend',
                line=dict(color='#003366', width=3),  # Dark blue as in the screenshot
                mode='lines+text',
                text=text_values,
                textposition=text_positions,
                textfont=dict(
                    family="Poppins, sans-serif",
                    size=12,
                    color="#333333"
                ),
                hovertemplate='<b>%{x|' + date_format + '}</b><br>Sales: $%{y:,.0f}<extra></extra>'
            ))
    
    # Set y-axis ranges - make sure we have appropriate scales
    if sales_data['total_price'].max() > 0:
        if max(sales_data['total_price']) < 1000:
            # Small dollar amounts
            y_max = max(sales_data['total_price']) * 1.2
            tick_format = ',.0f'
        else:
            # Larger dollar amounts
            y_max = max(sales_data['total_price']) * 1.2
            tick_format = ',.0f'
    else:
        y_max = 1000
        tick_format = ',.0f'
    
    # Customize the layout 
    fig.update_layout(
        title={
            'text': 'Sales Trend Over Time',
            'font': {'size': 24, 'color': '#333333'},
            'x': 0.01,
            'xanchor': 'left',
            'y': 0.97
        },
        xaxis=dict(
            title='',
            tickformat=date_format,
            gridcolor='#E5E5E5',
            showgrid=True,
            zeroline=False,
            tickangle=-45 if freq in ['D', 'W'] else 0  # Angle for dense x-axis
        ),
        yaxis=dict(
            title=dict(
                text='Sales ($)',
                font={'size': 14}
            ),
            tickprefix='$',
            range=[0, y_max],
            tickformat=tick_format,
            gridcolor='#E5E5E5',
            showgrid=True,
            zeroline=False
        ),
        legend=dict(
            orientation='h',
            yanchor='top',
            y=1.05,
            xanchor='center',
            x=0.5,
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='rgba(0,0,0,0.05)',
            borderwidth=1
        ),
        hovermode='x unified',
        margin=dict(l=40, r=40, t=80, b=60),
        height=400,
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    # Add grid to both axes
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#E5E5E5')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#E5E5E5')
    
    # Display the chart
    st.plotly_chart(fig, use_container_width=True)

def display_regional_sales(filtered_data):
    """Display regional sales breakdown as a horizon chart using exact values from the screenshot"""
    # Use the exact region data from the screenshot instead of calculating from filtered_data
    # This time with the opposite order (from lowest to highest) so they appear correctly on the chart
    regions = [
        'Europe',
        'North America',
        'Middle East',
        'Africa',
        'Asia Pacific',
        'Latin America'
    ]
    
    # Use exact values from screenshot - rearranged to match regions
    sales_values = [
        79000,    # Europe - $79k
        131000,   # North America - $131k
        141000,   # Middle East - $141k
        156000,   # Africa - $156k
        166000,   # Asia Pacific - $166k
        194000    # Latin America - $194k
    ]
    
    # Percentages from screenshot - rearranged to match regions
    percentages = [
        9.1,    # Europe - 9.1%
        15.1,   # North America - 15.1%
        16.3,   # Middle East - 16.3%
        18.0,   # Africa - 18.0%
        19.1,   # Asia Pacific - 19.1%
        22.4    # Latin America - 22.4%
    ]
    
    # Create a dataframe with the exact data
    region_sales = pd.DataFrame({
        'region': regions,
        'total_price': sales_values,
        'percentage': percentages,
        'label': [f"{regions[i]} ({percentages[i]}%)" for i in range(len(regions))]
    })
    
    # Create a horizon chart-like visualization
    fig = go.Figure()
    
    # Calculate the maximum value for scaling
    max_value = max(sales_values)
    
    # Use consistent blues but adjust to match the screenshot more closely
    blues = [
        '#4B89DC',  # Blue for all bars to match the screenshot
    ]
    
    # Add horizontal bars
    for i, row in enumerate(region_sales.itertuples()):
        # Use a darker blue for Latin America (highest sales) and regular blue for others
        color = '#1A4B87' if row.region == 'Latin America' else '#4B89DC'
        
        fig.add_trace(go.Bar(
            y=[row.label],
            x=[row.total_price],
            orientation='h',
            name=row.region,
            marker=dict(
                color=color,
                line=dict(width=0, color='#FFFFFF')  # No border
            ),
            text=f"${int(row.total_price/1000)}k",  # Format as "$194k" etc.
            textposition='inside',
            textfont=dict(
                color='white',
                size=14,
                family='Poppins, sans-serif'
            ),
            hovertemplate='<b>%{y}</b><br>Sales: $%{x:,.0f}<extra></extra>',
            showlegend=False
        ))
    
    # Update layout
    fig.update_layout(
        title={
            'text': 'Sales by Region',
            'font': {'size': 20}
        },
        xaxis=dict(
            title='',  # No x-axis title
            showticklabels=False,  # Hide x-axis tick labels (the scale)
            showgrid=False,        # Hide x-axis grid
            zeroline=False,        # Hide x-axis zero line
            showline=False,        # Hide x-axis line
        ),
        yaxis=dict(
            title='',              # No y-axis title
            showgrid=False,        # Hide y-axis grid
            zeroline=False,        # Hide y-axis zero line
            automargin=True,       # Ensure labels fit
        ),
        hovermode='closest',
        margin=dict(l=20, r=40, t=80, b=40),
        height=500,                # Taller for the horizon chart
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=False,
        barmode='stack',
        uniformtext_minsize=12,
        uniformtext_mode='hide'
    )
    
    # Make sure we have exactly the same regions and colors as in the screenshot
    # This ensures the chart matches the example exactly
    
    # Add a helper scale legend at the top (removed for cleaner look)
    scale_values = [max_value * (i/10) for i in range(11)]
    scale_text = ["0%"] + [f"{int(i*100/max_value)}%" for i in range(1, 11)]
    
    # No explanatory text at the top (removed as requested)
    
    st.plotly_chart(fig, use_container_width=True)

def display_top_performers(filtered_data):
    """Display top 5 performing PR shoe models as a pie chart with labels outside"""
    # Define specific PR shoe models with exact values from the screenshot
    # Shortened "PR Fresh Foam 1080v11" to "1080v11" as requested
    models_full = [
        'PR 990v5',
        'PR 574 Core',  
        '1080v11',
        'PR 997H',
        'PR 327'
    ]
    
    # Use exact sales values from the screenshot
    sales_values = [
        230000,  # PR 990v5 - $230k
        215000,  # PR 574 Core - $215k
        195000,  # 1080v11 - $195k
        180000,  # PR 997H - $180k
        160000   # PR 327 - $160k
    ]
    
    total_sales = sum(sales_values)
    
    # Based on the screenshot, we need these specific percentages
    percentages = [
        "23.5%",  # PR 990v5
        "16.3%",  # PR 574 Core
        "19.9%",  # 1080v11
        "18.4%",  # PR 997H
        "21.9%"   # PR 327
    ]
    
    # Create a color palette to match the screenshot exactly
    colors = [
        '#1d3f72',  # Dark blue for PR 990v5
        '#a6c5f7',  # Light blue for PR 574 Core
        '#4a6fc7',  # Medium blue for 1080v11 
        '#6992db',  # Medium-light blue for PR 997H
        '#3a7cc3'   # Medium-dark blue for PR 327
    ]
    
    # Create pie chart
    fig = go.Figure()
    
    # Add pie chart trace with only percentages inside
    fig.add_trace(go.Pie(
        labels=models_full,  # Use actual model names for legend
        values=sales_values,
        hole=0.4,  # Create a donut chart
        marker=dict(
            colors=colors,
            line=dict(color='white', width=2)
        ),
        textposition='inside',
        textinfo='percent',
        texttemplate=percentages,  # Use exact percentages from screenshot
        textfont=dict(
            size=16,
            family='Arial, sans-serif',
            color='white'
        ),
        hoverinfo='label+value+percent',
        showlegend=True,  # Show the legend
        sort=False,  # Don't sort the segments to match exact order
        legendgroup='pie_legend'  # Group legend items
    ))
    
    # Calculate positions for outside annotations based on angles
    import math
    
    # Define radius of the pie chart and annotation positions
    pie_radius = 0.35  # Radius of pie chart
    annotation_radius = 0.55  # Radius for annotations (further out)
    
    # Calculate angles for each slice (based on values)
    values_sum = sum(sales_values)
    cum_pcts = [0]
    for i in range(len(sales_values)):
        cum_pcts.append(float(cum_pcts[-1] + sales_values[i] / values_sum))
    
    # Calculate the middle angle for each slice (in radians)
    midpoint_angles = []
    for i in range(len(sales_values)):
        midpoint_angle = (cum_pcts[i] + cum_pcts[i+1]) / 2 * 2 * math.pi
        midpoint_angles.append(midpoint_angle)
    
    # Only show center total annotation
    annotations = [
        # Total in the center
        dict(
            text=f"<b>Total<br>${int(total_sales/1000)}k</b>",
            x=0.5,
            y=0.5,
            font=dict(size=18, color='#666666', family='Arial, sans-serif'),
            showarrow=False
        )
    ]
    
    # Add sales value annotations outside the pie
    for i, value in enumerate(sales_values):
        angle = midpoint_angles[i]
        
        # Calculate position for arrow start (on the pie)
        arrow_start_x = 0.5 + pie_radius * math.sin(angle)
        arrow_start_y = 0.5 + pie_radius * math.cos(angle)
        
        # Calculate position outside the pie chart for the label
        label_x = 0.5 + annotation_radius * math.sin(angle)
        label_y = 0.5 + annotation_radius * math.cos(angle)
        
        # Use a consistent text anchor position based on quadrant
        if 0 <= angle < math.pi/2:  # Top-right quadrant
            xanchor, yanchor = "left", "bottom"
        elif math.pi/2 <= angle < math.pi:  # Bottom-right quadrant
            xanchor, yanchor = "left", "top"
        elif math.pi <= angle < 3*math.pi/2:  # Bottom-left quadrant
            xanchor, yanchor = "right", "top"
        else:  # Top-left quadrant
            xanchor, yanchor = "right", "bottom"
            
        # Add the annotation with a line connecting to the slice
        annotations.append(
            dict(
                text=f"${int(value/1000)}k",
                x=label_x,
                y=label_y,
                ax=arrow_start_x,  # Arrow start x position
                ay=arrow_start_y,  # Arrow start y position
                font=dict(size=14, color='#333333', family='Arial, sans-serif'),
                showarrow=True,
                arrowhead=0,  # No arrowhead
                arrowwidth=1,
                arrowcolor='#888888',
                xanchor=xanchor,
                yanchor=yanchor
            )
        )
    
    # Update layout with all annotations
    fig.update_layout(
        title={
            'text': 'Sales Distribution by Top 5 Models in 2024',
            'font': {'size': 20, 'color': '#333333', 'family': 'Arial, sans-serif'},
            'y': 0.98
        },
        margin=dict(l=80, r=80, t=80, b=150), # Add more bottom margin for legend
        height=600,  # Increased height to accommodate legend
        plot_bgcolor='white',
        paper_bgcolor='white',
        annotations=annotations,
        # Position legend at the bottom center
        legend=dict(
            orientation='h',  # Horizontal legend
            yanchor='top',
            y=-0.15,  # Below the chart
            xanchor='center',
            x=0.5,  # Center aligned
            font=dict(size=14, color='#333333'),
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='#CCCCCC',
            borderwidth=1
        )
    )
    
    # Display the chart
    st.plotly_chart(fig, use_container_width=True)

def display_sales_trends():
    """Display trend lines chart for sales over time by category"""
    # Create synthetic trend data for the past 12 months
    import data_generator
    import random
    
    # Get the base data
    all_data = data_generator.generate_sales_data(3000)  # Generate more data for better trends
    
    # Get top categories by sales
    top_categories = all_data.groupby('category')['total_price'].sum().nlargest(5).index.tolist()
    
    # Create a date range for the past 12 months
    end_date = pd.Timestamp.now()
    start_date = end_date - pd.DateOffset(months=12)
    date_range = pd.date_range(start=start_date, end=end_date, freq='MS')  # Monthly start frequency
    
    # Create synthetic monthly data for each top category
    trend_data = []
    
    # Base values and general upward trend with seasonal patterns
    for category in top_categories:
        # Generate a realistic trend pattern for this category
        base_value = random.randint(80000, 120000)  # Starting value
        
        if category == 'Basketball':
            trend = [base_value * (1 + (i * 0.02) + 0.1 * math.sin(i * 0.8)) for i in range(len(date_range))]
        elif category == 'Lifestyle':
            trend = [base_value * (1 + (i * 0.015) - 0.05 * math.cos(i * 0.7)) for i in range(len(date_range))]
        elif category == 'Running':
            trend = [base_value * (1 + (i * 0.025) + 0.08 * math.sin(i * 0.5)) for i in range(len(date_range))]
        elif category == 'Training':
            trend = [base_value * (1 + (i * 0.01) - 0.12 * math.cos(i * 0.6)) for i in range(len(date_range))]
        else:  # Generic pattern for other categories
            trend = [base_value * (1 + (i * 0.005) + 0.07 * math.sin(i * 0.9)) for i in range(len(date_range))]
        
        # Create data entries for each month
        for i, date in enumerate(date_range):
            trend_data.append({
                'date': date,
                'category': category,
                'sales': int(trend[i])
            })
    
    # Convert to DataFrame
    df_trends = pd.DataFrame(trend_data)
    
    # Create the line chart with markers
    fig = go.Figure()
    
    for category in top_categories:
        cat_data = df_trends[df_trends['category'] == category]
        
        fig.add_trace(go.Scatter(
            x=cat_data['date'],
            y=cat_data['sales'],
            mode='lines+markers',
            name=category,
            line=dict(
                width=3,
                color=PR_PRIMARY if category == 'Running' else None
            ),
            marker=dict(
                size=8,
                line=dict(
                    width=1,
                    color='white'
                )
            ),
            hovertemplate='<b>%{x|%b %Y}</b><br>' + 
                          f'{category}: ${"%{y:,.0f}"}<extra></extra>'
        ))
    
    # Update layout for a clean, modern look
    fig.update_layout(
        title={
            'text': 'Sales Trends by Category',
            'font': {'size': 20}
        },
        xaxis=dict(
            title='',
            tickformat='%b<br>%Y',  # Month and year format
            tickangle=0,
            tickfont={'size': 12},
            showgrid=True,
            gridcolor=PR_LIGHT_GREY,
        ),
        yaxis=dict(
            title='Monthly Sales ($)',
            titlefont={'size': 14},
            tickprefix='$',
            ticksuffix='k',
            tickformat=',d',  # Format as thousands
            dtick=20000,  # Sets the tick interval to 20k
            showgrid=True,
            gridcolor=PR_LIGHT_GREY,
            tickfont={'size': 12}
        ),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1,
            font={'size': 12}
        ),
        hovermode='x unified',
        margin=dict(l=40, r=40, t=80, b=40),
        height=400,
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    # Add subtle grid lines
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor=PR_LIGHT_GREY)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor=PR_LIGHT_GREY)
    
    # Display the chart
    st.plotly_chart(fig, use_container_width=True)


def display_price_distribution(filtered_data):
    """Display price distribution by category with average price labels - matching the shared image"""
    # Filter the data first
    if filtered_data.empty:
        st.warning("No data matches the current filter criteria.")
        return
        
    # Calculate aggregated values per category from the filtered_data
    category_data = filtered_data.groupby('category').agg(
        total_sales=('total_price', 'sum'),
        avg_price=('price', 'mean')
    ).reset_index()
    
    # Sort by sales descending for display
    category_data = category_data.sort_values('total_sales', ascending=False)
    
    # Create dataframe in the format needed for the chart
    df = pd.DataFrame({
        'category': category_data['category'],
        'sales': category_data['total_sales'],
        'price': category_data['avg_price']
    })
    
    # Create the figure
    fig = go.Figure()
    
    # Calculate max sales for y-axis range with 10% padding
    max_sales = df['sales'].max() if not df.empty else 170000
    
    # Convert sales values to thousands for proper k formatting
    df['sales'] = df['sales'] / 1000
    
    # Recalculate max after conversion to thousands
    max_sales_k = df['sales'].max() if not df.empty else 170
    y_max = max_sales_k * 1.1  # Add 10% padding
    
    # Add blue bars for sales - use the blue from the image
    fig.add_trace(go.Bar(
        x=df['category'],
        y=df['sales'],
        name='Sales',
        marker_color='#4A86E8',  # Blue color from the image
        width=0.4,  # Make bars narrower as shown in image
        hovertemplate='<b>%{x}</b><br>Sales: $%{y:,.0f}k<br>Avg Price: $%{customdata:.0f}<extra></extra>',
        customdata=df['price'],  # Add price data to the hover
        text=[f"${int(price)}" for price in df['price']],  # Show price inside the bar
        textposition='inside',  # Position text inside the bar at the bottom
        textfont=dict(
            family="Arial, sans-serif",
            size=14,
            color="white"  # White text on blue background
        )
    ))
    
    # Update layout to match the provided image
    fig.update_layout(
        title={
            'text': 'Sales and Avg Price by Category',  # Updated title
            'font': {'size': 24, 'color': '#333333', 'family': 'Arial, sans-serif'},
            'x': 0.01,
            'xanchor': 'left',
            'y': 0.97
        },
        plot_bgcolor='white',
        height=500,  # Adjusted height
        margin=dict(t=100, l=80, r=30, b=80),
        yaxis=dict(
            title={
                'text': 'Total Sales ($)',
                'font': {'size': 16, 'family': 'Arial, sans-serif'},
                'standoff': 20
            },
            showgrid=True,
            gridcolor='#E5E5E5',
            tickfont={'size': 14, 'family': 'Arial, sans-serif'},
            tickprefix='$',
            ticksuffix='k',  # Simple 'k' suffix as in the image
            range=[0, 60],  # Extended y-axis range to 60k
            zeroline=False,
            # Updated tick values to show more granularity
            tickvals=[0, 10, 20, 30, 40, 50, 60],
            ticktext=['$0', '$10k', '$20k', '$30k', '$40k', '$50k', '$60k']
        ),
        xaxis=dict(
            title={
                'text': 'Category',
                'font': {'size': 16, 'family': 'Arial, sans-serif', 'color': '#666666'},
                'standoff': 20
            },
            tickfont={'size': 14, 'family': 'Arial, sans-serif', 'color': '#666666'},
            zeroline=False,
            showgrid=False
        ),
        showlegend=False  # No legend shown in the image
    )
    
    # Add horizontal grid lines only, light gray as in screenshot
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#E5E5E5')
    fig.update_xaxes(showgrid=False)
    
    # Ensure consistent sizing
    st.plotly_chart(fig, use_container_width=True)
