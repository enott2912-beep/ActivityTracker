from services import task
import aiogram

router = aiogram.Router()

@router.message(aiogram.filters.Command("add"))
async def add_task_handler(message: aiogram.types.Message):
    user_id = message.from_user.id
    task_text = message.text.replace("/add", "").strip()
    if not task_text:
        await message.answer("Пожалуйста, укажите задачу после команды /add.")
        return
    task.add_task(user_id, task_text)
    await message.answer(f"Задача \"{task_text}\" добавлена в список на сегодня.")