from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.query_orm import get_all_pdf_countries, get_pdf_country_by_code, get_pdf_services_by_country_id


async def pdf_country_markup() -> InlineKeyboardMarkup:
    """
    Формирует inline клавиатуру для выбора страны,
    используя данные из таблицы pdf_countries.
    """
    countries = await get_all_pdf_countries()
    builder = InlineKeyboardBuilder()
    for country in countries:
        builder.button(text=country.name, callback_data=f"country:{country.code}")
    builder.adjust(2)
    return builder.as_markup()

async def pdf_service_markup(country_code: str) -> InlineKeyboardMarkup:
    """
    Формирует inline клавиатуру для выбора сервиса по стране.
    Получает страну по коду, затем сервисы по её id.
    """
    country = await get_pdf_country_by_code(country_code)
    if not country:
        return InlineKeyboardMarkup(inline_keyboard=[])  # Если страна не найдена
    services = await get_pdf_services_by_country_id(country.id)
    builder = InlineKeyboardBuilder()
    for service in services:
        builder.button(text=service.name, callback_data=f"service:{service.id}")
    builder.adjust(2)
    return builder.as_markup()
