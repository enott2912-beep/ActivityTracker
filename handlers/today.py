from services import task
import aiogram


router = aiogram.Router()

@router.message(aiogram.filters.Command("today"))
async def today_command_handler(message: aiogram.types.Message):
    user_id = message.from_user.id
    tasks = task.get_today_tasks(user_id)
    if not tasks:
        await message.answer("📅 На сегодня задач нет. Отдыхайте! 🏖")
        return
    
    tasks_list = []
    i = 1
    for t in tasks:
        status = "✅" if t[2] else "     "
        tasks_list.append(f"{status} {i}. {t[1]}")
        i += 1
    
    await message.answer(f"📅 Задачи на сегодня:\n" + "\n".join(tasks_list))