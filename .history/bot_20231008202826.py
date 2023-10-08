import telebot
from config import TOKEN
from models import SessionLocal, Worker, Brigade, Profile, Object

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Добро пожаловать в бота!")

# Добавьте здесь другие обработчики сообщений...

if __name__ == "__main__":
    bot.polling(none_stop=True)
