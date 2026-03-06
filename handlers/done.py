from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from services.task import done_task, delete_task, get_today_tasks
import aiogram

router = Router()

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
    task_text = tasks[task_num - 1][1]

    if done_task(user_id, real_task_id):
        await message.answer(f"✅ Задача \"{task_text}\" выполнена! Отличная работа! 🎉")
    else:
        await message.answer(f"⚠️ Задача уже выполнена или не найдена.")

@router.callback_query(F.data.startswith("done_"))
async def done_callback_handler(callback: types.CallbackQuery):
    task_id = int(callback.data.split("_")[1])
    user_id = callback.from_user.id

    if done_task(user_id, task_id):
        await callback.answer("Отлично! Задача выполнена.")
        
        # Обновляем клавиатуру, не перерисовывая весь список
        current_keyboard = callback.message.reply_markup.inline_keyboard
        for row in current_keyboard:
            # Предполагаем, что кнопка для выполнения - первая в ряду
            task_button = row[0]
            if task_button.callback_data == callback.data:
                # Обновляем текст кнопки, добавляя галочку
                if not task_button.text.startswith("✅"):
                    task_button.text = "✅ " + task_button.text.lstrip()
                break
        try:
            await callback.message.edit_reply_markup(reply_markup=callback.message.reply_markup)
        except aiogram.exceptions.TelegramBadRequest:
            # Сообщение не изменено (например, повторное нажатие)
            pass
    else:
        await callback.answer("Задача уже выполнена или не найдена.", show_alert=True)

@router.callback_query(F.data.startswith("del_"))
async def delete_callback_handler(callback: types.CallbackQuery):
    task_id = int(callback.data.split("_")[1])
    user_id = callback.from_user.id

    if delete_task(user_id, task_id):
        await callback.answer("Задача удалена.")
        current_keyboard = callback.message.reply_markup.inline_keyboard
        new_keyboard_rows = [row for row in current_keyboard if row[1].callback_data != callback.data]

        if not new_keyboard_rows:
            await callback.message.edit_text("Задач в этом списке больше нет.")
        else:
            new_markup = InlineKeyboardBuilder(markup=new_keyboard_rows)
            await callback.message.edit_reply_markup(reply_markup=new_markup.as_markup())
    else:
        await callback.answer("Ошибка удаления.", show_alert=True)
