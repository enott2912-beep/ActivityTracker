import aiogram

router = aiogram.Router()
@router.message(aiogram.filters.Command("start"))
async def start_command_handler(message: aiogram.types.Message):
    await message.answer("👋 Добро пожаловать в Activity Tracker Bot!\n\nЯ помогу тебе планировать спорт и учебу. 🚀\nИспользуй /help, чтобы узнать команды.")