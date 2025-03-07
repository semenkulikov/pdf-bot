from asyncio import sleep
from config_data.config import CHANNEL_ID
from database.query_orm import get_all_users, set_is_subscribed
from loader import app_logger, bot
from utils.functions import is_subscribed


async def check_is_sub():
    """
    Проверяет, подписаны ли пользователи, и помечает всех, кто не подписан.
    """
    while True:
        app_logger.info("Проверка пользователей...")

        # Перебираем всех пользователей
        users = await get_all_users()
        for user in users:
            sub_status = await is_subscribed(CHANNEL_ID, user.user_id)
            if sub_status:
                await set_is_subscribed(user.user_id, True)
            else:
                await set_is_subscribed(user.user_id, False)
                app_logger.info(f"Пользователь {user.full_name} не подписан на канал.")

        await sleep(5 * 60)  # проверка раз в 5 минут
