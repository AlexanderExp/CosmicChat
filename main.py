import telebot
from telebot import types
import datetime
import re
import db_functions
import comp_func
import hse_spec_func
from thread_safe_dict import ThreadSafeDict
import schedule
import requests
import xml.etree.ElementTree as ET
import time
import threading
from bs4 import BeautifulSoup, NavigableString



TOKEN = '5717083963:AAHflxPNEMzSklg_hc5Snbs24MQv4aaUyNU'
url = "https://ignio.com/r/export/win/xml/daily/com.xml"

zodiac_signs = {
    "Овен": "Aries",
    "Телец": "Taurus",
    "Близнецы": "Gemini",
    "Рак": "Cancer",
    "Лев": "Leo",
    "Дева": "Virgo",
    "Весы": "Libra",
    "Скорпион": "Scorpio",
    "Стрелец": "Sagittarius",
    "Козерог": "Capricorn",
    "Водолей": "Aquarius",
    "Рыбы": "Pisces"
}

zodiac_compatibility = ["Овен2","Телец2","Близнецы2","Рак2","Лев2","Дева2","Весы2","Скорпион2","Стрелец2","Козерог2","Водолей2","Рыбы2"]

chinese_zodiac_animals = {
    "Крыса": "https://vashzodiak.ru/kitaiskii-prognoz/krysa/",
    "Бык": "https://vashzodiak.ru/kitaiskii-prognoz/byk/",
    "Тигр": "https://vashzodiak.ru/kitaiskii-prognoz/tigr/",
    "Кролик": "https://vashzodiak.ru/kitaiskii-prognoz/krolik/",
    "Дракон": "https://vashzodiak.ru/kitaiskii-prognoz/drakon/",
    "Змея": "https://vashzodiak.ru/kitaiskii-prognoz/zmeya/",
    "Лошадь": "https://vashzodiak.ru/kitaiskii-prognoz/loshad/",
    "Овца": "https://vashzodiak.ru/kitaiskii-prognoz/koza/",
    "Обезьяна": "https://vashzodiak.ru/kitaiskii-prognoz/obezyana/",
    "Курица": "https://vashzodiak.ru/kitaiskii-prognoz/petuh/",
    "Собака": "https://vashzodiak.ru/kitaiskii-prognoz/sobaka/",
    "Свинья": "https://vashzodiak.ru/kitaiskii-prognoz/kaban/"
}

safe_daily_horoscopes = ThreadSafeDict()

db_functions.create_database()

def update_daily_horoscope():
    response = requests.get(url)
    xml_content = response.content

    root = ET.fromstring(xml_content)

    for sign in list(root):
        sign_name = sign.tag
        if sign_name != 'date':
            safe_daily_horoscopes.set(sign_name.capitalize(), sign.find('today').text)

def run_bot():
    bot.infinity_polling()


# schedule.every().day.at("01:00").do(update_daily_horoscope)

def run_schedule():
    while True:
        # schedule.run_pending()
        update_daily_horoscope()
        time.sleep(100)

bot = telebot.TeleBot(TOKEN, parse_mode=None)

def fetch_horoscope(message, sign):
    horoscope_message = f'*Гороскоп:* {safe_daily_horoscopes.get(zodiac_signs[sign])}\n*Знак зодиака:* {sign}'
    bot.send_message(message.chat.id, "Вот ваш гороскоп!")
    bot.send_message(message.chat.id, horoscope_message, parse_mode="Markdown")

def fetch_chinese_horoscope(message, animal):
    response = requests.get(chinese_zodiac_animals[animal])
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    div = soup.find('div', class_='col-md-8')
    text_nodes = [element for element in div.contents if isinstance(element, NavigableString)]
    bot.send_message(message.chat.id, "Вот ваш гороскоп!")
    horoscope_message = f'*Китайский гороскоп:* {text_nodes[1]}\n*Китайское животное:* {animal}'
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

def create_zodiac_menu2():
    aries = types.InlineKeyboardButton('Овен', callback_data='Овен2')
    taurus = types.InlineKeyboardButton('Телец', callback_data='Телец2')
    gemini = types.InlineKeyboardButton('Близнецы', callback_data='Близнецы2')
    crayfish = types.InlineKeyboardButton('Рак', callback_data='Рак2')
    leo = types.InlineKeyboardButton('Лев', callback_data='Лев2')
    virgo = types.InlineKeyboardButton('Дева', callback_data='Дева2')
    libra = types.InlineKeyboardButton('Весы', callback_data='Весы2')
    scorpio = types.InlineKeyboardButton('Скорпион', callback_data='Скорпион2')
    sagittarius = types.InlineKeyboardButton('Стрелец', callback_data='Стрелец2')
    capricorn = types.InlineKeyboardButton('Козерог', callback_data='Козерог2')
    aquarius = types.InlineKeyboardButton('Водолей', callback_data='Водолей2')
    pisces = types.InlineKeyboardButton('Рыбы', callback_data='Рыбы2')

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
            fetch_horoscope(message, sign)

        elif(message.text == "Гороскоп на сегодня (выбрать зодиак)"):
            bot.send_message(message.chat.id, "Выберите знак зодиака:", reply_markup=create_zodiac_menu())

        elif(message.text == "Китайский гороскоп"):
            bot.send_message(message.chat.id, "Выберите животное:", reply_markup=create_chineese_menu())

        elif(message.text == "Совместимость"):
            bot.send_message(message.chat.id, "Выберите знак зодиака, про который Вы хотите узнать:", reply_markup=create_zodiac_menu2())

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
    elif call.data.capitalize() in zodiac_signs:
        fetch_horoscope(call.message, call.data.capitalize())
    elif call.data.capitalize() in chinese_zodiac_animals:
        fetch_chinese_horoscope(call.message, call.data.capitalize())
    elif call.data in zodiac_compatibility:
        comp = comp_func.find_comp(call.data)
        bot.send_message(call.message.chat.id, comp, reply_markup=create_main_menu_markup())


if __name__ == "__main__":
    bot_thread = threading.Thread(target=run_bot)
    schedule_thread = threading.Thread(target=run_schedule)

    bot_thread.start()
    schedule_thread.start()