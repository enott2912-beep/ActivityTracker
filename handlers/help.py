import aiogram

router = aiogram.Router()
@router.message(aiogram.filters.Command("help"))
async def help_command_handler(message: aiogram.types.Message):
    await message.answer("Вот команды, которые я поддерживаю:\n/start - начать работу\n/help — помощь\n/add — добавить активность\n/today — задачи на сегодня\n")


