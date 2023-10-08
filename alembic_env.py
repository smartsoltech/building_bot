import os
from dotenv import load_dotenv
import os
from alembic import command
from alembic.config import Config

# Загрузка переменных окружения из файла .env
load_dotenv()

# Получение параметров подключения из переменных окружения
DB_TYPE = os.getenv("DB_TYPE")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Формирование строки соединения
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


def migrate():
    # Set up the configuration
    alembic_cfg = Config(os.path.join(os.path.dirname(__file__), "alembic.ini"))
    
    # Generate the migration
    command.revision(alembic_cfg, autogenerate=True, message="Auto-generated migration")
    
    # Apply the migration
    command.upgrade(alembic_cfg, "head")

# Call the function to perform the migration
migrate()