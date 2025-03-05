from loader import app_logger, bot


async def is_subscribed(chat_id, user_id):
    """
    Проверяет, подписан ли пользователь на канал.
    Возвращает True, если статус входит в ("creator", "administrator", "member", "restricted").
    Если user_id некорректен, возвращает False.
    """
    try:
        # Приводим user_id к целому числу, если это возможно
        user_id = int(user_id)
    except (ValueError, TypeError):
        app_logger.error(f"Некорректный user_id: {user_id}")
        return False

    try:
        result = await bot.get_chat_member(chat_id, user_id)
        if result.status in ("creator", "administrator", "member", "restricted"):
            return True
    except Exception as e:
        app_logger.error(f"Ошибка при получении информации о пользователе {user_id}: {e}")
    return False
