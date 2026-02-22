import sqlite3
import os
import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'db', 'activitytracker.db')

def add_task(user_id, category, task):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute('INSERT INTO tasks(user_id, text, category, created_at) VALUES (?, ?, ?, datetime("now"))', (user_id, task, category))
        conn.commit()

def get_tasks(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute('SELECT id, text, is_done, created_at FROM tasks WHERE user_id = ?', (user_id,))
        return cur.fetchall()

def get_today_tasks(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, text, is_done FROM tasks WHERE user_id = ? AND date(created_at) = date('now', 'localtime') ORDER BY id", (user_id,))
        return cur.fetchall()

def done_task(user_id, task_id):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute('UPDATE tasks SET is_done = 1 WHERE user_id = ? AND id = ? AND is_done = 0', (user_id, task_id))
        conn.commit()
        return cur.rowcount > 0

def task_stats(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()

        cur.execute('SELECT COUNT(*), SUM(is_done) FROM tasks WHERE user_id = ?', (user_id,))
        res = cur.fetchone()
        total_tasks = res[0]

        done_tasks = int(res[1]) if res[1] is not None else 0

        by_category = cur.execute('SELECT category, COUNT(*) FROM tasks WHERE user_id = ? GROUP BY category', (user_id,)).fetchall()
        
        progress = (done_tasks / total_tasks) * 100 if total_tasks > 0 else 0

        return total_tasks, done_tasks, by_category, progress