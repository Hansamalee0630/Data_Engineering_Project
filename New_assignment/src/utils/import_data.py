import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
import pymysql

def load_data_from_db():
    # Load environment variables
    load_dotenv()
    
    # Get database connection details from environment variables
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_DATABASE = os.getenv('DB_DATABASE')
    
    # Create connection string
    connection_string = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_DATABASE}"
    
    try:
        # Create database engine
        engine = create_engine(connection_string)
        
        # Print current working directory and available files
        print(f"Current working directory: {os.getcwd()}")
        print(f"Files in current directory: {os.listdir()}")
        
        # Load data from MySQL with error handling
        try:
            customers_df = pd.read_sql("SELECT * FROM customers", engine)
            print(f"Successfully loaded customers data with {len(customers_df)} rows")
        except Exception as e:
            print(f"Error loading customers data: {e}")
            return
            
        try:
            orders_df = pd.read_sql("SELECT * FROM orders", engine)
            print(f"Successfully loaded orders data with {len(orders_df)} rows")
        except Exception as e:
            print(f"Error loading orders data: {e}")
            return
        
        # Convert created_at to datetime, handling invalid dates
        orders_df['created_at'] = pd.to_datetime(orders_df['created_at'], errors='coerce')
        
        # Print sample of data
        print("\nCustomers data sample:")
        print(customers_df.head())
        print("\nOrders data sample:")
        print(orders_df.head())
        
        # Display summary statistics for both datasets
        print("\nCustomers data summary:")
        print(customers_df.describe())
        print("\nOrders data summary:")
        print(orders_df.describe())
        
        # Display date range for orders
        min_date = orders_df['created_at'].min()
        max_date = orders_df['created_at'].max()
        print(f"Order date range: {min_date} to {max_date}")
        
        # Handle rows with invalid dates
        invalid_dates = orders_df[orders_df['created_at'].isna()]
        if not invalid_dates.empty:
            print(f"\nRows with invalid dates: {len(invalid_dates)}")
            print(invalid_dates)
        
    except Exception as e:
        print(f"Error in loading data process: {e}")

if __name__ == "__main__":
    load_data_from_db()