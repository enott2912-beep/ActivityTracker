import sqlite3
import os
from config import DB_PATH

def setup_database():
    """
    Инициализирует базу данных: создает директорию и файл БД,
    а также таблицу 'tasks', если они не существуют.
    """
    base_dir = os.path.dirname(DB_PATH)
    os.makedirs(base_dir, exist_ok=True)

    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        cur.execute('''
        CREATE TABLE IF NOT EXISTS tasks(
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_done BOOLEAN DEFAULT FALSE,
            category TEXT,
            date DATE,
            time TIME,
            reminder_job_id TEXT,
            done_at TIMESTAMP        
        )''')
        conn.commit()
        print(f"База данных '{DB_PATH}' и таблица 'tasks' успешно созданы/проверены.")
    except sqlite3.Error as e:
        print(f"Произошла ошибка SQLite: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    setup_database()