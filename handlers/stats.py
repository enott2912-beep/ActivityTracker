from aiogram import Router, types, F
from aiogram.filters import Command
from services.task import task_stats, calculate_streak

router = Router()

@router.message(Command("stats"))
async def stats_command_handler(message: types.Message):
    await show_stats(message, message.from_user.id)

@router.message(F.text == "📊 Статистика")
async def stats_text_handler(message: types.Message):
    await show_stats(message, message.from_user.id)

def _get_streak_motivation(streak: int) -> str:
    """Returns a motivational message based on streak length."""
    if streak == 0:
        return ""

    # Russian pluralization for "day"
    if streak % 10 == 1 and streak % 100 != 11:
        day_word = "день"
    elif 2 <= streak % 10 <= 4 and (streak % 100 < 10 or streak % 100 >= 20):
        day_word = "дня"
    else:
        day_word = "дней"

    message = f"🔥 Ваш стрик: {streak} {day_word}! "

    if streak <= 3:
        message += "Отличное начало!"
    elif streak <= 7:
        message += "Вы на верном пути!"
    elif streak <= 14:
        message += "Невероятно, так держать!"
    elif streak <= 30:
        message += "Вы просто машина продуктивности!"
    else:
        message += "Легендарно! Вы вошли в историю!"
    return message

async def show_stats(message_obj, user_id):
    try:
        total_tasks, done_tasks, by_category, progress, overdue_count = await task_stats(user_id)
        streak = await calculate_streak(user_id)
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

        streak_motivation = _get_streak_motivation(streak)

        stats_text = (
            f"📊 Статистика:\n\n"
            f"📝 Всего задач: {total_tasks}\n"
            f"✅ Выполнено: {done_tasks}\n"
            f"😥 Просрочено: {overdue_count}\n"
            f"📈 Прогресс: {progress:.1f}%\n"
        )
        if streak_motivation:
            stats_text += f"\n{streak_motivation}\n"
        
        stats_text += f"\n{category_text}"

        await message_obj.answer(stats_text.strip())
    except Exception as e:
        await message_obj.answer(f"⚠️ Произошла ошибка при получении статистики:\n{e}")