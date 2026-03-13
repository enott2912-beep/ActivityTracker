import logging
from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from services.task import get_task, get_all_user_ids, get_today_active_tasks


scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

async def send_morning_summary(bot: Bot):
    """Sends morning task summary to all users."""
    user_ids = await get_all_user_ids()
    for user_id in user_ids:
        tasks = await get_today_active_tasks(user_id)
        if tasks:
            task_list = "\n".join([f"▫️ {task[1]}" for task in tasks])
            message = f"☀️ Доброе утро!\n\nЗадачи на сегодня:\n{task_list}\n\nХорошего дня! ✨"
            try:
                await bot.send_message(user_id, message)
            except Exception as e:
                logging.error(f"Failed to send morning summary to {user_id}: {e}")

async def send_task_reminder(bot: Bot, user_id: int, task_id: int, task_text: str):
    """Sends a task reminder one hour before execution."""
    task = await get_task(task_id)
    if task and not task['is_done']:
        message = f"⏰ Напоминание! Через час задача:\n\n📝 {task_text}"
        try:
            await bot.send_message(user_id, message)
        except Exception as e:
            logging.error(f"Failed to send reminder to {user_id} for task {task_id}: {e}")

def setup_scheduler_jobs(bot: Bot):
    """Adds all scheduled jobs to the scheduler."""
    scheduler.add_job(send_morning_summary, 'cron', hour=9, minute=0, args=[bot])