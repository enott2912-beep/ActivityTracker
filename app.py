import aiogram
from config import BOT_TOKEN
from handlers import start, help, add, today, done, stats, all_tasks, upcoming, overdue
import asyncio

bot = aiogram.Bot(token=BOT_TOKEN)
dp = aiogram.Dispatcher()

def setup(dp: aiogram.Dispatcher):
    dp.include_router(start.router)
    dp.include_router(help.router)
    dp.include_router(today.router)
    dp.include_router(all_tasks.router)
    dp.include_router(upcoming.router)
    dp.include_router(overdue.router)
    dp.include_router(done.router)
    dp.include_router(add.router)
    dp.include_router(stats.router)


async def main(dp: aiogram.Dispatcher):
    setup(dp)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main(dp))
