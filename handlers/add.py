import datetime
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from services.task import add_task
from handlers.start import get_main_keyboard

router = Router()

class AddTask(StatesGroup):
    waiting_for_category = State()
    waiting_for_text = State()

@router.message(F.text == "➕ Добавить задачу")
async def start_add_process(message: types.Message, state: FSMContext):
    builder = InlineKeyboardBuilder()
    builder.button(text="🏋🏼‍♀️ Спорт", callback_data="cat_sport")
    builder.button(text="👨‍🎓 Учеба", callback_data="cat_study")
    builder.button(text="📁 Другое", callback_data="cat_other")
    builder.adjust(2)
    
    await message.answer("Выберите категорию:", reply_markup=builder.as_markup())
    await state.set_state(AddTask.waiting_for_category)

@router.callback_query(AddTask.waiting_for_category, F.data.startswith("cat_"))
async def category_chosen(callback: types.CallbackQuery, state: FSMContext):
    category = callback.data.split("_")[1]
    await state.update_data(category=category)
    
    await callback.message.edit_text(f"Категория: {category}.\n✍️ Напишите задачу и дату (например: Сдать отчет 25.10):")
    await state.set_state(AddTask.waiting_for_text)
    await callback.answer()

@router.message(AddTask.waiting_for_text)
async def task_text_chosen(message: types.Message, state: FSMContext):
    if not message.text:
        await message.answer("Пожалуйста, отправьте текстовое сообщение.")
        return
    
    # Если пользователь ввел команду (например /start), отменяем добавление
    if message.text.startswith("/"):
        await message.answer("Ввод задачи отменен, так как была введена команда.", reply_markup=get_main_keyboard())
        await state.clear()
        return

    user_data = await state.get_data()
    category = user_data['category']
    full_text = message.text.strip()
    task_text = full_text
    task_date = None

    parts = full_text.split()
    if len(parts) > 1:
        possible_date = parts[-1]
        for fmt in ("%d.%m.%Y", "%d-%m-%Y", "%Y-%m-%d", "%d.%m"):
            try:
                dt = datetime.datetime.strptime(possible_date, fmt)
                if fmt == "%d.%m":
                    dt = dt.replace(year=datetime.datetime.now().year)
                task_date = dt.strftime("%Y-%m-%d")
                task_text = " ".join(parts[:-1])
                break
            except ValueError:
                pass

    add_task(message.from_user.id, category, task_text, task_date)
    
    date_str = task_date if task_date else "Сегодня"
    await message.answer(f"✅ Задача добавлена!\n📂 Категория: {category}\n📝 {task_text}\n📅 Дата: {date_str}", reply_markup=get_main_keyboard())
    
    await state.clear()