import db_functions
import telebot
import schedule
import time
import xml.etree.ElementTree as ElemTree

import requests
import telebot
import db_functions
from related_info import zodiac_signs
from thread_safe_dict import ThreadSafeDict

safe_daily_horoscopes = ThreadSafeDict()

TOKEN = '5717083963:AAHflxPNEMzSklg_hc5Snbs24MQv4aaUyNU'
url = "https://ignio.com/r/export/win/xml/daily/com.xml"
bot = telebot.TeleBot(TOKEN, parse_mode=None)

def update_daily_horoscope():
    response = requests.get(url)
    xml_content = response.content

    root = ElemTree.fromstring(xml_content)

    for sign in list(root):
        sign_name = sign.tag
        if sign_name != 'date':
            safe_daily_horoscopes.set(sign_name.capitalize(), sign.find('today').text)



def job1():
    update_daily_horoscope()
    users = db_functions.get_susubscription()
    for user in users:
        bot.send_photo(user[0], photo=open('photos/zodiac_horoscope.jpg', 'rb'))
        horoscope_message = f'*Гороскоп:* {safe_daily_horoscopes.get(zodiac_signs[user[1]])}\n*Знак зодиака:* {user[1]}'
        print(safe_daily_horoscopes.get(zodiac_signs[user[1]]))
        bot.send_message(user[0], "Вот ваш ежедневный гороскоп!")
        bot.send_message(user[0], horoscope_message, parse_mode="Markdown")

        

schedule.every().day.at("12:00", "Europe/Moscow").do(job1)

while True:
    schedule.run_pending()
    time.sleep(10)

