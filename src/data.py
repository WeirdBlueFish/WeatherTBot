import sqlite3

conn = sqlite3.connect('weather_bot.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id INTEGER UNIQUE,
    username TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS favorite_cities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    city_name TEXT,
    FOREIGN KEY (user_id) REFERENCES users (id)
)
''')

conn.commit()
conn.close()
# =================FUNCTIONS====================

def add_user(chat_id, username=None):
    conn = sqlite3.connect('weather_bot.db')
    cursor = conn.cursor()

    cursor.execute('SELECT id FROM users WHERE chat_id = ?', (chat_id,))
    user = cursor.fetchone()

    if not user:
        cursor.execute('INSERT INTO users (chat_id, username) VALUES (?, ?)', (chat_id, username))
        conn.commit()

    conn.close()

def add_favorite_city(chat_id, city_name):
    conn = sqlite3.connect('weather_bot.db')
    cursor = conn.cursor()

    cursor.execute('SELECT id FROM users WHERE chat_id = ?', (chat_id,))
    user = cursor.fetchone()

    if user:
        user_id = user[0]
        cursor.execute('INSERT INTO favorite_cities (user_id, city_name) VALUES (?, ?)', (user_id, city_name))
        conn.commit()

    conn.close()

def get_favorite_cities(chat_id):
    conn = sqlite3.connect('weather_bot.db')
    cursor = conn.cursor()

    cursor.execute('SELECT id FROM users WHERE chat_id = ?', (chat_id,))
    user = cursor.fetchone()

    if user:
        user_id = user[0]
        cursor.execute('SELECT city_name FROM favorite_cities WHERE user_id = ?', (user_id,))
        cities = cursor.fetchall()
        conn.close()
        return [city[0] for city in cities]  
    else:
        conn.close()
        return []

def remove_favorite_city(chat_id, city_name):
    conn = sqlite3.connect('weather_bot.db')
    cursor = conn.cursor()

    
    cursor.execute('SELECT id FROM users WHERE chat_id = ?', (chat_id,))
    user = cursor.fetchone()

    if user:
        user_id = user[0]

        cursor.execute('DELETE FROM favorite_cities WHERE user_id = ? AND city_name = ?', (user_id, city_name))
        conn.commit()

    conn.close()