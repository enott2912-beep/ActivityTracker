from services import task
import aiogram


router = aiogram.Router()

@router.message(aiogram.filters.Command("today"))
async def today_command_handler(message: aiogram.types.Message):
    user_id = message.from_user.id
    tasks = task.get_tasks(user_id)
    if not tasks:
        await message.answer("На сегодня задач нет.")
        return
    
    tasks_list = "\n".join([f"- {t[0]}" for t in tasks])
    await message.answer(f"Задачи на сегодня:\n{tasks_list}")