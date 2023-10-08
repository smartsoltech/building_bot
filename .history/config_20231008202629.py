import os

TOKEN = os.getenv(TG_TOKEN)
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///your_database_name.db')