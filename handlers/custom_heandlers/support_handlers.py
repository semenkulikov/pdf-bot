from aiogram import F, types

from config_data.config import SUPPORTED_USERS
from loader import dp


@dp.message(F.text == "🧩 Помощь")
async def support_handler(message: types.Message):
    """ Хендлер для обращения в поддержку """
    await message.answer(f"🤝 Для поддержки обращайтесь: {" ".join(SUPPORTED_USERS)}")