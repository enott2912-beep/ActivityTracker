from aiogram import Router, types, F
from aiogram.filters import Command
from services.task import get_user_activity_summary, calculate_streak
from services.ai_service import analyze_productivity

router = Router()

async def run_analysis(message_obj: types.Message, user_id: int):
    """Общая функция для запуска анализа (из команды или кнопки)."""
    # 1. Получаем статистику
    summary_data = get_user_activity_summary(user_id)
    streak = calculate_streak(user_id)

    if not summary_data or summary_data['total_tasks'] == 0:
        await message_obj.answer("📊 У вас еще нет задач для анализа. Добавьте несколько и попробуйте снова!")
        return

    # Дополняем данные для AI
    data_for_ai = {
        "total_tasks": summary_data['total_tasks'],
        "done_tasks": summary_data['done_tasks'],
        "categories": summary_data['categories'],
        "tasks": summary_data['tasks'],
        "streak": streak,
    }

    # 2. Отправляем в AI
    msg = await message_obj.answer("⏳ Анализирую вашу продуктивность... Подождите немного.")
    analysis_text = await analyze_productivity(data_for_ai)

    # 3. Выводим ответ
    response_text = (
        "📊 Анализ продуктивности\n\n"
        f"{analysis_text}"
    )

    await msg.edit_text(response_text)

@router.message(Command("analyze"))
async def analyze_command_handler(message: types.Message):
    await run_analysis(message, message.from_user.id)

@router.message(F.text == "🧠 AI Анализ")
async def analyze_text_handler(message: types.Message):
    await run_analysis(message, message.from_user.id)

@router.callback_query(F.data == "analyze_productivity")
async def analyze_callback_handler(callback: types.CallbackQuery):
    await callback.answer()
    await run_analysis(callback.message, callback.from_user.id)
