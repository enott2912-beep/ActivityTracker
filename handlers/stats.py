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
        total_tasks, done_tasks, by_category, progress, overdue_count = task_stats(user_id)
        if total_tasks == 0:
            await message_obj.answer("📭 У вас пока нет задач.")
            return

        category_text = ""
        display_map = {
            "sport": "🏋🏼‍♀️ Спорт",
            "study": "👨‍🎓 Учеба",
            "other": "📁 Другое"
        }

        for cat, count in by_category:
            key = cat.lower() if cat else ""
            display_name = display_map.get(key, f"📁 {cat}")
            category_text += f"{display_name}: {count}\n"

        stats_text = (
            f"📊 Статистика:\n\n"
            f"📝 Всего задач: {total_tasks}\n"
            f"✅ Выполнено: {done_tasks}\n"
            f"😥 Просрочено: {overdue_count}\n"
            f"📈 Прогресс: {progress:.1f}%\n\n"
            f"{category_text}"
        )
        await message_obj.answer(stats_text)
    except Exception as e:
        await message_obj.answer(f"⚠️ Произошла ошибка при получении статистики:\n{e}")