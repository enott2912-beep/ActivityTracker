import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'db', 'activitytracker.db')

def add_task(user_id, task):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute('INSERT INTO tasks(user_id, text) VALUES (?, ?)', (user_id, task))
        conn.commit()

def get_tasks(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute('SELECT text FROM tasks WHERE user_id = ?', (user_id,))
        return cur.fetchall()