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
    chat_id = message.chat.id
    user_id = message.from_user.id

    if (user_id, chat_id) in active_registrations:
        bot.send_message(chat_id, "Вы уже начали регистрацию. Пожалуйста, завершите ее или начните заново.")
        return

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    itembtn1 = types.KeyboardButton('Начать регистрацию')
    markup.add(itembtn1)
    msg = bot.send_message(chat_id, "Добро пожаловать в процесс регистрации!", reply_markup=markup)
    bot.register_next_step_handler(msg, handle_registration)

    active_registrations[(user_id, chat_id)] = {
        'stage': 'full_name',
        'data': {}
    }

def handle_registration(message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if (user_id, chat_id) not in active_registrations:
        return

    registration = active_registrations[(user_id, chat_id)]

    if registration['stage'] == 'full_name':
        registration['data']['full_name'] = message.text
        bot.send_message(chat_id, "Введите вашу дату рождения в формате ДД.ММ.ГГГГ:")
        registration['stage'] = 'birthdate'

    elif registration['stage'] == 'birthdate':
        registration['data']['birthdate'] = message.text
        bot.send_message(chat_id, "Введите ваше гражданство:")
        registration['stage'] = 'citizenship'

    elif registration['stage'] == 'citizenship':
        registration['data']['citizenship'] = message.text
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=3)
        itembtns = [types.KeyboardButton(v) for v in ["F4", "H2", "G1", "E7", "E9", "D2", "нет"]]
        markup.add(*itembtns)
        msg = bot.send_message(chat_id, "Выберите тип вашей визы:", reply_markup=markup)
        bot.register_next_step_handler(msg, handle_registration)
        registration['stage'] = 'visa_type'

    elif registration['stage'] == 'visa_type':
        registration['data']['visa_type'] = message.text
        bot.send_message(chat_id, "У вас есть сертификат об обучении? (да/нет):")
        registration['stage'] = 'certificate'

    elif registration['stage'] == 'certificate':
        registration['data']['certificate'] = message.text
        bot.send_message(chat_id, "Введите ваш номер телефона:")
        registration['stage'] = 'phone'

    elif registration['stage'] == 'phone':
        registration['data']['phone'] = message.text
        bot.send_message(chat_id, "Введите ваш адрес проживания:")
        registration['stage'] = 'address'

    elif registration['stage'] == 'address':
        registration['data']['address'] = message.text
        bot.send_message(chat_id, "Пожалуйста, отправьте 3 фотографии в одном сообщении: фото айди-карты с обеих сторон и фото сертификата.")
        registration['stage'] = 'photo_id'

    elif registration['stage'] == 'photo_id':
        if message.media_group_id:  # Если это медиа-группа
            photos = message.photo
            if len(photos) != 3:
                bot.send_message(chat_id, "Пожалуйста, отправьте ровно 3 фотографии в одном сообщении.")
                return

            registration['data']['photo_id_front'] = photos[0].file_id
            registration['data']['photo_id_back'] = photos[1].file_id
            registration['data']['photo_certificate'] = photos[2].file_id

            # Переход к следующему этапу
            registration['stage'] = 'completed'
            bot.send_message(chat_id, "Регистрация завершена!")
            save_registration_to_db(registration)
            del active_registrations[(user_id, chat_id)]
        else:
            bot.send_message(chat_id, "Пожалуйста, отправьте 3 фотографии в одном сообщении.")

def save_registration_to_db(registration):
    db = SessionLocal()
    new_worker = Worker(
        full_name=registration['data']['full_name'],
        birthdate=registration['data']['birthdate'],
        citizenship=registration['data']['citizenship'],
        visa_type=registration['data']['visa_type'],
        certificate=registration['data']['certificate'],
        phone=registration['data']['phone'],
        address=registration['data']['address'],
        photo_id_front=registration['data']['photo_id_front'],
        photo_id_back=registration['data']['photo_id_back'],
        photo_certificate=registration['data']['photo_certificate']
    )
    db.add(new_worker)
    db.commit()
    db.close()