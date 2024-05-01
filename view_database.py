import sqlite3

conn = sqlite3.connect('bot_database.db')

cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    last_name TEXT
                )''')
cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER,
                    message TEXT,
                    timestamp TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )''')
conn.commit()
conn.close()
