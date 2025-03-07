import os
import asyncio
from loader import bot, dp, app_logger
from utils.set_bot_commands import set_default_commands
from database.engine import engine
from database.models import Base
from config_data.config import ADMIN_ID
from utils.tasks import check_is_sub
import handlers

async def main():
    # Создание таблиц в базе данных
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    app_logger.info("Подключение к базе данных...")

    await set_default_commands()
    app_logger.info("Загрузка базовых команд...")

    me = await bot.get_me()
    app_logger.info(f"Бот @{me.username} запущен.")

    try:
        await bot.send_message(ADMIN_ID, "Бот запущен.")
    except Exception as e:
        app_logger.error(f"Ошибка при отправке сообщения администратору: {e}")

    # Запуск чекера подписки
    asyncio.create_task(check_is_sub())

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
