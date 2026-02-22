from aiogram import Router, types, F
from aiogram.filters import Command
from services.task import task_stats

router = Router()

@router.message(Command("stats"))
async def stats_command_handler(message: types.Message):
    await show_stats(message, message.from_user.id)

@router.message(F.text == "📊 Статистика")
async def stats_text_handler(message: types.Message):
    await show_stats(message, message.from_user.id)

async def show_stats(message_obj, user_id):
    try:
        total_tasks, done_tasks, by_category, progress = task_stats(user_id)
        if total_tasks == 0:
            await message_obj.answer("📭 У вас пока нет задач.")
            return

        category_text = ""
        display_map = {
            "sport": "🏋🏼‍♀️ Спорт",
            "study": "👨‍🎓 Учеба"
        }

        for cat, count in by_category:
            key = cat.lower() if cat else ""
            display_name = display_map.get(key, f"📁 {cat}")
            category_text += f"{display_name}: {count}\n"

        await message_obj.answer(f"📊 Статистика:\n\n📝 Всего задач: {total_tasks}\n✅ Выполнено: {done_tasks}\n📈 Прогресс: {progress:.1f}%\n\n{category_text}")
    except Exception as e:
        await message_obj.answer(f"⚠️ Произошла ошибка при получении статистики:\n{e}")