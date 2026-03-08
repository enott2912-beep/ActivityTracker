from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from services.task import done_task, delete_task, get_today_tasks, get_task
import aiogram
from scheduler import scheduler
from apscheduler.jobstores.base import JobLookupError

router = Router()

def _cancel_reminder_if_exists(task_id: int):
    """Отменяет напоминание для задачи, если оно существует."""
    task = get_task(task_id)
    if task and task['reminder_job_id']:
        try:
            scheduler.remove_job(task['reminder_job_id'])
        except JobLookupError:
            pass # Работа уже была выполнена или удалена

@router.message(Command("done"))
async def done_command_handler(message: types.Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2 or not parts[1].isdigit():
        await message.answer("Пожалуйста, укажите номер задачи из списка /today.\nПример: /done 1")
        return

    task_num = int(parts[1])
    user_id = message.from_user.id

    tasks = get_today_tasks(user_id)

    if task_num < 1 or task_num > len(tasks):
        await message.answer(f"⚠️ Задача с номером {task_num} не найдена. Проверьте список через /today.")
        return

    real_task_id = tasks[task_num - 1][0]

    _cancel_reminder_if_exists(real_task_id)
    task_text = tasks[task_num - 1][1]

    if done_task(user_id, real_task_id):
        await message.answer(f"✅ Задача \"{task_text}\" выполнена! Отличная работа! 🎉")
    else:
        await message.answer(f"⚠️ Задача уже выполнена или не найдена.")

@router.callback_query(F.data.startswith("done_"))
async def done_callback_handler(callback: types.CallbackQuery):
    task_id = int(callback.data.split("_")[1])
    user_id = callback.from_user.id

    _cancel_reminder_if_exists(task_id)
    if done_task(user_id, task_id):
        await callback.answer("Отлично! Задача выполнена.")
        current_keyboard = callback.message.reply_markup.inline_keyboard
        for row in current_keyboard:
            task_button = row[0]
            if task_button.callback_data == callback.data:
                if not task_button.text.startswith("✅"):
                    task_button.text = "✅ " + task_button.text.lstrip()
                break
        try:
            await callback.message.edit_reply_markup(reply_markup=callback.message.reply_markup)
        except aiogram.exceptions.TelegramBadRequest:
            pass
    else:
        await callback.answer("Задача уже выполнена или не найдена.", show_alert=True)

@router.callback_query(F.data.startswith("del_"))
async def delete_callback_handler(callback: types.CallbackQuery):
    task_id = int(callback.data.split("_")[1])
    user_id = callback.from_user.id

    _cancel_reminder_if_exists(task_id)
    if delete_task(user_id, task_id):
        await callback.answer("Задача удалена.")
        current_keyboard = callback.message.reply_markup.inline_keyboard
        new_keyboard_rows = [row for row in current_keyboard if row[1].callback_data != callback.data]

        if not new_keyboard_rows:
            await callback.message.edit_text("Задач в этом списке больше нет.")
        else:
            new_markup = types.InlineKeyboardMarkup(inline_keyboard=new_keyboard_rows)
            await callback.message.edit_reply_markup(reply_markup=new_markup)
    else:
        await callback.answer("Ошибка удаления.", show_alert=True)
