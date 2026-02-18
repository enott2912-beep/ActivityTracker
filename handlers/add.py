from aiogram import Router, types
from aiogram.filters import Command
from services.task import add_task

router = Router()

@router.message(Command("add"))
async def add_command_handler(message: types.Message):
    parts = message.text.split(maxsplit=2)
    
    if len(parts) < 3:
        await message.answer("Пожалуйста, укажите категорию и задачу.\nПример: /add sport Пробежка 5 км")
        return

    category = parts[1]
    task_text = parts[2]
    
    add_task(message.from_user.id, category, task_text)
    await message.answer(f"Добавлена активность в категорию '{category}': {task_text}")