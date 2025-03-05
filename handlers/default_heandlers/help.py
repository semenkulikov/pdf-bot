from aiogram import types
from aiogram.filters import Command

from loader import dp
from config_data.config import DEFAULT_COMMANDS, ADMIN_COMMANDS, ALLOWED_USERS, SUPPORTED_USERS


@dp.message(Command('help'))
async def bot_help(message: types.Message):
    commands = [f"/{cmd} - {desc}" for cmd, desc in DEFAULT_COMMANDS]
    if int(message.from_user.id) in ALLOWED_USERS:
        commands.extend([f"/{cmd} - {desc}" for cmd, desc in ADMIN_COMMANDS])
    await message.reply("Доступные команды:\n" + "\n".join(commands))
    await message.answer(f"🤝 Для поддержки обращайтесь: {" ".join(SUPPORTED_USERS)}")
