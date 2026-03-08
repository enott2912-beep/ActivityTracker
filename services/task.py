import sqlite3
import os
import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'db', 'activitytracker.db')

def add_task(user_id, category, task, date=None, time=None):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute('INSERT INTO tasks(user_id, text, category, date, time) VALUES (?, ?, ?, ?, ?)',
                    (user_id, task, category, date, time))
        conn.commit()
        return cur.lastrowid

def get_tasks(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute('SELECT id, text, is_done, date FROM tasks WHERE user_id = ?', (user_id,))
        return cur.fetchall()

def get_today_tasks(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, text, is_done, time FROM tasks WHERE user_id = ? AND (date = date('now', 'localtime') OR date IS NULL) ORDER BY time, id", (user_id,))
        return cur.fetchall()

def done_task(user_id, task_id):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute('UPDATE tasks SET is_done = 1 WHERE user_id = ? AND id = ? AND is_done = 0', (user_id, task_id))
        conn.commit()
        return cur.rowcount > 0

def delete_task(user_id, task_id):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute('DELETE FROM tasks WHERE user_id = ? AND id = ?', (user_id, task_id))
        conn.commit()
        return cur.rowcount > 0

def task_stats(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()

        cur.execute('SELECT COUNT(*), SUM(is_done) FROM tasks WHERE user_id = ?', (user_id,))
        res = cur.fetchone()
        total_tasks = res[0] if res[0] is not None else 0

        done_tasks = int(res[1]) if res[1] is not None else 0

        cur.execute("SELECT COUNT(*) FROM tasks WHERE user_id = ? AND date < date('now', 'localtime') AND is_done = 0", (user_id,))
        overdue_count = cur.fetchone()[0]

        by_category = cur.execute('SELECT category, COUNT(*) FROM tasks WHERE user_id = ? GROUP BY category', (user_id,)).fetchall()
        
        progress = (done_tasks / total_tasks) * 100 if total_tasks > 0 else 0

        return total_tasks, done_tasks, by_category, progress, overdue_count

def upcoming_tasks(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, text, is_done, date, time FROM tasks WHERE user_id = ? AND date > date('now', 'localtime') AND is_done = 0 ORDER BY date, time", (user_id,))
        return cur.fetchall()

def get_overdue_tasks(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, text, is_done, date, time FROM tasks WHERE user_id = ? AND date < date('now', 'localtime') AND is_done = 0 ORDER BY date, time", (user_id,))
        return cur.fetchall()

def get_task(task_id):
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        return cur.fetchone()

def set_reminder_job_id(task_id, job_id):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute('UPDATE tasks SET reminder_job_id = ? WHERE id = ?', (job_id, task_id))
        conn.commit()