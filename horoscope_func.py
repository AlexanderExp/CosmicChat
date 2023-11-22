import requests

def get_daily_horoscope(sign: str) -> dict:
    """Get daily horoscope for a zodiac sign.
    Keyword arguments:
    sign:str - Zodiac sign
    day:str - Date in format (YYYY-MM-DD) OR TODAY OR TOMORROW OR YESTERDAY
    Return:dict - JSON data
    """
    url = "https://www.chita.ru/horoscope/daily/"
    params = {"sign": sign}
    response = requests.get(url, params)

    a = response.json()
    b=1
    return response.json()
