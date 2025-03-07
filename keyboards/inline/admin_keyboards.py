from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_admin_main_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Управление пользователями", callback_data="admin:users")
    builder.button(text="Управление PDF", callback_data="admin:pdf")
    builder.adjust(1)
    return builder.as_markup()

def get_admin_pdf_menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Управление странами", callback_data="admin:pdf:countries")
    builder.button(text="Управление сервисами", callback_data="admin:pdf:services")
    builder.button(text="Назад", callback_data="admin:pdf:back")
    builder.adjust(1)
    return builder.as_markup()

def get_pdf_countries_keyboard(countries) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for country in countries:
        builder.button(text=country.name, callback_data=f"admin:pdf:edit_country:{country.code}")
    builder.button(text="Добавить страну", callback_data="admin:pdf:add_country")
    builder.button(text="Назад", callback_data="admin:pdf:back")
    builder.adjust(1)
    return builder.as_markup()

def get_country_edit_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Редактировать", callback_data="admin:pdf:do_edit_country")
    builder.button(text="Удалить", callback_data="admin:pdf:delete_country")
    builder.button(text="Назад", callback_data="admin:pdf:countries")
    builder.adjust(1)
    return builder.as_markup()

def get_pdf_services_keyboard(services, country_name: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for service in services:
        builder.button(text=service.name, callback_data=f"admin:pdf:edit_service:{service.id}")
    builder.button(text="Добавить сервис", callback_data="admin:pdf:add_service")
    builder.button(text="Назад", callback_data="admin:pdf:services")
    builder.adjust(1)
    return builder.as_markup()

def get_service_edit_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Редактировать", callback_data="admin:pdf:do_edit_service")
    builder.button(text="Удалить", callback_data="admin:pdf:delete_service")
    builder.button(text="Назад", callback_data="admin:pdf:services")
    builder.adjust(1)
    return builder.as_markup()
