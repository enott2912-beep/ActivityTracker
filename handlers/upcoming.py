from aiogram import Router, types, F
from aiogram.filters import Command
from services.task import upcoming_tasks as get_upcoming_tasks
from utils.display import show_task_list, format_dated_task

router = Router()

@router.message(Command("upcoming"))
async def upcoming_command_handler(message: types.Message):
    await show_upcoming_tasks(message, message.from_user.id)

@router.callback_query(F.data == "view_upcoming")
async def view_upcoming_callback_handler(callback: types.CallbackQuery):
    await show_upcoming_tasks(callback.message, callback.from_user.id)
    await callback.message.delete()
    await callback.answer()

async def show_upcoming_tasks(message_obj, user_id):
    await show_task_list(
        message_obj=message_obj,
        tasks_func=get_upcoming_tasks,
        user_id=user_id,
        title="🤩 Ваши предстоящие задачи (нажмите, чтобы выполнить):",
        empty_message="🤩 Предстоящих задач нет. Можно расслабиться!",
        formatter_func=format_dated_task
    )
