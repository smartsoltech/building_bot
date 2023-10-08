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

# Строка подключения к БД в зависимости от типа
if DB_TYPE == "sqlite":
    DATABASE_URL = f"sqlite:///{DB_NAME}.db"
elif DB_TYPE == "mysql":
    DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
elif DB_TYPE == "pgsql":
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
elif DB_TYPE == "mariadb":
    DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
else:
    raise ValueError("Unsupported DB_TYPE value in .env file")
