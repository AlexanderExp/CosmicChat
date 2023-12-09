import db_functions
import hse_spec_func
import natal_map
from info_validators import validate_birth_place, validate_and_parse_time, validate_and_parse_date
from main import fetch_horoscope, update_daily_horoscope
from menus import create_zodiac_menu, create_menu_yes_no, create_zodiac_menu2, create_main_menu_markup, \
    create_chinese_menu

user_data = {}


def handle_message(message, bot):
    user_id = message.from_user.id
    ensure_user_data_exists(user_id)
    process_user_message(message, user_id, bot)


def ensure_user_data_exists(user_id):
    if user_id not in user_data:
        user_data[user_id] = {}


def handle_registration_process(message, bot):
    date_text = message.text
    is_valid, birth_date = validate_and_parse_date(date_text)
    if is_valid:
        db_functions.set_birthday(birth_date, message.from_user.id)
        bot.reply_to(message, "Вы успешно зарегистрированы!")
        bot.send_message(message.chat.id, "Хотите получать ежедневный астрологический прогноз?",
                         reply_markup=create_menu_yes_no())
    else:
        bot.reply_to(message, "Неверный формат даты. Пожалуйста, введите дату в формате ДД.ММ.ГГГГ.")


def process_user_message(message, user_id, bot):
    state = db_functions.check_user(user_id)
    if state is None:
        handle_new_user(message, user_id, bot)
    elif state[0] == 'false':
        handle_registration_process(message, bot)
    else:
        handle_registered_user_actions(message, bot)


def handle_new_user(message, user_id, bot):
    db_functions.register_user(user_id, None)
    welcome_message = "Добро пожаловать в бота-гороскоп! Пожалуйста, введите вашу дату рождения в формате ДД.ММ.ГГГГ."
    bot.reply_to(message, welcome_message)


def handle_compatibility(message, bot):
    bot.send_message(message.chat.id, "Выберите знак зодиака, про который Вы хотите узнать:",
                     reply_markup=create_zodiac_menu2())


def handle_natal_map(message, bot):
    natal_map.run(message.from_user.id, message.chat.id, bot)


def handle_HSE_crow(message, bot):
    bot.send_message(message.chat.id, hse_spec_func.random_crow())


def handle_daily_motivation(message, bot):
    bot.send_message(message.chat.id, hse_spec_func.random_motivation())


def handle_daily_horoscope_subscription(message, bot):
    """
    Handles the subscription or unsubscription of the user from the daily horoscope mailing list.
    It toggles the current state of the user's subscription.
    """
    is_subscribed = db_functions.change_subscription(message.from_user.id)
    if is_subscribed == (1,):
        response_message = "Done! Вы отписались от ежедневной рассылки."
    else:
        response_message = "Готово! Вы подписались на ежедневную рассылку гороскопа."
    bot.send_message(message.chat.id, response_message)


def handle_natal_map_set_awaiting_for_addition_flag(message, user_id, bot):
    if message.text == "Ввести имя":
        bot.reply_to(message, "Пожалуйста, введите ваше имя")
        user_data[user_id]['awaiting_info'] = 'name'
    elif message.text == "Ввести дату рождения":
        bot.reply_to(message, "Пожалуйста, введите вашу дату рождения в формате 'ДД.ММ.ГГГГ'")
        user_data[user_id]['awaiting_info'] = 'birth_date'
    elif message.text == "Ввести время рождения":
        bot.reply_to(message, "Пожалуйста, введите ваше время рождения в формате 'ЧЧ:ММ'")
        user_data[user_id]['awaiting_info'] = 'birth_time'
    elif message.text == "Ввести место рождения":
        bot.reply_to(message, "Пожалуйста, введите место вашего рождения в формате 'Город, Страна'")
        user_data[user_id]['awaiting_info'] = 'birth_place'
    elif message.text == "Выйти":
        bot.reply_to(message, "Ходят слухи, что в начале 90-х на эту кнопку нажали 15 союзных республик")
        bot.send_message(message.chat.id, "Выберите действие", reply_markup=create_main_menu_markup())


