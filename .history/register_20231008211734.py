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

from models import Worker, SessionLocal

def handle_registration(bot, message):
    registration = active_registrations[message.chat.id]

    if not registration.full_name:
        registration.full_name = message.text
        bot.send_message(message.chat.id, "Введите вашу дату рождения (например, 01.01.2000):")

    elif not registration.birth_date:
        registration.birth_date = message.text
        bot.send_message(message.chat.id, "Введите ваше гражданство:")

    elif not registration.citizenship:
        registration.citizenship = message.text
        markup = types.ReplyKeyboardMarkup(row_width=3)
        visa_types = ['F4', 'H2', 'G1', 'E7', 'E9', 'D2', 'нет']
        for visa_type in visa_types:
            markup.add(types.KeyboardButton(visa_type))
        bot.send_message(message.chat.id, "Выберите ваш тип визы:", reply_markup=markup)

    elif not registration.visa:
        if message.text in ['F4', 'H2', 'G1', 'E7', 'E9', 'D2', 'нет']:
            registration.visa = message.text
            bot.send_message(message.chat.id, "У вас есть сертификат об обучении? (Да/Нет):")
        else:
            bot.send_message(message.chat.id, "Пожалуйста, выберите тип визы из предложенных вариантов.")

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
                bot.send_message(message.chat.id, "Теперь отправьте фото вашего сертификата об обучении:", reply_markup=markup)
        elif message.text == 'Отправить фото айди-карты':
            bot.send_message(message.chat.id, "Пожалуйста, отправьте фото вашей айди-карты с обеих сторон.")
        else:
            bot.send_message(message.chat.id, "Пожалуйста, отправьте фото.")

    elif not registration.certificate_photo:
        if message.photo:
            registration.certificate_photo = message.photo[-1].file_id

            # Сохранение данных в базе данных
            db = SessionLocal()
            worker = Worker(
                full_name=registration.full_name,
                birth_date=registration.birth_date,
                citizenship=registration.citizenship,
                visa=registration.visa,
                certificate=registration.certificate,
                phone=registration.phone,
                address=registration.address,
                id_card_photos=','.join(registration.id_card_photos),
                certificate_photo=registration.certificate_photo,
                user_id=message.from_user.id,
                chat_id=message.chat.id
            )
            db.add(worker)
            db.commit()
            db.close()

            del active_registrations[message.chat.id]
            markup = types.ReplyKeyboardRemove()
            bot.send_message(message.chat.id, "Регистрация завершена! Спасибо!", reply_markup=markup)
        elif message.text == 'Отправить фото сертификата':
            bot.send_message(message.chat.id, "Пожалуйста, отправьте фото вашего сертификата об обучении.")
        else:
            bot.send_message(message.chat.id, "Пожалуйста, отправьте фото.")

