from telebot import types
from models import SessionLocal
from models.worker import Worker

class WorkerRegistration:
    def __init__(self):
        self.full_name = None
        self.birth_date = None
        self.citizenship = None
        self.visa = None
        self.certificate = None
        self.phone = None
        self.address = None
        self.id_card_photos = []
        self.certificate_photo = None

active_registrations = {}

def start_registration(bot, message):
    registration = WorkerRegistration()
    active_registrations[message.chat.id] = registration
    bot.send_message(message.chat.id, "Введите вашу фамилию и имя:")

def handle_registration(bot, message):
    session = SessionLocal()
    registration = active_registrations[message.chat.id]

    if not registration.full_name:
        registration.full_name = message.text
        bot.send_message(message.chat.id, "Введите вашу дату рождения (дд.мм.гггг):")
    elif not registration.birth_date:
        registration.birth_date = message.text
        bot.send_message(message.chat.id, "Введите ваше гражданство:")
    elif not registration.citizenship:
        registration.citizenship = message.text
        bot.send_message(message.chat.id, "У вас есть виза? (да/нет):")
    elif not registration.visa:
        registration.visa = message.text
        bot.send_message(message.chat.id, "У вас есть сертификат об обучении? (да/нет):")
    elif not registration.certificate:
        registration.certificate = message.text
        bot.send_message(message.chat.id, "Введите ваш номер телефона:")
    elif not registration.phone:
        registration.phone = message.text
        bot.send_message(message.chat.id, "Введите ваш адрес проживания:")
    elif not registration.address:
        registration.address = message.text
        markup = types.ReplyKeyboardMarkup(row_width=1)
        itembtn1 = types.KeyboardButton('Отправить фото айди-карты')
        markup.add(itembtn1)
        bot.send_message(message.chat.id, "Отправьте фото вашей айди-карты с обеих сторон:", reply_markup=markup)
    elif not registration.id_card_photos:
        if message.photo:
            registration.id_card_photos.append(message.photo[-1].file_id)
            if len(registration.id_card_photos) == 1:
                bot.send_message(message.chat.id, "Отправьте фото с другой стороны айди-карты:")
            else:
                markup = types.ReplyKeyboardMarkup(row_width=1)
                itembtn1 = types.KeyboardButton('Отправить фото сертификата')
                markup.add(itembtn1)
                bot.send_message(message.chat.id, "Отправьте фото вашего сертификата об обучении:", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "Пожалуйста, отправьте фото.")
    elif not registration.certificate_photo:
        if message.photo:
            registration.certificate_photo = message.photo[-1].file_id
            new_worker = Worker(
                user_id=message.from_user.id,
                chat_id=message.chat.id,
                full_name=registration.full_name,
                birth_date=registration.birth_date,
                citizenship=registration.citizenship,
                visa=True if registration.visa.lower() == 'да' else False,
                certificate=True if registration.certificate.lower() == 'да' else False,
                phone=registration.phone,
                address=registration.address,
                id_card_photo_front=registration.id_card_photos[0],
                id_card_photo_back=registration.id_card_photos[1] if len(registration.id_card_photos) > 1 else None,
                certificate_photo=registration.certificate_photo
            )
            session.add(new_worker)
            session.commit()
            session.close()
            del active_registrations[message.chat.id]
            markup = types.ReplyKeyboardRemove()
            bot.send_message(message.chat.id, "Регистрация завершена! Спасибо!", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "Пожалуйста, отправьте фото.")
