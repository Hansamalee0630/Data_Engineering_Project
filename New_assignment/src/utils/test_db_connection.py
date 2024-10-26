from database_utils import DatabaseConnection

def test_db_connection():
    db = DatabaseConnection()
    engine = db.connect()
    if engine:
        print("Connection successful!")
        customers_count, orders_count, min_date, max_date = db.test_data_exists()
        print(f"Number of customers: {customers_count}")
        print(f"Number of orders: {orders_count}")
        print(f"Order date range: {min_date} to {max_date}")
    else:
        print("Connection failed!")

if __name__ == "__main__":
    test_db_connection()