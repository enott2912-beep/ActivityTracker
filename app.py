import aiogram
import logging
from config import BOT_TOKEN
from handlers import start, help, add, today, done, stats, all_tasks, upcoming, overdue, analyze
import asyncio
from scheduler import scheduler, setup_scheduler_jobs

logging.basicConfig(level=logging.INFO)
bot = aiogram.Bot(token=BOT_TOKEN)
dp = aiogram.Dispatcher()

def setup_routers(dp: aiogram.Dispatcher):
    dp.include_router(start.router)
    dp.include_router(help.router)
    dp.include_router(today.router)
    dp.include_router(all_tasks.router)
    dp.include_router(upcoming.router)
    dp.include_router(overdue.router)
    dp.include_router(done.router)
    dp.include_router(add.router)
    dp.include_router(stats.router)
    dp.include_router(analyze.router)



async def main(dp: aiogram.Dispatcher):
    setup_routers(dp)

    setup_scheduler_jobs(bot)
    scheduler.start()

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main(dp))
