from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from services.task import add_task

router = Router()

class AddTask(StatesGroup):
    waiting_for_category = State()
    waiting_for_text = State()

@router.message(F.text == "➕ Добавить задачу")
async def start_add_process(message: types.Message, state: FSMContext):
    builder = InlineKeyboardBuilder()
    builder.button(text="🏋🏼‍♀️ Спорт", callback_data="cat_sport")
    builder.button(text="👨‍🎓 Учеба", callback_data="cat_study")
    builder.adjust(2)
    
    await message.answer("Выберите категорию:", reply_markup=builder.as_markup())
    await state.set_state(AddTask.waiting_for_category)

@router.callback_query(AddTask.waiting_for_category, F.data.startswith("cat_"))
async def category_chosen(callback: types.CallbackQuery, state: FSMContext):
    category = callback.data.split("_")[1] # sport или study
    await state.update_data(category=category)
    
    await callback.message.edit_text(f"Категория: {category}.\n✍️ Теперь напишите текст задачи:")
    await state.set_state(AddTask.waiting_for_text)
    await callback.answer()

@router.message(AddTask.waiting_for_text)
async def task_text_chosen(message: types.Message, state: FSMContext):
    if not message.text:
        await message.answer("Пожалуйста, отправьте текстовое сообщение.")
        return

    user_data = await state.get_data()
    category = user_data['category']
    task_text = message.text

    add_task(message.from_user.id, category, task_text)
    
    await message.answer(f"✅ Задача добавлена!\n📂 Категория: {category}\n📝 {task_text}")
    
    await state.clear()