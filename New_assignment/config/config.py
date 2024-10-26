import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Debug prints to verify environment variables
print("DB_HOST:", os.getenv('DB_HOST'))
print("DB_USER:", os.getenv('DB_USER'))
print("DB_PASSWORD:", os.getenv('DB_PASSWORD'))
print("DB_DATABASE:", os.getenv('DB_DATABASE'))

# Database configurations
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_DATABASE')
}

# Application configurations
APP_CONFIG = {
    'debug': os.getenv('DEBUG', 'False') == 'True',
    'port': int(os.getenv('PORT', 8501)),
    'log_level': os.getenv('LOG_LEVEL', 'INFO')
}

# Machine Learning configurations
ML_CONFIG = {
    'min_training_samples': 50,
    'test_size': 0.2,
    'random_state': 42
}

# Path configurations
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, 'processed')
LOG_DIR = os.path.join(BASE_DIR, 'logs')

# Create directories if they don't exist
for directory in [DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, LOG_DIR]:
    os.makedirs(directory, exist_ok=True)