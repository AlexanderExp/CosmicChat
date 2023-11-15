import sqlite3

def create_database() -> None:
    conn = sqlite3.connect('users.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY,
        birth_date TIMESTAMP,
        birth_place TEXT,
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
    cursor.execute('UPDATE user SET birth_date = ?, state = ? WHERE id = ?', (date, 'true', user_id))
    conn.commit()
    conn.close()