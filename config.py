import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MySQL config dictionary
db_config = {
    'host': os.getenv('MYSQL_HOST'),
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'database': os.getenv('MYSQL_DB')
}
