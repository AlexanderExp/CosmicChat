from telebot import types


def create_chinese_menu():
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
