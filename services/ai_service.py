import logging
import random
from config import DEEPSEEK_API_KEY, AI_MODE, OPENAI_API_KEY

# Try importing the OpenAI library
try:
    from openai import AsyncOpenAI
    HAS_OPENAI_LIB = True
except ImportError:
    HAS_OPENAI_LIB = False

# AI Configuration
AI_CONFIG = {
    'deepseek': {
        'api_key': DEEPSEEK_API_KEY,
        'base_url': "https://api.deepseek.com",
        'model': "deepseek-chat"
    },
    'ollama': {
        'api_key': "ollama",              # Any key works for local Ollama
        'base_url': "http://localhost:11434/v1",
        'model': "phi3:mini"              # Ensure model is pulled: ollama run phi3:mini
    },
    'openai': {
        'api_key': OPENAI_API_KEY,
        'base_url': "https://api.openai.com/v1",
        'model': "gpt-3.5-turbo"
    }
}

client = None
if HAS_OPENAI_LIB and AI_MODE and AI_MODE in AI_CONFIG:
    conf = AI_CONFIG[AI_MODE]
    # Initialize client if key exists or if mode is ollama
    if conf.get('api_key') or AI_MODE == 'ollama':
        try:
            client = AsyncOpenAI(
                api_key=conf['api_key'],
                base_url=conf['base_url'],
                timeout=10.0,
                max_retries=1
            )
        except Exception as e:
            logging.error(f"AI Initialization Error ({AI_MODE}): {e}")

async def analyze_productivity(data):
    """
    Attempts to get analysis from AI.
    Falls back to simple local analysis if AI fails.
    """
    # 1. AI Attempt
    if client:
        try:
            # Build prompt
            categories_str = "\n".join([f"{cat.capitalize()}: {count}" for cat, count in data['categories'].items()]) or "Нет"
            tasks_str = "\n".join([f"- {'[x]' if t['is_done'] else '[ ]'} {t['text']}" for t in data['tasks']])
            
            prompt = (
                f"Данные:\nВсего: {data['total_tasks']}, Сделано: {data['done_tasks']}, Стрик: {data['streak']}\n"
                f"Категории:\n{categories_str}\nЗадачи:\n{tasks_str}\n\n"
                "Дай краткий мотивирующий анализ продуктивности и 1 полезный совет на русском. Обращайся на 'ты'."
            )

            response = await client.chat.completions.create(
                model=AI_CONFIG[AI_MODE]['model'],
                messages=[
                    {"role": "system", "content": "Ты помощник по продуктивности. Отвечай кратко и по делу на русском."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            logging.warning(f"⚠️ AI ({AI_MODE}) unavailable or error: {e}. Switching to simple algorithm.")
            # Fallthrough to _simple_analysis

    # 2. Fallback
    return _simple_analysis(data)

def _simple_analysis(data):
    """Simple logic without Neural Networks."""
    total = data['total_tasks']
    done = data['done_tasks']
    streak = data['streak']
    
    if total == 0:
        return "Пока нечего анализировать. Добавь пару задач!"

    percent = (done / total) * 100

    # 1. Formulate analysis
    analysis_lines = []
    if percent == 100:
        analysis_lines.append("🚀 Фантастика! Ты выполнил(а) абсолютно все задачи.")
    elif percent >= 75:
        analysis_lines.append("🔥 Отличный результат! Большая часть дел сделана.")
    elif percent >= 50:
        analysis_lines.append("👍 Хороший темп. Половина пути уже пройдена.")
    else:
        analysis_lines.append("🌱 Начало положено. Главное — не останавливаться.")

    if streak > 3:
        analysis_lines.append(f"Твой стрик составляет {streak} дн. Это мощная дисциплина!")
    elif streak > 0:
        analysis_lines.append(f"Ты держишь ритм уже {streak} дн.")
    else:
         analysis_lines.append("Попробуй выполнять задачи каждый день, чтобы набить стрик!")

    advices = [
        "Совет: Сложные задачи лучше делать с утра (""съешь лягушку"").",
        "Совет: Используй метод Pomodoro: 25 минут работы, 5 минут отдыха.",
        "Совет: Если задача занимает меньше 2 минут — сделай её прямо сейчас.",
        "Совет: Не забывай пить воду и делать разминку для глаз.",
        "Совет: Разбивай большие задачи на маленькие подзадачи.",
        "Совет: Хвали себя даже за небольшие победы!",
        "Совет: Планируй следующий день с вечера, чтобы утром сразу начать.",
        "Совет: Убери телефон в другую комнату, когда нужна концентрация."
    ]
    
    random_advice = random.choice(advices)
    
    return f"{' '.join(analysis_lines)}\n\n💡 {random_advice}"
    
