import datetime
from aiogram import Router, types, F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from services.task import add_task, set_reminder_job_id
from handlers.start import get_main_keyboard
from scheduler import scheduler
from scheduler import send_task_reminder

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
    
    await callback.message.edit_text(f"Категория: {category}.\n✍️ Напишите задачу. Дату и время можно указать в конце (например: Сдать отчет 25.10 15:30):")
    await state.set_state(AddTask.waiting_for_text)
    await callback.answer()

@router.message(AddTask.waiting_for_text)
async def task_text_chosen(message: types.Message, state: FSMContext, bot: Bot):
    if not message.text:
        await message.answer("Пожалуйста, отправьте текстовое сообщение.")
        return
    
    if message.text.startswith("/"):
        await message.answer("Ввод задачи отменен, так как была введена команда.", reply_markup=get_main_keyboard())
        await state.clear()
        return

    user_data = await state.get_data()
    category = user_data['category']
    
    parts = message.text.strip().split()
    task_text_parts = []
    task_date = None
    task_time = None

    for part in reversed(parts):
        if task_time is None:
            try:
                task_time = datetime.datetime.strptime(part, "%H:%M").time()
                continue
            except ValueError:
                pass
        
        if task_date is None:
            for fmt in ("%d.%m.%Y", "%d.%m"):
                try:
                    dt = datetime.datetime.strptime(part, fmt)
                    if fmt == "%d.%m":
                        dt = dt.replace(year=datetime.datetime.now().year)
                    task_date = dt.date()
                    break
                except ValueError:
                    pass
            if task_date:
                continue
        
        task_text_parts.insert(0, part)

    task_text = " ".join(task_text_parts)

    date_str = task_date.strftime('%d.%m.%Y') if task_date else "Сегодня"

    if task_time and not task_date:
        task_date = datetime.date.today()
    if not task_date:
        task_date = datetime.date.today()

    date_db = task_date.strftime("%Y-%m-%d")
    time_db = task_time.strftime("%H:%M") if task_time else None

    task_id = add_task(message.from_user.id, category, task_text, date_db, time_db)

    if task_id and task_date and task_time:
        reminder_dt = datetime.datetime.combine(task_date, task_time) - datetime.timedelta(hours=1)
        if reminder_dt > datetime.datetime.now():
            job_id = f"task_{task_id}"
            scheduler.add_job(send_task_reminder, 'date', run_date=reminder_dt,
                              args=[bot, message.from_user.id, task_id, task_text],
                              id=job_id, replace_existing=True)
            set_reminder_job_id(task_id, job_id)
    
    time_str = f"\n⏰ Время: {time_db}" if time_db else ""
    await message.answer(f"✅ Задача добавлена!\n📂 Категория: {category}\n📝 {task_text}\n📅 Дата: {date_str}{time_str}", reply_markup=get_main_keyboard())
    
    await state.clear()