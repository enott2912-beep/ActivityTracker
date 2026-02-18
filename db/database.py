import sqlite3
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, 'activitytracker.db')
conn = sqlite3.connect(db_path)
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS tasks(
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_done BOOLEAN DEFAULT FALSE,
    category TEXT
)''')
conn.commit()
conn.close()
print(f"База данных '{db_path}' и таблица 'tasks' успешно созданы/проверены.")