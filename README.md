# Delivergate Customer Orders App
# Customer Orders Dashboard
<img src="app View.png">

This is a Streamlit dashboard application that analyzes customer order data from a MySQL database.

## Directory Structure
```
NEW_ASSIGNMENT/
├── .conda/
├── .streamlit/
├── config/
│   └── config.py
├── data/
│   ├── processed/
│       ├── customers_cleaned.csv
│       └── orders_cleaned.csv
│   └── raw/
│       ├── customers.csv
│       └── order.csv
├── notebooks/
│   └── model.ipynb
├── src/
│   └── app/
│       ├── database_utils.py
│       ├── import_data.py
│       ├── ml_utils.py
│       └── test_db_connection.py
├── .env
├── .gitignore
├── README.md
└── requirements.txt
```

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

5. Set up environment variables:
Create a `.env` file in the root directory with the following configuration:
```
DB_HOST=localhost
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=your_database
```

6. Run config file:
```python
python config/config.py
```

7. Import initial data:
```python
python src/app/import_data.py
```

8.Run database_utils file:
```python
python src/utils/database_utils.py
```

9. Check if the DB connection established or not:
```python
python src/utils/test_db_cennection.py
```

10. Run the Streamlit app:
```bash
streamlit run src/app/streamlit_app.py
```

## Features
- Date range filtering for orders
- Minimum spend and order count filters
- Top 10 customers visualization
- Revenue over time analysis
- Summary metrics
- Detailed order data table

## Machine Learning Model
The application includes a logistic regression model that predicts whether a customer is likely to be a repeat purchaser based on their order history and spending patterns.

## Project Components
- `src/app/streamlit_app.py`: Main Streamlit application
- `src/app/database_utils.py`: Database connection and query utilities
- `src/app/ml_utils.py`: Machine learning model implementation
- `src/app/import_data.py`: Data import utilities
- `src/app/test_db_connection.py`: Database connection testing
- `config/config.py`: Configuration settings
- `notebooks/model.ipynb`: Data analysis and LR model include notebook
- `requirements.txt`: Required Python packages
- `.env`: Environment variables (not tracked in git)

## Development
- Use the `notebooks/model.ipynb` for data analysis and feature development
- Run tests using: `python -m pytest tests/`
- Update requirements using: `pip freeze > requirements.txt`

## Note
- Make sure to properly secure your database credentials using the `.env` file
- Never commit sensitive information to the repository
- For development, use the provided test database connection utility
- Check logs directory for any error messages during data import

## Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request
