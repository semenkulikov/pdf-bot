from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


async def handlers_reply() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="📂 Генерация PDF")
    kb.button(text="🏆 Мой аккаунт")
    kb.button(text="⭐️ Избранное")
    kb.button(text="🧩 Помощь")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True, input_field_placeholder="Выберите одну из кнопок")
