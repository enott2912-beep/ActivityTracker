import sqlite3

conn = sqlite3.connect('db/activitytracker.db')
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS tasks(
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_done BOOLEAN DEFAULT FALSE
)''')
conn.commit()
conn.close()
print("База данных 'db/activitytracker.db' и таблица 'tasks' успешно созданы/проверены.")