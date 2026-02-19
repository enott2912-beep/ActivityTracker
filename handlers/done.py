from aiogram import Router, types
from aiogram.filters import Command
from services.task import done_task

router = Router()

@router.message(Command("done"))
async def done_command_handler(message: types.Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2 or not parts[1].isdigit():
        await message.answer("Пожалуйста, укажите ID задачи.\nПример: /done 1")
        return

    task_id = int(parts[1])
    user_id = message.from_user.id

    if done_task(user_id, task_id):
        await message.answer(f"✅ Задача {task_id} выполнена! Отличная работа! 🎉")
    else:
        await message.answer(f"⚠️ Задача с ID {task_id} не найдена или уже выполнена.")
