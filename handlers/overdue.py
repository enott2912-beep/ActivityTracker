from aiogram import Router, types, F
from aiogram.filters import Command
from services.task import get_overdue_tasks
from utils.display import show_task_list, format_dated_task

router = Router()

@router.message(Command("overdue"))
async def overdue_command_handler(message: types.Message):
    await show_overdue_tasks(message, message.from_user.id)

@router.callback_query(F.data == "view_overdue")
async def view_overdue_callback_handler(callback: types.CallbackQuery):
    await show_overdue_tasks(callback.message, callback.from_user.id)
    await callback.message.delete()
    await callback.answer()

async def show_overdue_tasks(message_obj, user_id):
    await show_task_list(
        message_obj=message_obj,
        tasks_func=get_overdue_tasks,
        user_id=user_id,
        title="😥 Ваши просроченные задачи (нажмите, чтобы выполнить):",
        empty_message="👍 Просроченных задач нет. Так держать!",
        formatter_func=format_dated_task
    )
