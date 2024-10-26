import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import sys
import os
os.system("pip install plotly")
import plotly.express as px
import pymysql
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from src.utils.database_utils import DatabaseConnection
from src.utils.ml_utils import CustomerPredictor

# Initialize database connection
@st.cache_resource
def init_db_connection():
    db_connection = DatabaseConnection()
    engine = db_connection.connect()
    if engine is None:
        st.error("Failed to connect to the database.")
    return db_connection

def main():
    st.title("Customer Orders Dashboard")
    
    # Initialize database connection
    db_connection = init_db_connection()
    if db_connection is None:
        st.error("Database connection failed.")
        return
    
    # Sidebar filters
    st.sidebar.header("Filters")
    
    # Date range filter
    default_start_date = datetime.now() - timedelta(days=365)
    default_end_date = datetime.now()
    
    start_date = st.sidebar.date_input(
        "Start Date",
        value=default_start_date,
        max_value=default_end_date
    )
    
    end_date = st.sidebar.date_input(
        "End Date",
        value=default_end_date,
        min_value=start_date
    )
    
    # Amount spent filter
    min_amount = st.sidebar.slider(
        "Minimum Total Spent ($)",
        min_value=0,
        max_value=10000,
        value=0,
        step=100
    )
    
    # Minimum orders filter
    min_orders = st.sidebar.selectbox(
        "Minimum Number of Orders",
        options=[0, 1, 2, 3, 4, 5, 10],
        index=0
    )
    
    # Retrieve data from database
    filtered_data = db_connection.get_filtered_data(
        start_date=start_date,
        end_date=end_date,
        min_total_amount=min_amount,
        min_orders=min_orders
    )
    
    if filtered_data.empty:
        st.warning("No data found for the selected filters.")
        return
    
    # Summary metrics
    st.header("Summary Metrics")
    total_revenue = filtered_data['total_amount'].sum()
    unique_customers = filtered_data['customer_id'].nunique()
    total_orders = filtered_data.shape[0]
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Revenue", f"${total_revenue:,.2f}")
    with col2:
        st.metric("Unique Customers", unique_customers)
    with col3:
        st.metric("Total Orders", total_orders)
        
    # Top 10 customers chart
    st.header("Top 10 Customers by Revenue")
    top_customers = filtered_data.groupby('customer_id')['total_amount'].sum().sort_values(ascending=False).head(10)
    
    fig_top_customers = px.bar(
        x=top_customers.index,
        y=top_customers.values,
        labels={'x': 'Customer ID', 'y': 'Total Revenue ($)'},
        title="Top 10 Customers by Revenue"
    )
    st.plotly_chart(fig_top_customers)
    
    # Revenue over time
    st.header("Revenue Over Time")
    daily_revenue = filtered_data.groupby(filtered_data['created_at'].dt.date)['total_amount'].sum().reset_index()
    daily_revenue.columns = ['Date', 'Revenue']
    
    fig_revenue = px.line(
        daily_revenue,
        x='Date',
        y='Revenue',
        labels={'Date': 'Date', 'Revenue': 'Revenue ($)'},
        title="Revenue Over Time"
    )
    st.plotly_chart(fig_revenue)
    
    # Filtered data table
    st.header("Filtered Orders")
    st.dataframe(
        filtered_data[['customer_id', 'display_order_id', 'created_at', 'total_amount']]
        .sort_values('created_at', ascending=False)
    )
    
if __name__ == "__main__":
    main()















# import streamlit as st
# import pandas as pd
# import plotly.express as px
# from datetime import datetime, timedelta

# # Initialize data loading function
# @st.cache_resource
# def load_data():
#     try:
#         # Load customer and order data from CSV files
#         customers_df = pd.read_csv("data/processed/customers_cleaned.csv")
#         orders_df = pd.read_csv("data/processed/orders_cleaned.csv")
        
#         # Ensure 'created_at' is in datetime format
#         orders_df['created_at'] = pd.to_datetime(orders_df['created_at'])
        
#         # Merge datasets if needed or return separately
#         return customers_df, orders_df
#     except Exception as e:
#         st.error(f"Error loading data: {e}")
#         return pd.DataFrame(), pd.DataFrame()  # Return empty DataFrames if loading fails

