from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from services.task import get_overdue_tasks

router = Router()

@router.message(Command("overdue"))
async def overdue_command_handler(message: types.Message):
    await show_overdue_tasks(message, message.from_user.id)

@router.callback_query(F.data == "view_overdue")
async def view_overdue_callback_handler(callback: types.CallbackQuery):
    await show_overdue_tasks(callback.message, callback.from_user.id)
    await callback.message.delete()
    await callback.answer()

async def show_overdue_tasks(message_obj, user_id):
    tasks = get_overdue_tasks(user_id)
    if not tasks:
        await message_obj.answer("👍 Просроченных задач нет. Так держать!")
        return

    builder = InlineKeyboardBuilder()
    for t_id, t_text, t_is_done, t_date in tasks:
        builder.row(
            types.InlineKeyboardButton(text=f"{t_date[5:]}: {t_text}", callback_data=f"done_{t_id}"),
            types.InlineKeyboardButton(text="❌", callback_data=f"del_{t_id}")
        )

    await message_obj.answer("😥 Ваши просроченные задачи (нажмите, чтобы выполнить):", reply_markup=builder.as_markup())
