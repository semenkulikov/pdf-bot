from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config_data.config import ADMIN_ID, CHANNEL_ID

async def is_subscribed_markup() -> InlineKeyboardMarkup:
    """ Inline buttons для стартового сообщения о подписке """
    builder = InlineKeyboardBuilder()
    builder.button(text="🤝 Новостной канал", url=f"https://t.me/{CHANNEL_ID[1:]}", callback_data="1")
    builder.button(text="🔄 Проверить подписку", callback_data="2")

    builder.adjust(2)
    return builder.as_markup()
