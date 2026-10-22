import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
    
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_NAME = os.getenv('DB_NAME', 'test')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_PORT = int(os.getenv('DB_PORT', 3306))
    
    DB_POOL_MIN_CACHED = int(os.getenv('DB_POOL_MIN_CACHED', 2))
    DB_POOL_MAX_CONNECTIONS = int(os.getenv('DB_POOL_MAX_CONNECTIONS', 10))
    
    DEBUG = os.getenv('FLASK_ENV') == 'development'