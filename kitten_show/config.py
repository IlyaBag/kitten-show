import os

from dotenv import load_dotenv


load_dotenv()

DB_ECHO = os.getenv('DB_ECHO', '').lower() in ('true', 'yes', 'y', '1')

DB_USER = os.getenv('POSTGRES_USER')
DB_PASS = os.getenv('POSTGRES_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