# def main():
#     st.title("Customer Orders Dashboard")
    
#     # Load data
#     customers_df, orders_df = load_data()
    
#     if customers_df.empty or orders_df.empty:
#         st.warning("No data available. Please check the CSV files.")
#         return
    
#     # Sidebar filters
#     st.sidebar.header("Filters")
    
#     # Date range filter
#     default_start_date = datetime.now() - timedelta(days=365)
#     default_end_date = datetime.now()
    
#     start_date = st.sidebar.date_input(
#         "Start Date",
#         value=default_start_date,
#         max_value=default_end_date
#     )
    
#     end_date = st.sidebar.date_input(
#         "End Date",
#         value=default_end_date,
#         min_value=start_date
#     )
    
#     # Amount spent filter
#     min_amount = st.sidebar.slider(
#         "Minimum Total Spent ($)",
#         min_value=0,
#         max_value=10000,
#         value=0,
#         step=100
#     )
    
#     # Minimum orders filter
#     min_orders = st.sidebar.selectbox(
#         "Minimum Number of Orders",
#         options=[0, 1, 2, 3, 4, 5, 10],
#         index=0
#     )
    
#     # Apply filters to data
#     filtered_orders_df = orders_df[
#         (orders_df['created_at'] >= pd.to_datetime(start_date)) &
#         (orders_df['created_at'] <= pd.to_datetime(end_date)) &
#         (orders_df['total_amount'] >= min_amount)
#     ]
    
#     # Filter by minimum orders per customer
#     order_counts = filtered_orders_df['customer_id'].value_counts()
#     customers_with_min_orders = order_counts[order_counts >= min_orders].index
#     filtered_orders_df = filtered_orders_df[filtered_orders_df['customer_id'].isin(customers_with_min_orders)]
    
#     if filtered_orders_df.empty:
#         st.warning("No data found for the selected filters.")
#         return
    
#     # Summary metrics
#     st.header("Summary Metrics")
#     total_revenue = filtered_orders_df['total_amount'].sum()
#     unique_customers = filtered_orders_df['customer_id'].nunique()
#     total_orders = filtered_orders_df.shape[0]
    
#     col1, col2, col3 = st.columns(3)
#     with col1:
#         st.metric("Total Revenue", f"${total_revenue:,.2f}")
#     with col2:
#         st.metric("Unique Customers", unique_customers)
#     with col3:
#         st.metric("Total Orders", total_orders)
        
#     # Top 10 customers chart
#     st.header("Top 10 Customers by Revenue")
#     top_customers = filtered_orders_df.groupby('customer_id')['total_amount'].sum().sort_values(ascending=False).head(10)
    
#     fig_top_customers = px.bar(
#         x=top_customers.index,
#         y=top_customers.values,
#         labels={'x': 'Customer ID', 'y': 'Total Revenue ($)'},
#         title="Top 10 Customers by Revenue"
#     )
#     st.plotly_chart(fig_top_customers)
    
#     # Revenue over time
#     st.header("Revenue Over Time")
#     daily_revenue = filtered_orders_df.groupby(filtered_orders_df['created_at'].dt.date)['total_amount'].sum().reset_index()
#     daily_revenue.columns = ['Date', 'Revenue']
    
#     fig_revenue = px.line(
#         daily_revenue,
#         x='Date',
#         y='Revenue',
#         labels={'Date': 'Date', 'Revenue': 'Revenue ($)'},
#         title="Revenue Over Time"
#     )
#     st.plotly_chart(fig_revenue)
    
#     # Filtered data table
#     st.header("Filtered Orders")
#     st.dataframe(
#         filtered_orders_df[['customer_id', 'display_order_id', 'created_at', 'total_amount']]
#         .sort_values('created_at', ascending=False)
#     )
    
#     # Optional Machine Learning Section (If Predictor Available)
#     st.header("Repeat Customer Prediction (Optional)")
#     st.info("This section is for predicting repeat customers. Uncomment relevant code if CustomerPredictor is available.")

# if __name__ == "__main__":
#     main()
