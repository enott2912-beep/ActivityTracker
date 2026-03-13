from aiogram import Router, F, types
from aiogram.filters import Command
from services import task
from utils.display import show_task_list, format_today_task

router = Router()

@router.message(Command("today"))
async def today_command_handler(message: types.Message):
    await show_today_tasks(message, message.from_user.id)

@router.message(F.text == "📅 Задачи на сегодня")
async def today_text_handler(message: types.Message):
    await show_today_tasks(message, message.from_user.id)

@router.callback_query(F.data == "view_today")
async def view_today_callback_handler(callback: types.CallbackQuery):
    await show_today_tasks(callback.message, callback.from_user.id)
    await callback.message.delete()
    await callback.answer()

async def show_today_tasks(message_obj, user_id):
    # Button to launch analysis directly from the task list
    analyze_btn = types.InlineKeyboardButton(text="🧠 AI Анализ", callback_data="analyze_productivity")
    
    await show_task_list(
        message_obj=message_obj,
        tasks_func=task.get_today_tasks,
        user_id=user_id,
        title="📅 Ваши задачи (нажмите, чтобы выполнить):",
        empty_message="📅 На сегодня задач нет. Отдыхайте! 🏖",
        formatter_func=format_today_task,
        extra_buttons=[analyze_btn]
    )