import telebot
from telebot import types
import datetime
import re
import db_functions
import horoscope_func
import hse_spec_func

TOKEN = '5717083963:AAHflxPNEMzSklg_hc5Snbs24MQv4aaUyNU'
db_functions.create_database()


bot = telebot.TeleBot(TOKEN, parse_mode=None)

def fetch_horoscope(message, sign):
    horoscope = horoscope_func.get_daily_horoscope(sign)
    data = horoscope["data"]
    horoscope_message = f'*Horoscope:* {data["horoscope_data"]}\\n*Sign:* {sign}'
    bot.send_message(message.chat.id, "Here's your horoscope!")
    bot.send_message(message.chat.id, horoscope_message, parse_mode="Markdown")

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

def create_chineese_menu():
    rat = types.InlineKeyboardButton('Крыса', callback_data='Крыса')
    bull = types.InlineKeyboardButton('Бык', callback_data='Бык')
    tiger = types.InlineKeyboardButton('Тигр', callback_data='Тигр')
    rabbit = types.InlineKeyboardButton('Кролик', callback_data='Кролик')
    dragon = types.InlineKeyboardButton('Дракон', callback_data='Дракон')
    snake = types.InlineKeyboardButton('Змея', callback_data='Змея')
    horse = types.InlineKeyboardButton('Лошадь', callback_data='Лошадь')
    sheep = types.InlineKeyboardButton('Овца', callback_data='Овца')
    monkey = types.InlineKeyboardButton('Обезьяна', callback_data='Обезьяна')
    chicken = types.InlineKeyboardButton('Курица', callback_data='Курица')
    dog = types.InlineKeyboardButton('Собака', callback_data='Собака')
    pig = types.InlineKeyboardButton('Свинья', callback_data='Свинья')

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(rat, bull, tiger, rabbit, dragon, snake, horse, sheep, monkey, chicken, dog, pig)
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
        else:
            bot.reply_to(message, "Неверный формат даты. Пожалуйста, введите дату в формате ДД.ММ.ГГГГ.")
    else:
        if(message.text == "Мой гороскоп на сегодня"):
            sign = db_functions.get_sign(message.from_user.id)
            fetch_horoscope(message.from_user.id, sign)
            bot.send_message(message.chat.id, "Пока не знаю")

        elif(message.text == "Гороскоп на сегодня (выбрать зодиак)"):
            bot.send_message(message.chat.id, "Выберите знак зодиака:", reply_markup=create_zodiac_menu())

        elif(message.text == "Китайский гороскоп"):
            bot.send_message(message.chat.id, "Выберите животное:", reply_markup=create_chineese_menu())

        elif(message.text == "Совместимость"):
            bot.send_message(message.chat.id, "Пока не знаю")

        elif(message.text == "Натальная карта"):
            bot.send_message(message.chat.id, "Пока не знаю")

        elif(message.text == "HSE Special: Какая ворона ты сегодня?"):
            bot.send_message(message.chat.id, hse_spec_func.random_crow())

        elif(message.text == "Мотивашка дня"):
            bot.send_message(message.chat.id, hse_spec_func.random_motivation())

        elif(message.text == "Отписаться / подписаться на ежедневный гороскоп"):
            b = db_functions.change_subscription(message.from_user.id)
            if (b == (1,)):
                bot.send_message(message.chat.id, "Done! Вы отписались от ежедневной рассылки")
            else:
                bot.send_message(message.chat.id, "Готово! Вы подписались на ежедневную рассылку гороскопа")

        elif re.match(r'\d{2}\.\d{2}\.\d{4}', message.text):
            bot.send_message(message.chat.id, "Похоже вы пытаетесь ввести дату, но я уже знаю ваш День Рождения ^ - ^")

        else:
            bot.send_message(message.chat.id, 'Ой! Я вас не понял :(', reply_markup=create_main_menu_markup())



# Функция callback_query_handler вносится один раз для обработки всех событий
@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    if call.data == 'да':
        db_functions.set_subscription(1, call.from_user.id)
        bot.send_message(call.message.chat.id, "Принято! Ждите гороскопы)", reply_markup=create_main_menu_markup())
    elif call.data == 'нет':
        db_functions.set_subscription(0, call.from_user.id)
        bot.send_message(call.message.chat.id, "Окей, не буду беспокоить)", reply_markup=create_main_menu_markup())



bot.infinity_polling()