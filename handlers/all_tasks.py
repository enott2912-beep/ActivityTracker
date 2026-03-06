from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

@router.message(F.text == "🗂️ Списки задач")
async def all_tasks_handler(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.button(text="😥 Просроченные", callback_data="view_overdue")
    builder.button(text="📅 На сегодня", callback_data="view_today")
    builder.button(text="🤩 Предстоящие", callback_data="view_upcoming")
    builder.adjust(1)
    await message.answer("Какой список задач показать?", reply_markup=builder.as_markup())
