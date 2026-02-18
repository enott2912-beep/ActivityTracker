import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'db', 'activitytracker.db')

def add_task(user_id, category, task):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute('INSERT INTO tasks(user_id, text, category) VALUES (?, ?, ?)', (user_id, task, category))
        conn.commit()

def get_tasks(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute('SELECT id, text FROM tasks WHERE user_id = ? AND is_done = 0', (user_id,))
        return cur.fetchall()

def done_task(user_id, task_id):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute('UPDATE tasks SET is_done = 1 WHERE user_id = ? AND id = ? AND is_done = 0', (user_id, task_id))
        conn.commit()
        return cur.rowcount > 0