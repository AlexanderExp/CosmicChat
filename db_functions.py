import sqlite3
import zodiac_sign

def create_database() -> None:
    conn = sqlite3.connect('users.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY,
        birth_date TIMESTAMP,
        zodiac_sign TEXT,
        chineese_zodiac TEXT,
        birth_place TEXT,
        daily_mess INTEGER,
        state BOOL
    )
    ''')
    conn.commit()
    conn.close()

def check_user(user_id: int):
    conn = sqlite3.connect('users.sqlite')
    cursor = conn.cursor()
    cursor.execute('SELECT state FROM user WHERE id = ?', (user_id,))
    result = cursor.fetchone()
    conn.commit()
    conn.close()
    return result
    
def register_user(user_id: int, state) -> None:
    if state is None:
        conn = sqlite3.connect('users.sqlite')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO user (id, state) VALUES (?, ?)', (user_id, 'false'))
        conn.commit()
        conn.close()

def set_birthday(date: str, user_id) -> None:
    conn = sqlite3.connect('users.sqlite')
    cursor = conn.cursor()
    cursor.execute('UPDATE user SET birth_date = ?, zodiac_sign = ?, chineese_zodiac = ?, state = ? WHERE id = ?', 
                   (date, zodiac_sign.zodiac_info(date)[0], zodiac_sign.zodiac_info(date)[1], 'true', user_id))
    conn.commit()
    conn.close()

def set_subscription(b: int, user_id) -> None:
    conn = sqlite3.connect('users.sqlite')
    cursor = conn.cursor()
    cursor.execute('UPDATE user SET daily_mess = ?, state = ? WHERE id = ?', 
                   (b, 'true', user_id))
    conn.commit()
    conn.close()