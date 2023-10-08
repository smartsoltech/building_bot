import telebot
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from models import Base, SessionLocal
from models.worker import Worker
from models.brigade import Brigade
from models.profile import Profile
from models.object import Object
from config import TOKEN, DATABASE_URL
from register import start_registration, handle_registration, active_registrations

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Добро пожаловать в бота!")

# Добавьте здесь другие обработчики сообщений...

def setup_database():
    engine = create_engine(DATABASE_URL)
    try:
        # Попробуем подключиться к базе данных
        connection = engine.connect()
        connection.close()
        print("Successfully connected to the existing database!")
    except OperationalError:
        # Если подключение не удалось, создаем новую базу данных
        Base.metadata.create_all(bind=engine)
        print("Database not found. A new database has been created!")

if __name__ == "__main__":
    setup_database()
    bot.polling(none_stop=True)
