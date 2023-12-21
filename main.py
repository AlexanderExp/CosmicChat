import threading
import time
import xml.etree.ElementTree as ElemTree

import requests
import telebot
from bs4 import BeautifulSoup, NavigableString

import comp_func
import db_functions
import message_handler
from menus import create_main_menu_markup
from related_info import zodiac_signs, zodiac_compatibility, chinese_zodiac_animals
from thread_safe_dict import ThreadSafeDict

TOKEN = '5717083963:AAHflxPNEMzSklg_hc5Snbs24MQv4aaUyNU'
url = "https://ignio.com/r/export/win/xml/daily/com.xml"

user_data = {}

safe_daily_horoscopes = ThreadSafeDict()

db_functions.create_database()


def update_daily_horoscope():
    response = requests.get(url)
    xml_content = response.content

    root = ElemTree.fromstring(xml_content)

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
    bot.send_photo(message.chat.id, photo=open('photos/zodiac_horoscope.jpg', 'rb'))
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


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    state = db_functions.check_user(message.from_user.id)
    if state is None or state[0] == 'false':
        db_functions.register_user(message.from_user.id, state)
        bot.send_photo(message.chat.id, photo=open('photos/welcome.jpg', 'rb'))
        bot.reply_to(message,
                     "🔮 Добро пожаловать в бота-гороскоп! 🔮\nПожалуйста, введите вашу дату рождения в формате ДД.ММ.ГГГГ.")
    else:
        bot.send_message(message.chat.id, "Выберите действие", reply_markup=create_main_menu_markup())


@bot.message_handler(func=lambda message: True)
def check_message(message):
    message_handler.handle_message(message, bot)


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
