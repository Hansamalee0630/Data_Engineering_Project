"""
database_utils.py: Database Connection Manager

This module manages MySQL database connections and provides utility functions for 
data retrieval, filtering, and metrics calculation for the customer orders system.

Author: Hansamalee Ekanayake
Date: October 2024

Functions:
    connect() -> sqlalchemy.engine.Engine
        Establishes and tests database connection
    get_filtered_data(start_date, end_date, min_total_amount, min_orders) -> pd.DataFrame
        Retrieves filtered customer and order data
    get_summary_metrics(start_date, end_date) -> pd.DataFrame
        Calculates summary statistics for orders
    test_data_exists() -> Tuple[int, int, datetime, datetime]
        Verifies data existence and returns counts and date ranges

Classes:
    DatabaseConnection
        Handles all database operations and connections

Dependencies:
    - pandas
    - sqlalchemy
    - pymysql
    - datetime
"""

import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime
import sys
import os
import pymysql  # Ensure pymysql is imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from config.config import DB_CONFIG  

class DatabaseConnection:
    """
    A class to manage database connections and operations for the customer orders system.
    
    This class handles all database-related operations including connection management,
    data retrieval, and metric calculations.
    
    Attributes:
        connection_string (str): SQLAlchemy connection string
        engine (sqlalchemy.engine.Engine): Database engine instance
        
    Methods:
        connect() -> sqlalchemy.engine.Engine:
            Creates and tests database connection
        get_filtered_data(start_date: datetime, end_date: datetime, 
                         min_total_amount: float, min_orders: int) -> pd.DataFrame:
            Retrieves filtered customer and order data
        get_summary_metrics(start_date: datetime, end_date: datetime) -> pd.DataFrame:
            Calculates order summary statistics
        test_data_exists() -> Tuple[int, int, datetime, datetime]:
            Verifies database data and returns statistics
    """

    
    def __init__(self):
        """
        Initializes the database connection with configuration from DB_CONFIG.
        Constructs the connection string and initializes the engine attribute.
        """
        
        # Debug print to verify DB_CONFIG
        print("DB_CONFIG:", DB_CONFIG)
        
        self.connection_string = f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}/{DB_CONFIG['database']}"
        # Debug print to verify connection string
        print("Connection string:", self.connection_string)
        self.engine = None
        
    def connect(self):
        """
        Establishes connection to the MySQL database.
        
        Returns:
            sqlalchemy.engine.Engine: Database engine if successful, None if failed
            
        Raises:
            Exception: If connection cannot be established
        """
        
        try:
            self.engine = create_engine(self.connection_string)
            # Test connection
            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                print("Database connection successful!")
            return self.engine
        except Exception as e:
            print(f"Error connecting to database: {e}")
            return None
            
    def get_filtered_data(self, start_date, end_date, min_total_amount, min_orders):
        """
        Retrieves filtered customer and order data based on specified criteria.
        
        Args:
            start_date (datetime): Start date for filtering orders
            end_date (datetime): End date for filtering orders
            min_total_amount (float): Minimum total amount spent by customer
            min_orders (int): Minimum number of orders by customer
            
        Returns:
            pd.DataFrame: Filtered customer and order data
        """
        
        query = """
        WITH customer_stats AS (
            SELECT
                c.customer_id,
                c.name,
                COUNT(o.display_order_id) AS order_count,
                SUM(o.total_amount) AS total_spent
            FROM customers c
            LEFT JOIN orders o ON c.customer_id = o.customer_id
            WHERE o.created_at BETWEEN %s AND %s
            AND o.created_at IS NOT NULL
            GROUP BY c.customer_id, c.name
            HAVING SUM(o.total_amount) >= %s
                AND COUNT(o.display_order_id) >= %s
        )
        SELECT
            cs.customer_id,
            cs.name,
            cs.order_count,
            cs.total_spent,
            o.display_order_id,
            o.created_at,
            o.total_amount
        FROM customer_stats cs
        JOIN orders o ON cs.customer_id = o.customer_id
        WHERE o.created_at BETWEEN %s AND %s
        AND o.created_at IS NOT NULL
        ORDER BY o.created_at DESC
        """
        
        try:
            # Prepare parameters as a tuple
            params = (
                start_date, end_date, min_total_amount, min_orders,
                start_date, end_date
            )
            
            # Print debugging info
            print("Executing query with parameters:")
            print(f"  Start date: {start_date}")
            print(f"  End date: {end_date}")
            print(f"  Minimum total amount: {min_total_amount}")
            print(f"  Minimum orders: {min_orders}")
            
            # Execute query with parameterized inputs
            df = pd.read_sql(query, self.engine, params=params)
            
            # Check if data is returned
            if df.empty:
                print("No data returned for the given filters.")
            else:
                print(f"Data fetched successfully: {len(df)} rows.")
                print(df.head())  # Display the first few rows for verification
            
            return df
        except Exception as e:
            print(f"Error executing query: {e}")
            return pd.DataFrame()



            
    def get_summary_metrics(self, start_date, end_date):
        """
        Calculates summary metrics for orders within a date range.
        
        Args:
            start_date (datetime): Start date for calculating metrics
            end_date (datetime): End date for calculating metrics
            
        Returns:
            pd.DataFrame: Summary metrics including unique customers,
                         total orders, and total revenue
        """
        
        query = """
        SELECT 
            COUNT(DISTINCT customer_id) as unique_customers,
            COUNT(display_order_id) as total_orders,
            SUM(total_amount) as total_revenue
        FROM orders
        WHERE created_at BETWEEN :start_date AND :end_date
        """
        
        try:
            # Print parameters for debugging
            print(f"Summary metrics parameters:")
            print(f"Start date: {start_date}")
            print(f"End date: {end_date}")
            
            result = pd.read_sql(
                query,
                self.engine,
                params={"start_date": start_date, "end_date": end_date}
            )
            
            # Print results for debugging
            print(f"Summary metrics results:")
            print(result)
            
            return result
        except Exception as e:
            print(f"Error getting summary metrics: {e}")
            return pd.DataFrame()

    def test_data_exists(self):
        """
        Tests existence of data in the database tables.
        
        Returns:
            Tuple[int, int, datetime, datetime]: Returns a tuple containing:
                - Number of customers
                - Number of orders
                - Earliest order date
                - Latest order date
                
        Raises:
            Exception: If database query fails
        """
        try:
            with self.engine.connect() as conn:
                # Check customers table
                result = conn.execute(text("SELECT COUNT(*) FROM customers"))
                customers_count = result.scalar()
                print(f"Number of customers: {customers_count}")
                
                # Check orders table
                result = conn.execute(text("SELECT COUNT(*) FROM orders"))
                orders_count = result.scalar()
                print(f"Number of orders: {orders_count}")
                
                # Check date range in orders, filtering out invalid dates
                result = conn.execute(text("""
                    SELECT MIN(created_at) as min_date, MAX(created_at) as max_date 
                    FROM orders
                    WHERE created_at IS NOT NULL
                """))
                min_date, max_date = result.first()
                print(f"Order date range: {min_date} to {max_date}")
                
                return customers_count, orders_count, min_date, max_date
                
        except Exception as e:
            print(f"Error testing data: {e}")
            return 0, 0, None, None
        
