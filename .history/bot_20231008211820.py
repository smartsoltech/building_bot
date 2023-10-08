import telebot
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from models import Worker, SessionLocal
from models import Base, SessionLocal
from models.worker import Worker
from models.brigade import Brigade
from models.profile import Profile
from models.object import Object
from config import TOKEN, DATABASE_URL
from register import start_registration, handle_registration, active_registrations

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['register'])
def register_command(message):
    start_registration(bot, message)

@bot.message_handler(func=lambda message: message.chat.id in active_registrations)
def registration_handler(message):
    handle_registration(bot, message)
                        
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Добро пожаловать в бота!")

# @bot.message_handler(content_types=['TEXT'])
# def register_command(message):
#     if message.text.lower() == 'register':
#         start_registration(bot, message)

# @bot.message_handler(func=lambda message: message.chat.id in active_registrations)
# def registration_handler(message):
#     handle_registration(bot, message)
    
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
