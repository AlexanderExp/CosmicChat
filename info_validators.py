import re
from datetime import datetime


def validate_and_parse_date(date_text):
    """
    Проверяет, соответствует ли текст даты формату ДД.ММ.ГГГГ, и преобразует его в объект datetime.
    Возвращает кортеж (bool, datetime), где первый элемент - успешность преобразования, второй - объект datetime или None.
    """
    if re.match(r"\d{2}\.\d{2}\.\d{4}", date_text):
        try:
            return True, datetime.strptime(date_text, '%d.%m.%Y')
        except ValueError:
            return False, None
    else:
        return False, None


def validate_and_parse_time(time_text):
    """
    Проверяет, соответствует ли текст времени формату ЧЧ:ММ в 24-часовом формате, и преобразует его в объект datetime.time.
    Возвращает кортеж (bool, datetime.time), где первый элемент - успешность преобразования, второй - объект datetime.time или None.
    """
    if re.match(r'^([01][0-9]|2[0-3]):[0-5][0-9]$', time_text):
        try:
            return True, datetime.strptime(time_text, '%H:%M').time()
        except ValueError:
            return False, None
    else:
        return False, None


def validate_birth_place(place_text):
    """
    Проверяет, соответствует ли текст места рождения формату 'Город, Страна'.
    Возвращает bool - успешность проверки.
    """
    if re.match(r"^[a-zA-Zа-яА-ЯёЁ\s-]+, [a-zA-Zа-яА-ЯёЁ\s-]+$", place_text):
        return True
    else:
        return False
