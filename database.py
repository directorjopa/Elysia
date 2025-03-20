import sqlite3

def init_db():
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS users')  # Удаляем старую таблицу, если она есть
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            name TEXT,
            days_in_bot INTEGER DEFAULT 0,
            prefrontal_cortex INTEGER DEFAULT 0,
            hippocampus INTEGER DEFAULT 0,
            amygdala INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def get_user_data(user_id):
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user_data = cursor.fetchone()
    conn.close()
    return user_data

def update_user_data(user_id, **kwargs):
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    set_clause = ', '.join([f"{key} = ?" for key in kwargs.keys()])
    values = list(kwargs.values())
    values.append(user_id)
    cursor.execute(f'UPDATE users SET {set_clause} WHERE user_id = ?', values)
    conn.commit()
    conn.close()

def add_user(user_id, name):
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (user_id, name) VALUES (?, ?)', (user_id, name))
    conn.commit()
    conn.close()
