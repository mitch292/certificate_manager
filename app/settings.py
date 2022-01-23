import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = os.environ.get('APP_NAME', 'Certificate Manager')
# NOTE: the below database values are used in create_database.sh, if you'd like to use other values
# that file will need to be updated
DB_USER = os.environ.get('DB_USER', 'certificate_manager')
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'password')
DB_NAME = os.environ.get('DB_NAME', 'certificate_manager')
DB_PORT = os.environ.get('DB_PORT', '5432')