import os

from dotenv import load_dotenv

load_dotenv()

APP_NAME = os.environ.get("APP_NAME", "Certificate Manager")
DB_USER = os.environ.get("DB_USER", "certificate_manager")
DB_HOST = os.environ.get("DB_HOST", "db")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "password")
DB_NAME = os.environ.get("DB_NAME", "certificate_manager")
DB_PORT = os.environ.get("DB_PORT", "5432")
