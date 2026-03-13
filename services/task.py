import aiosqlite
import datetime
from config import DB_PATH

async def add_task(user_id, category, task, date=None, time=None):
    async with aiosqlite.connect(DB_PATH) as conn:
        cursor = await conn.execute('INSERT INTO tasks(user_id, text, category, date, time) VALUES (?, ?, ?, ?, ?)',
                                    (user_id, task, category, date, time))
        await conn.commit()
        return cursor.lastrowid

async def get_today_tasks(user_id):
    async with aiosqlite.connect(DB_PATH) as conn:
        async with conn.execute("""SELECT id, text, is_done, time FROM tasks
                                   WHERE user_id = ? AND (date = date('now', 'localtime') OR (date IS NULL AND date(created_at, 'localtime') = date('now', 'localtime')))
                                   ORDER BY time, id""", (user_id,)) as cursor:
            return await cursor.fetchall()

async def done_task(user_id, task_id):
    async with aiosqlite.connect(DB_PATH) as conn:
        cursor = await conn.execute('UPDATE tasks SET is_done = 1, done_at = datetime("now") WHERE user_id = ? AND id = ? AND is_done = 0', (user_id, task_id))
        await conn.commit()
        return cursor.rowcount > 0

async def delete_task(user_id, task_id):
    async with aiosqlite.connect(DB_PATH) as conn:
        cursor = await conn.execute('DELETE FROM tasks WHERE user_id = ? AND id = ?', (user_id, task_id))
        await conn.commit()
        return cursor.rowcount > 0

async def task_stats(user_id):
    async with aiosqlite.connect(DB_PATH) as conn:
        async with conn.execute('SELECT COUNT(*), SUM(is_done) FROM tasks WHERE user_id = ?', (user_id,)) as cursor:
            res = await cursor.fetchone()
            total_tasks = res[0] if res[0] is not None else 0
            done_tasks = int(res[1]) if res[1] is not None else 0

        async with conn.execute("SELECT COUNT(*) FROM tasks WHERE user_id = ? AND date < date('now', 'localtime') AND is_done = 0", (user_id,)) as cursor:
            overdue_res = await cursor.fetchone()
            overdue_count = overdue_res[0]

        async with conn.execute('SELECT category, COUNT(*) FROM tasks WHERE user_id = ? GROUP BY category', (user_id,)) as cursor:
            by_category = await cursor.fetchall()
            
            progress = (done_tasks / total_tasks) * 100 if total_tasks > 0 else 0

            return total_tasks, done_tasks, by_category, progress, overdue_count

async def upcoming_tasks(user_id):
    async with aiosqlite.connect(DB_PATH) as conn:
        async with conn.execute("SELECT id, text, is_done, date, time FROM tasks WHERE user_id = ? AND date > date('now', 'localtime') AND is_done = 0 ORDER BY date, time", (user_id,)) as cursor:
            return await cursor.fetchall()

async def get_overdue_tasks(user_id):
    async with aiosqlite.connect(DB_PATH) as conn:
        async with conn.execute("SELECT id, text, is_done, date, time FROM tasks WHERE user_id = ? AND date < date('now', 'localtime') AND is_done = 0 ORDER BY date, time", (user_id,)) as cursor:
            return await cursor.fetchall()

async def get_task(task_id):
    async with aiosqlite.connect(DB_PATH) as conn:
        conn.row_factory = aiosqlite.Row
        async with conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)) as cursor:
            return await cursor.fetchone()

async def set_reminder_job_id(task_id, job_id):
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute('UPDATE tasks SET reminder_job_id = ? WHERE id = ?', (job_id, task_id))
        await conn.commit()

async def get_completed_task_dates(user_id):
    """Returns a sorted list of unique dates (YYYY-MM-DD) when tasks were completed."""
    async with aiosqlite.connect(DB_PATH) as conn:
        async with conn.execute("""
                SELECT DISTINCT date(done_at, 'localtime')
                FROM tasks
                WHERE user_id = ? AND is_done = 1 AND done_at IS NOT NULL
                ORDER BY date(done_at, 'localtime') DESC
            """, (user_id,)) as cursor:
            rows = await cursor.fetchall()
            return [row[0] for row in rows]

async def calculate_streak(user_id):
    """Calculates the current streak (consecutive days with completed tasks)."""
    completed_dates_str = await get_completed_task_dates(user_id)
    if not completed_dates_str:
        return 0

    completed_dates = [datetime.date.fromisoformat(d) for d in completed_dates_str]

    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)

    # Streak is valid if the last task was done today or yesterday.
    if completed_dates[0] not in [today, yesterday]:
        return 0

    streak = 1
    last_date = completed_dates[0]
    # Check previous dates
    for i in range(1, len(completed_dates)):
        expected_previous_date = last_date - datetime.timedelta(days=1)
        if completed_dates[i] == expected_previous_date:
            streak += 1
            last_date = completed_dates[i]
        else:
            # Sequence broken
            break

    return streak

async def get_user_activity_summary(user_id):
    """
    Aggregates user activity summary.
    Returns a dict with total tasks, completed tasks, category stats, and full task list.
    """
    async with aiosqlite.connect(DB_PATH) as conn:
        conn.row_factory = aiosqlite.Row
        
        # General stats
        async with conn.execute("""
            SELECT
                COUNT(*) AS total_tasks,
                SUM(CASE WHEN is_done = 1 THEN 1 ELSE 0 END) AS done_tasks
            FROM tasks
            WHERE user_id = ?
        """, (user_id,)) as cursor:
            summary = await cursor.fetchone()
            total_tasks = summary['total_tasks'] if summary else 0
            done_tasks = summary['done_tasks'] if summary and summary['done_tasks'] is not None else 0
    
        # Category stats (completed only)
        async with conn.execute("""
            SELECT category, COUNT(*) as count
            FROM tasks
            WHERE user_id = ? AND is_done = 1
            GROUP BY category
        """, (user_id,)) as cursor:
            categories_raw = await cursor.fetchall()
            categories = {row['category']: row['count'] for row in categories_raw}
    
        # List of all tasks
        async with conn.execute("SELECT text, is_done FROM tasks WHERE user_id = ?", (user_id,)) as cursor:
            tasks_raw = await cursor.fetchall()
            tasks = [{'text': row['text'], 'is_done': bool(row['is_done'])} for row in tasks_raw]
    
            return {
                'total_tasks': total_tasks,
                'done_tasks': done_tasks,
                'categories': categories,
                'tasks': tasks
            }

async def get_today_active_tasks(user_id):
    async with aiosqlite.connect(DB_PATH) as conn:
        async with conn.execute("""SELECT id, text, is_done FROM tasks
                                   WHERE user_id = ? AND is_done = 0 AND
                                         (date = date('now', 'localtime') OR (date IS NULL AND date(created_at, 'localtime') = date('now', 'localtime')))
                                   ORDER BY id""", (user_id,)) as cursor:
            return await cursor.fetchall()

async def get_all_user_ids():
    async with aiosqlite.connect(DB_PATH) as conn:
        async with conn.execute("SELECT DISTINCT user_id FROM tasks") as cursor:
            rows = await cursor.fetchall()
            return [item[0] for item in rows]