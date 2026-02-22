import aiogram
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

router = aiogram.Router()
@router.message(aiogram.filters.Command("start"))
async def start_command_handler(message: aiogram.types.Message):
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="📅 Задачи на сегодня"), KeyboardButton(text="➕ Добавить задачу")],
        [KeyboardButton(text="📊 Статистика")]
    ], resize_keyboard=True)

    await message.answer("👋 Добро пожаловать в Activity Tracker Bot!\n\nМеню теперь всегда внизу 👇", reply_markup=kb)