from services import task
import aiogram
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F, types


router = aiogram.Router()

@router.message(aiogram.filters.Command("today"))
async def today_command_handler(message: aiogram.types.Message):
    await show_today_tasks(message, message.from_user.id)

@router.message(F.text == "📅 Задачи на сегодня")
async def today_text_handler(message: aiogram.types.Message):
    await show_today_tasks(message, message.from_user.id)

async def show_today_tasks(message_obj, user_id):
    tasks = task.get_today_tasks(user_id)
    if not tasks:
        await message_obj.answer("📅 На сегодня задач нет. Отдыхайте! 🏖")
        return
    
    builder = InlineKeyboardBuilder()
    for t in tasks:
        # t[0]=id, t[1]=text, t[2]=is_done
        status = "✅" if t[2] else "     "
        builder.row(
            types.InlineKeyboardButton(text=f"{status} {t[1]}", callback_data=f"done_{t[0]}"),
            types.InlineKeyboardButton(text="❌", callback_data=f"del_{t[0]}")
        )
    
    await message_obj.answer("📅 Ваши задачи (нажмите, чтобы выполнить):", reply_markup=builder.as_markup())