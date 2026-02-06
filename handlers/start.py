import aiogram

router = aiogram.Router()
@router.message(aiogram.filters.Command("start"))
async def start_command_handler(message: aiogram.types.Message):
    await message.answer("Добро пожаловать Activity Tracker Bot! Скоро я помогу планировать спорт и учебу.")