import telebot
from telebot import types
import datetime
import re
import db_functions

TOKEN = '5717083963:AAHflxPNEMzSklg_hc5Snbs24MQv4aaUyNU'
db_functions.create_database()


bot = telebot.TeleBot(TOKEN, parse_mode=None)

def create_main_menu_markup():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    itembtn1 = types.KeyboardButton('Мой гороскоп на сегодня')
    itembtn2 = types.KeyboardButton('Гороскоп на сегодня (выбрать зодиак)')
    itembtn3 = types.KeyboardButton('Китайский гороскоп')
    itembtn4 = types.KeyboardButton('Совместимость')
    itembtn5 = types.KeyboardButton('Натальная карта')
    itembtn6 = types.KeyboardButton('HSE Special: Какая ворона ты сегодня?')
    itembtn7 = types.KeyboardButton('Мотивашка дня')
    itembtn8 = types.KeyboardButton('Отписаться / подписаться на ежедневный гороскоп')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6, itembtn7, itembtn8)
    return markup

def create_menu_yes_no():
    btn_yes = types.InlineKeyboardButton('Да', callback_data='да')
    btn_no = types.InlineKeyboardButton('Нет', callback_data='нет')
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(btn_yes)
    keyboard.add(btn_no)
    return keyboard

def create_zodiac_menu():
    aries = types.InlineKeyboardButton('Овен', callback_data='овен')
    taurus = types.InlineKeyboardButton('Телец', callback_data='телец')
    gemini = types.InlineKeyboardButton('Близнецы', callback_data='близнецы')
    crayfish = types.InlineKeyboardButton('Рак', callback_data='рак')
    leo = types.InlineKeyboardButton('Лев', callback_data='лев')
    virgo = types.InlineKeyboardButton('Дева', callback_data='дева')
    libra = types.InlineKeyboardButton('Весы', callback_data='весы')
    scorpio = types.InlineKeyboardButton('Скорпион', callback_data='скорпион')
    sagittarius = types.InlineKeyboardButton('Стрелец', callback_data='стрелец')
    capricorn = types.InlineKeyboardButton('Козерог', callback_data='козерог')
    aquarius = types.InlineKeyboardButton('Водолей', callback_data='водолей')
    pisces = types.InlineKeyboardButton('Рыбы', callback_data='рыбы')

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(aries, taurus, gemini, crayfish, leo, virgo, libra, scorpio, sagittarius, capricorn, aquarius, pisces)
    return keyboard

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    state = db_functions.check_user(message.from_user.id)
    if state is None or state[0] == 'false':
        db_functions.register_user(message.from_user.id, state)
        bot.reply_to(message, "Добро пожаловать в бота-гороскоп! Пожалуйста, введите вашу дату рождения в формате ДД.ММ.ГГГГ.")
    else:
        bot.send_message(message.chat.id, "Выберите действие", reply_markup=create_main_menu_markup())

@bot.message_handler(func=lambda message: True)
def check_message(message):
    state = db_functions.check_user(message.from_user.id)
    if state is None:
        db_functions.register_user(message.from_user.id, state)
        bot.reply_to(message, "Добро пожаловать в бота-гороскоп! Пожалуйста, введите вашу дату рождения в формате ДД.ММ.ГГГГ.")
    elif state[0] == 'false':
        date_text = message.text
        if re.match(r'\d{2}\.\d{2}\.\d{4}', date_text):
            try:
                birth_date = datetime.datetime.strptime(date_text, '%d.%m.%Y')
                db_functions.set_birthday(birth_date, message.from_user.id)
                bot.reply_to(message, "Вы успешно зарегистрированы!")
                bot.send_message(message.chat.id, "Хотите получать ежедневный астрологический прогноз?", 
                                 reply_markup=create_menu_yes_no())
            except:
                bot.reply_to(message, "Неверный формат даты. Пожалуйста, введите дату в формате ДД.ММ.ГГГГ.")
        elif(message.text == "Мой гороскоп на сегодня"):
            bot.send_message(message.chat.id, "Test")
        else:
            bot.reply_to(message, "Неверный формат даты. Пожалуйста, введите дату в формате ДД.ММ.ГГГГ.")
    else:
        bot.send_message(message.chat.id, 'Класс', reply_markup=create_main_menu_markup())


# Функция callback_query_handler вносится один раз для обработки всех событий
@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    if call.data == 'да':
        db_functions.set_subscription(1, call.from_user.id)
        bot.send_message(call.message.chat.id, "Принято! Ждите гороскопы)", reply_markup=create_main_menu_markup())
    elif call.data == 'нет':
        db_functions.set_subscription(0, call.from_user.id)
        bot.send_message(call.message.chat.id, "Окей, не буду беспокоить)", reply_markup=create_main_menu_markup())
    elif call.data == 'гороскоп на сегодня':
        bot.send_message(call.message.chat.id, "Пока не знаю")

@bot.message_handler(func=lambda message: message.text == "Мой гороскоп на сегодня")
def button1(message):
    bot.send_message(message.chat.id, "U select bottom 1")

bot.infinity_polling()