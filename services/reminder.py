import sqlite3
import os
import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'db', 'activitytracker.db')

def get_today_active_tasks(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, text, is_done FROM tasks WHERE user_id = ? AND (date = date('now', 'localtime') OR date IS NULL) AND is_done = 0 ORDER BY id", (user_id,))
        return cur.fetchall()

def get_all_user_ids():
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT user_id FROM tasks")
        return [item[0] for item in cur.fetchall()]
