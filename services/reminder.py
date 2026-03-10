import sqlite3
import datetime
from config import DB_PATH

def get_today_active_tasks(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("""SELECT id, text, is_done FROM tasks
                       WHERE user_id = ? AND is_done = 0 AND
                             (date = date('now', 'localtime') OR (date IS NULL AND date(created_at, 'localtime') = date('now', 'localtime')))
                       ORDER BY id""", (user_id,))
        return cur.fetchall()

def get_all_user_ids():
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT user_id FROM tasks")
        return [item[0] for item in cur.fetchall()]
