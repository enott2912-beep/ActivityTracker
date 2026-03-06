import aiogram
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

router = aiogram.Router()

def get_main_keyboard():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="📅 Задачи на сегодня"), KeyboardButton(text="🗂️ Списки задач")],
        [KeyboardButton(text="➕ Добавить задачу"), KeyboardButton(text="📊 Статистика")],
    ], resize_keyboard=True)

@router.message(aiogram.filters.Command("start"))
async def start_command_handler(message: aiogram.types.Message):
    await message.answer("👋 Добро пожаловать в Activity Tracker Bot!\n\nМеню теперь всегда внизу 👇", reply_markup=get_main_keyboard())