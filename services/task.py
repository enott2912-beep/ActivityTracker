import sqlite3
import datetime
from config import DB_PATH

def add_task(user_id, category, task, date=None, time=None):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute('INSERT INTO tasks(user_id, text, category, date, time) VALUES (?, ?, ?, ?, ?)',
                    (user_id, task, category, date, time))
        conn.commit()
        return cur.lastrowid

def get_today_tasks(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("""SELECT id, text, is_done, time FROM tasks
                       WHERE user_id = ? AND (date = date('now', 'localtime') OR (date IS NULL AND date(created_at, 'localtime') = date('now', 'localtime')))
                       ORDER BY time, id""", (user_id,))
        return cur.fetchall()

def done_task(user_id, task_id):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute('UPDATE tasks SET is_done = 1, done_at = datetime("now") WHERE user_id = ? AND id = ? AND is_done = 0', (user_id, task_id))
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

def get_completed_task_dates(user_id):
    """Возвращает отсортированный список уникальных дат (YYYY-MM-DD), когда были выполнены задачи."""
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT DISTINCT date(done_at, 'localtime')
            FROM tasks
            WHERE user_id = ? AND is_done = 1 AND done_at IS NOT NULL
            ORDER BY date(done_at, 'localtime') DESC
        """, (user_id,))
        return [row[0] for row in cur.fetchall()]

def calculate_streak(user_id):
    """Вычисляет текущий стрик (серию последовательных дней с выполненными задачами)."""
    completed_dates_str = get_completed_task_dates(user_id)
    if not completed_dates_str:
        return 0

    completed_dates = [datetime.date.fromisoformat(d) for d in completed_dates_str]

    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)

    # Стрик продолжается, если последняя задача была выполнена сегодня или вчера.
    if completed_dates[0] not in [today, yesterday]:
        return 0

    streak = 1
    last_date = completed_dates[0]
    # Проверяем остальные даты
    for i in range(1, len(completed_dates)):
        expected_previous_date = last_date - datetime.timedelta(days=1)
        if completed_dates[i] == expected_previous_date:
            streak += 1
            last_date = completed_dates[i]
        else:
            # Последовательность прервалась
            break

    return streak

def get_user_activity_summary(user_id):
    """
    Собирает сводную информацию по активности пользователя.
    Возвращает словарь с общим количеством задач, выполненными задачами,
    статистикой по категориям выполненных задач и полным списком задач.
    """
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        # Общая статистика
        cur.execute("""
            SELECT
                COUNT(*) AS total_tasks,
                SUM(CASE WHEN is_done = 1 THEN 1 ELSE 0 END) AS done_tasks
            FROM tasks
            WHERE user_id = ?
        """, (user_id,))
        summary = cur.fetchone()
        total_tasks = summary['total_tasks'] if summary else 0
        done_tasks = summary['done_tasks'] if summary and summary['done_tasks'] is not None else 0

        # Статистика по категориям (только выполненные)
        cur.execute("""
            SELECT category, COUNT(*) as count
            FROM tasks
            WHERE user_id = ? AND is_done = 1
            GROUP BY category
        """, (user_id,))
        categories_raw = cur.fetchall()
        categories = {row['category']: row['count'] for row in categories_raw}

        # Список всех задач
        cur.execute("SELECT text, is_done FROM tasks WHERE user_id = ?", (user_id,))
        tasks_raw = cur.fetchall()
        tasks = [{'text': row['text'], 'is_done': bool(row['is_done'])} for row in tasks_raw]

        return {
            'total_tasks': total_tasks,
            'done_tasks': done_tasks,
            'categories': categories,
            'tasks': tasks
        }

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