def user_info_name_addition(message, user_id, bot):
    if message.text == "":
        bot.reply_to(message, "Вы ничего не ввели, попробуйте еще раз")
    else:
        db_functions.update_user_info(user_id, user_name=message.text)
        bot.reply_to(message, "Ваше имя сохранено")
        del user_data[user_id]['awaiting_info']
        natal_map.run(user_id, message.chat.id, bot)


def user_info_birth_date_addition(message, user_id, bot):
    is_valid, birth_date = validate_and_parse_date(message.text)
    if is_valid:
        db_functions.update_user_info(user_id, birth_date=message.text)
        bot.reply_to(message, "Дата рождения сохранена")
        del user_data[user_id]['awaiting_info']
        natal_map.run(user_id, message.chat.id, bot)
    else:
        bot.reply_to(message, "Вы ничего не ввели, попробуйте ввести дату рождения (ДД.ММ.ГГГГ) еще раз")


def user_info_birth_time_addition(message, user_id, bot):
    is_valid, time_value = validate_and_parse_time(message.text)
    if is_valid:
        db_functions.update_user_info(user_id, birth_time=time_value.strftime('%H:%M'))
        bot.reply_to(message, "Время рождения сохранено")
        del user_data[user_id]['awaiting_info']
        natal_map.run(user_id, message.chat.id, bot)
    else:
        bot.reply_to(message, "Неверный формат времени. Пожалуйста, введите время в формате ЧЧ:ММ.")


def user_info_birth_place_addition(message, user_id, bot):
    is_valid = validate_birth_place(message.text)
    if is_valid:
        db_functions.update_user_info(user_id, birth_place=message.text)
        bot.reply_to(message, "Место рождения сохранено")
        del user_data[user_id]['awaiting_info']
        natal_map.run(user_id, message.chat.id, bot)
    else:
        bot.reply_to(message,
                     "Неверный формат места рождения. Пожалуйста, введите в формате 'Город, Страна'")


def handle_natal_map_info_addition(message, awaiting_info, user_id, bot):
    if awaiting_info == 'name':
        user_info_name_addition(message, user_id, bot)
    elif awaiting_info == 'birth_date':
        user_info_birth_date_addition(message, user_id, bot)
    elif awaiting_info == 'birth_time':
        user_info_birth_time_addition(message, user_id, bot)
    elif awaiting_info == 'birth_place':
        user_info_birth_place_addition(message, user_id, bot)


def handle_daily_horoscope(message, user_id):
    sign = db_functions.get_sign(user_id)
    update_daily_horoscope()
    fetch_horoscope(message, sign)


def handle_zodiac_selection(message, bot):
    bot.send_message(message.chat.id, "Выберите знак зодиака:", reply_markup=create_zodiac_menu())


def handle_chinese_horoscope(message, bot):
    bot.send_message(message.chat.id, "Выберите животное:", reply_markup=create_chinese_menu())


def handle_registered_user_actions(message, bot):
    user_id = message.from_user.id
    if message.text == "Мой гороскоп на сегодня":
        handle_daily_horoscope(message, user_id)
    elif message.text == "Гороскоп на сегодня (выбрать зодиак)":
        handle_zodiac_selection(message, bot)
    elif message.text == "Китайский гороскоп":
        handle_chinese_horoscope(message, bot)
    elif message.text == "Совместимость":
        handle_compatibility(message, bot)
    elif message.text == "Натальная карта":
        handle_natal_map(message, bot)
    elif message.text == "HSE Special: Какая ворона ты сегодня?":
        handle_HSE_crow(message, bot)
    elif message.text == "Мотивашка дня":
        handle_daily_motivation(message, bot)
    elif message.text == "Отписаться / подписаться на ежедневный гороскоп":
        handle_daily_horoscope_subscription(message, bot)
    elif message.text in ["Ввести имя", "Ввести дату рождения", "Ввести время рождения", "Ввести место рождения"]:
        handle_natal_map_set_awaiting_for_addition_flag(message, user_id, bot)
    elif user_id in user_data and 'awaiting_info' in user_data[user_id]:
        awaiting_info = user_data[user_id]['awaiting_info']
        handle_natal_map_info_addition(message, awaiting_info, user_id, bot)
    else:
        bot.send_message(message.chat.id, 'Ой! Я вас не понял :(', reply_markup=create_main_menu_markup())
