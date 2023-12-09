import os
from datetime import datetime

import cairosvg as cairosvg
from kerykeion import AstrologicalSubject, KerykeionChartSVG, Report
from telebot import types

from db_functions import get_user_name, get_birth_date, get_birth_time, get_birth_place
from main import bot


def request_missing_info(chat_id, missing_info):
    """Send a message to the user requesting the missing information."""
    bot.send_message(chat_id, f"Please enter your {missing_info}.")


def run(user_id, chat_id):
    birth_date_str = get_birth_date(user_id)
    user_name = get_user_name(user_id)
    birth_time_str = get_birth_time(user_id)
    birth_place_str = get_birth_place(user_id)

    missing_info = []

    if not user_name:
        missing_info.append("Enter name")
    if not birth_date_str:
        missing_info.append("Enter birth date")
    if not birth_time_str:
        missing_info.append("Enter birth time")
    if not birth_place_str:
        missing_info.append("Enter birth place")

    if missing_info:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for item in missing_info:
            markup.add(item)
        markup.add("Exit")
        bot.send_message(chat_id, "Please provide the missing information:", reply_markup=markup)
        return  # Exit the function and wait for user's response

    # Parsing birthdate and time
    birth_date_str = birth_date_str.split(' ')[0]
    birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d')
    birth_time = datetime.strptime(birth_time_str, '%H:%M')

    birth_place_parts = birth_place_str.split(', ')
    city = birth_place_parts[0]
    nation = birth_place_parts[1] if len(birth_place_parts) > 1 else ""

    # Initialize AstrologicalSubject with parsed data
    person = AstrologicalSubject(
        name=user_name,
        year=birth_date.year,
        month=birth_date.month,
        day=birth_date.day,
        hour=birth_time.hour,
        minute=birth_time.minute,
        city=city,
        nation=nation
    )
    cur_dir = os.getcwd()
    svg = KerykeionChartSVG(person, chart_type='Natal', new_output_directory=cur_dir)
    svg.makeSVG()

    svg_filename = f"{svg.name}{svg.chart_type}Chart.svg"
    png_filename = svg_filename.replace('.svg', '.png')

    # Convert SVG to PNG
    cairosvg.svg2png(url=os.path.join(cur_dir, svg_filename), write_to=os.path.join(cur_dir, png_filename))

    photo = open(os.path.join(cur_dir, png_filename), 'rb')
    bot.send_photo(chat_id, photo)
    photo.close()

    report = Report(person)
    report_text = report.get_full_report()

    bot.send_message(chat_id, report_text)
