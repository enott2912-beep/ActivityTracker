from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from services.task import done_task, get_today_tasks, delete_task

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
        
        tasks = get_today_tasks(user_id)
        builder = InlineKeyboardBuilder()
        for t in tasks:
            status = "✅" if t[2] else "     "
            builder.row(
                types.InlineKeyboardButton(text=f"{status} {t[1]}", callback_data=f"done_{t[0]}"),
                types.InlineKeyboardButton(text="❌", callback_data=f"del_{t[0]}")
            )
        
        await callback.message.edit_reply_markup(reply_markup=builder.as_markup())
    else:
        await callback.answer("Задача уже выполнена или не найдена.", show_alert=True)

@router.callback_query(F.data.startswith("del_"))
async def delete_callback_handler(callback: types.CallbackQuery):
    task_id = int(callback.data.split("_")[1])
    user_id = callback.from_user.id

    if delete_task(user_id, task_id):
        await callback.answer("Задача удалена.")
        # Просто удаляем сообщение, если задач больше нет, или обновляем список
        # Для простоты вызовем обновление списка, но так как мы внутри callback, 
        # проще всего перерисовать клавиатуру или удалить сообщение, если список пуст.
        # Здесь мы просто удалим текущее сообщение и пришлем новый список (или обновим текущий).
        # Самый простой способ обновить UI - удалить строку. Но edit_reply_markup требует полного списка.
        # Поэтому перерисовываем:
        
        tasks = get_today_tasks(user_id)
        if not tasks:
            await callback.message.edit_text("📅 На сегодня задач больше нет.")
        else:
            builder = InlineKeyboardBuilder()
            for t in tasks:
                status = "✅" if t[2] else "     "
                builder.row(
                    types.InlineKeyboardButton(text=f"{status} {t[1]}", callback_data=f"done_{t[0]}"),
                    types.InlineKeyboardButton(text="❌", callback_data=f"del_{t[0]}")
                )
            await callback.message.edit_reply_markup(reply_markup=builder.as_markup())
    else:
        await callback.answer("Ошибка удаления.", show_alert=True)
