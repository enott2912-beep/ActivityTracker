import aiogram
from config import BOT_TOKEN
from handlers import start
import asyncio

bot = aiogram.Bot(token=BOT_TOKEN)
dp = aiogram.Dispatcher()

def setup(dp: aiogram.Dispatcher):
    dp.include_router(start.router)

async def main(dp: aiogram.Dispatcher):
    setup(dp)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main(dp))
