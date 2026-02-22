from aiogram import Router, types
from aiogram.filters import Command
from services.task import done_task, get_today_tasks

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
