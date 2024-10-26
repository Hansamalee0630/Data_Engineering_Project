# Delivergate Customer Orders App

# Customer Orders Dashboard
<img src="app View.png">
This is a Streamlit dashboard application that analyzes customer order data from a MySQL database.

## Setup Instructions

1. Clone this repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Create a MySQL database and tables:
```sql
CREATE DATABASE your_database;
USE your_database;

CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(255)
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    total_amount DECIMAL(10, 2),
    order_date DATE,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
```

5. Update the database connection details in `database_utils.py`:
```python
host="localhost"
user="your_username"
password="your_password"
database="your_database"
```

6. Import initial data (if using CSV files):
```python
from database_utils import DatabaseConnection

db = DatabaseConnection()
db.connect()
db.import_csv_data('customer.csv', 'orders.csv')
```

7. Run the Streamlit app:
```bash
streamlit run streamlit_app.py
```

## Features

- Date range filtering for orders
- Minimum spend and order count filters
- Top 10 customers visualization
- Revenue over time analysis
- Customer repeat purchase prediction
- Summary metrics
- Detailed order data table

## Machine Learning Model

The application includes a logistic regression model that predicts whether a customer is likely to be a repeat purchaser based on their order history and spending patterns.

## Files Structure

- `streamlit_app.py`: Main Streamlit application
- `database_utils.py`: Database connection and query utilities
- `ml_utils.py`: Machine learning model implementation
- `requirements.txt`: Required Python packages
- `README.md`: This file

## Note

Make sure to properly secure your database credentials in a production environment. Consider using environment variables or a secure configuration management system.
