from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from services.task import upcoming_tasks as get_upcoming_tasks

router = Router()

@router.message(Command("upcoming"))
async def upcoming_command_handler(message: types.Message):
    await show_upcoming_tasks(message, message.from_user.id)

@router.callback_query(F.data == "view_upcoming")
async def view_upcoming_callback_handler(callback: types.CallbackQuery):
    await show_upcoming_tasks(callback.message, callback.from_user.id)
    await callback.message.delete()
    await callback.answer()

async def show_upcoming_tasks(message_obj, user_id):
    tasks = get_upcoming_tasks(user_id)
    if not tasks:
        await message_obj.answer("🤩 Предстоящих задач нет. Можно расслабиться!")
        return

    builder = InlineKeyboardBuilder()
    for t_id, t_text, t_is_done, t_date, t_time in tasks:
        time_str = f" {t_time}" if t_time else ""
        builder.row(
            types.InlineKeyboardButton(text=f"{t_date[5:]}{time_str}: {t_text}", callback_data=f"done_{t_id}"),
            types.InlineKeyboardButton(text="❌", callback_data=f"del_{t_id}")
        )

    await message_obj.answer("🤩 Ваши предстоящие задачи (нажмите, чтобы выполнить):", reply_markup=builder.as_markup())
