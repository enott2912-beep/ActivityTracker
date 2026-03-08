import logging
from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from services.reminder import get_all_user_ids, get_today_active_tasks
from services.task import get_task
logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.INFO)

scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

async def send_morning_summary(bot: Bot):
    """Отправляет утреннюю сводку задач всем пользователям."""
    user_ids = get_all_user_ids()
    for user_id in user_ids:
        tasks = get_today_active_tasks(user_id)
        if tasks:
            task_list = "\n".join([f"▫️ {task[1]}" for task in tasks])
            message = f"☀️ Доброе утро!\n\nЗадачи на сегодня:\n{task_list}\n\nХорошего дня! ✨"
            try:
                await bot.send_message(user_id, message)
            except Exception as e:
                logging.error(f"Не удалось отправить утреннюю сводку пользователю {user_id}: {e}")

async def send_task_reminder(bot: Bot, user_id: int, task_id: int, task_text: str):
    """Отправляет напоминание о задаче за час до выполнения."""
    task = get_task(task_id)
    if task and not task['is_done']:
        message = f"⏰ Напоминание! Через час задача:\n\n📝 {task_text}"
        try:
            await bot.send_message(user_id, message)
        except Exception as e:
            logging.error(f"Не удалось отправить напоминание пользователю {user_id} для задачи {task_id}: {e}")

def setup_scheduler_jobs(bot: Bot):
    """Добавляет все запланированные задачи в планировщик."""
    scheduler.add_job(send_morning_summary, 'cron', hour=9, minute=0, args=[bot])