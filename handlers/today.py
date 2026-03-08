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

@router.callback_query(F.data == "view_today")
async def view_today_callback_handler(callback: types.CallbackQuery):
    await show_today_tasks(callback.message, callback.from_user.id)
    await callback.message.delete()
    await callback.answer()

async def show_today_tasks(message_obj, user_id):
    tasks = task.get_today_tasks(user_id)
    if not tasks:
        await message_obj.answer("📅 На сегодня задач нет. Отдыхайте! 🏖")
        return
    
    builder = InlineKeyboardBuilder()
    for t_id, t_text, t_is_done, t_time in tasks:
        status = "✅" if t_is_done else "     "
        time_str = f" ({t_time})" if t_time else ""
        builder.row(
            types.InlineKeyboardButton(text=f"{status} {t_text}{time_str}", callback_data=f"done_{t_id}"),
            types.InlineKeyboardButton(text="❌", callback_data=f"del_{t_id}")
        )
    
    await message_obj.answer("📅 Ваши задачи (нажмите, чтобы выполнить):", reply_markup=builder.as_markup())