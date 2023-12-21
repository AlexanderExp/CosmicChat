import sqlite3

import zodiac_sign


def create_database() -> None:
    conn = sqlite3.connect('users.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY,
        birth_date TIMESTAMP,
        birth_time TEXT,
        user_name TEXT,
        zodiac_sign TEXT,
        chineese_zodiac TEXT,
        birth_place TEXT,
        daily_mess INTEGER,
        crow_type TEXT,
        crow_text TEXT,
        crow_time TEXT,
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


def change_subscription(user_id):
    conn = sqlite3.connect('users.sqlite')
    cursor = conn.cursor()
    [is_subs, ] = cursor.execute('SELECT daily_mess FROM user WHERE id = ?',
                                 (user_id,))
    if is_subs == (1,):
        cursor.execute('UPDATE user SET daily_mess = ?, state = ? WHERE id = ?',
                       (0, 'true', user_id))
    else:
        cursor.execute('UPDATE user SET daily_mess = ?, state = ? WHERE id = ?',
                       (1, 'true', user_id))
    conn.commit()
    conn.close()
    return is_subs


def get_sign(user_id):
    conn = sqlite3.connect('users.sqlite')
    cursor = conn.cursor()
    [sign, ] = cursor.execute('SELECT zodiac_sign FROM user WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()
    return sign[0]


def get_user_name(user_id):
    """ Query user_name by user_id """
    conn = sqlite3.connect('users.sqlite')
    cur = conn.cursor()
    cur.execute("SELECT user_name FROM user WHERE id=?", (user_id,))
    result = cur.fetchone()
    return result[0] if result else None


def get_birth_date(user_id):
    """ Query birth_date by user_id """
    conn = sqlite3.connect('users.sqlite')
    cur = conn.cursor()
    cur.execute("SELECT birth_date FROM user WHERE id=?", (user_id,))
    result = cur.fetchone()
    return result[0] if result else None


def get_birth_time(user_id):
    """ Query birth_time by user_id """
    conn = sqlite3.connect('users.sqlite')
    cur = conn.cursor()
    cur.execute("SELECT birth_time FROM user WHERE id=?", (user_id,))
    result = cur.fetchone()
    return result[0] if result else None


def get_birth_place(user_id):
    """ Query birth_place by user_id """
    conn = sqlite3.connect('users.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT birth_place FROM user WHERE id=?", (user_id,))
    result = cursor.fetchone()
    return result[0] if result else None

def get_crow(user_id):
    """ Query current crow by user_id """
    conn = sqlite3.connect('users.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT crow_type, crow_text FROM user WHERE id=?", (user_id,))
    result = cursor.fetchone()
    return result if result else None

def get_crow_time(user_id):
    """ Query current crow by user_id """
    conn = sqlite3.connect('users.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT crow_time FROM user WHERE id=?", (user_id,))
    result = cursor.fetchone()
    return result[0] if result else None

def set_crow(user_id, crow, crow_text, time):
    """ Set current crow by user_id """
    conn = sqlite3.connect('users.sqlite')
    cursor = conn.cursor()
    cursor.execute("UPDATE user SET crow_type = ?, crow_text = ?, crow_time = ? WHERE id = ?",
                       (crow, crow_text, time, user_id))
    conn.commit()
    conn.close()


def update_user_info(user_id, user_name=None, birth_date=None, birth_time=None, birth_place=None):
    """
    Insert or update user information in the database.
    If a user with the given user_id exists, update their information.
    Otherwise, insert a new record.
    """
    conn = sqlite3.connect('users.sqlite')
    cursor = conn.cursor()
    if user_name:
        cursor.execute("UPDATE user SET user_name=? WHERE id=?", (user_name, user_id))
    if birth_date:
        cursor.execute("UPDATE user SET birth_date=? WHERE id=?", (birth_date, user_id))
    if birth_time:
        cursor.execute("UPDATE user SET birth_time=? WHERE id=?", (birth_time, user_id))
    if birth_place:
        cursor.execute("UPDATE user SET birth_place=? WHERE id=?", (birth_place, user_id))

    conn.commit()
    conn.close()
