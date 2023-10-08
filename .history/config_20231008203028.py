import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Параметры подключения к БД
DB_TYPE = os.getenv('DB_TYPE', 'sqlite')  # Тип БД: sqlite, mysql, pgsql, mariadb
DB_HOST = os.getenv('DB_HOST', 'localhost')  # Адрес сервера БД
DB_PORT = os.getenv('DB_PORT', '3306')  # Порт сервера БД
DB_NAME = os.getenv('DB_NAME', 'your_database_name')  # Название БД
DB_USER = os.getenv('DB_USER', 'root')  # Имя пользователя БД
DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')  # Пароль пользователя БД

# Строка подключения к БД
DATABASE_URL = f"{DB_TYPE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
