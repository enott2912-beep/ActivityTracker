from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import Callable, List, Any


async def show_task_list(message_obj: types.Message,
                         tasks_func: Callable[[int], List[Any]],
                         user_id: int,
                         title: str,
                         empty_message: str,
                         formatter_func: Callable[[Any], str]):
    """
    Универсальная функция для отображения списка задач с кнопками.
    """
    tasks = tasks_func(user_id)
    if not tasks:
        await message_obj.answer(empty_message)
        return

    builder = InlineKeyboardBuilder()
    for task_data in tasks:
        task_id = task_data[0]
        text = formatter_func(task_data)
        builder.row(
            types.InlineKeyboardButton(text=text, callback_data=f"done_{task_id}"),
            types.InlineKeyboardButton(text="❌", callback_data=f"del_{task_id}")
        )

    await message_obj.answer(title, reply_markup=builder.as_markup())


def format_today_task(task_data: tuple) -> str:
    """Форматирует текст для задачи из списка 'на сегодня'."""
    _t_id, t_text, t_is_done, t_time = task_data
    status = "✅" if t_is_done else "     "
    time_str = f" ({t_time})" if t_time else ""
    return f"{status} {t_text}{time_str}"


def format_dated_task(task_data: tuple) -> str:
    """Форматирует текст для просроченной или предстоящей задачи."""
    _t_id, t_text, _t_is_done, t_date, t_time = task_data
    time_str = f" {t_time}" if t_time else ""
    return f"{t_date[5:]}{time_str}: {t_text}"