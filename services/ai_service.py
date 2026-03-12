from openai import AsyncOpenAI, APIStatusError
from config import DEEPSEEK_API_KEY

client = AsyncOpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com"
)

async def analyze_productivity(data):
    """
    Анализирует данные о продуктивности пользователя и возвращает текст анализа.
    """
    # Форматируем категории выполненных задач
    categories_str = "\n".join([f"{cat.capitalize()}: {count}" for cat, count in data['categories'].items()])
    if not categories_str:
        categories_str = "Пока нет выполненных задач в категориях."

    # Форматируем список всех задач
    tasks_list_str = "\n".join([f"- {'[x]' if task['is_done'] else '[ ]'} {task['text']}" for task in data['tasks']])

    prompt = f"""User productivity data:

Total tasks: {data['total_tasks']}
Completed tasks: {data['done_tasks']}
Streak: {data['streak']} days

Completed tasks by category:
{categories_str}

Full task list:
{tasks_list_str}

Give a short productivity analysis and one piece of advice in Russian. Be friendly and encouraging. Address the user directly ("Ты...").
The analysis should be based on the provided data.
"""
    
    try:
        response = await client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful productivity assistant. You analyze task data and give concise, motivating advice in Russian."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
        analysis = response.choices[0].message.content
        return analysis.strip() if analysis else "AI не смог сгенерировать ответ. Попробуйте позже."
    except APIStatusError as e:
        if e.status_code == 402:
            return "Не удалось провести анализ. На балансе вашего AI-аккаунта (DeepSeek) недостаточно средств. Пожалуйста, пополните баланс."
        return f"Не удалось провести анализ. Ошибка API: {e}"
    except Exception as e:
        return f"Не удалось провести анализ. Произошла непредвиденная ошибка: {e}"
