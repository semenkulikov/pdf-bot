from aiogram import types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from loader import dp, app_logger
from database.query_orm import (
    get_all_pdf_countries,
    get_pdf_country_by_code,
    create_pdf_country,
    get_pdf_services_by_country_id,
    get_pdf_service_by_id,
    create_pdf_service
)
from database.engine import async_session
from states.states import AdminPanel
from keyboards.inline.admin_keyboards import (
    get_admin_pdf_menu_keyboard,
    get_pdf_countries_keyboard,
    get_country_edit_keyboard,
    get_pdf_services_keyboard,
    get_service_edit_keyboard
)


async def show_pdf_admin_menu(message: types.Message, state: FSMContext):
    app_logger.info("Показ админ панели PDF.")
    keyboard = get_admin_pdf_menu_keyboard()
    await message.edit_text("Админ панель PDF:\nВыберите действие:", reply_markup=keyboard)
    await state.set_state(AdminPanel.pdf_admin_menu)

# Управление странами (PDFCountry)
@dp.callback_query(StateFilter(AdminPanel.pdf_admin_menu), F.data == "admin:pdf:countries")
async def show_pdf_countries(call: types.CallbackQuery, state: FSMContext):
    app_logger.info(f"Админ @{call.from_user.username} запросил список PDF стран.")
    countries = await get_all_pdf_countries()
    keyboard = get_pdf_countries_keyboard(countries)
    await call.message.edit_text("Список стран для PDF:", reply_markup=keyboard)
    await state.update_data(current_menu="countries")
    await call.answer()

@dp.callback_query(StateFilter(AdminPanel.pdf_admin_menu), F.data == "admin:pdf:add_country")
async def admin_add_country_prompt(call: types.CallbackQuery, state: FSMContext):
    app_logger.info(f"Админ @{call.from_user.username} выбрал добавление новой страны.")
    await call.message.edit_text(
        "Введите данные для новой страны в формате:\nНазвание;код\nПример: 🇫🇷 Франция;france"
    )
    await state.set_state(AdminPanel.add_pdf_country)
    await call.answer()

@dp.message(StateFilter(AdminPanel.add_pdf_country))
async def admin_add_country_receive(message: types.Message, state: FSMContext):
    app_logger.info(f"Админ @{message.from_user.username} вводит данные новой страны.")
    try:
        name, code = map(str.strip, message.text.split(";"))
    except ValueError:
        await message.answer("Неверный формат. Используйте формат: Название;код")
        app_logger.error("Неверный формат ввода для добавления страны.")
        return
    country = await create_pdf_country(name=name, code=code)
    await message.answer(f"Страна добавлена: {country.name} ({country.code})")
    app_logger.info(f"Страна {country.name} успешно добавлена.")
    await state.clear()
    await show_pdf_admin_menu(message, state)

@dp.callback_query(StateFilter(AdminPanel.pdf_admin_menu), F.data.startswith("admin:pdf:edit_country:"))
async def admin_edit_country_prompt(call: types.CallbackQuery, state: FSMContext):
    country_code = call.data.split(":")[-1]
    app_logger.info(f"Админ @{call.from_user.username} выбрал редактирование страны {country_code}.")
    await state.update_data(edit_country_code=country_code)
    keyboard = get_country_edit_keyboard()
    await call.message.edit_text(f"Управление страной: {country_code}\nВыберите действие:", reply_markup=keyboard)
    await call.answer()

@dp.callback_query(StateFilter(AdminPanel.pdf_admin_menu), F.data == "admin:pdf:do_edit_country")
async def admin_do_edit_country(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    country_code = data.get("edit_country_code")
    if not country_code:
        await call.answer("Ошибка: страна не выбрана.", show_alert=True)
        app_logger.error("Редактирование страны: не выбран код страны.")
        return
    app_logger.info(f"Админ @{call.from_user.username} редактирует страну {country_code}.")
    await call.message.edit_text("Введите новые данные для страны в формате:\nНазвание;код")
    await state.set_state(AdminPanel.edit_pdf_country)
    await call.answer()

@dp.message(StateFilter(AdminPanel.edit_pdf_country))
async def admin_edit_country_receive(message: types.Message, state: FSMContext):
    app_logger.info(f"Админ @{message.from_user.username} вводит новые данные для страны.")
    try:
        new_name, new_code = map(str.strip, message.text.split(";"))
    except ValueError:
        await message.answer("Неверный формат. Используйте формат: Название;код")
        app_logger.error("Неверный формат ввода при редактировании страны.")
        return
    data = await state.get_data()
    old_code = data.get("edit_country_code")
    if not old_code:
        await message.answer("Ошибка: страна не выбрана.")
        app_logger.error("Редактирование страны: отсутствует выбранная страна.")
        return
    country = await get_pdf_country_by_code(old_code)
    if not country:
        await message.answer("Страна не найдена.")
        app_logger.error(f"Страна с кодом {old_code} не найдена.")
        return
    country.name = new_name
    country.code = new_code
    async with async_session() as session:
        session.add(country)
        await session.commit()
    await message.answer(f"Страна обновлена: {new_name} ({new_code})")
    app_logger.info(f"Страна успешно обновлена: {new_name} ({new_code}).")
    await state.clear()
    await show_pdf_admin_menu(message, state)

@dp.callback_query(StateFilter(AdminPanel.pdf_admin_menu), F.data == "admin:pdf:delete_country")
async def admin_delete_country(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    country_code = data.get("edit_country_code")
    if not country_code:
        await call.answer("Ошибка: страна не выбрана.", show_alert=True)
        app_logger.error("Удаление страны: не выбран код страны.")
        return
    async with async_session() as session:
        await session.execute("DELETE FROM pdf_countries WHERE code = :code", {"code": country_code})
        await session.commit()
    await call.message.edit_text(f"Страна с кодом {country_code} удалена.")
    app_logger.info(f"Страна с кодом {country_code} удалена администратором.")
    await state.clear()
    await show_pdf_admin_menu(call.message, state)
    await call.answer()


@dp.callback_query(StateFilter(AdminPanel.pdf_admin_menu), F.data == "admin:pdf:services")
async def show_country_for_services(call: types.CallbackQuery, state: FSMContext):
    app_logger.info(f"Админ @{call.from_user.username} выбрал управление сервисами PDF.")
    countries = await get_all_pdf_countries()
    keyboard = InlineKeyboardBuilder()
    for country in countries:
        keyboard.button(text=country.name, callback_data=f"admin:pdf:select_services:{country.code}")
    keyboard.button(text="Назад", callback_data="admin:pdf:back")
    keyboard.adjust(1)
    await call.message.edit_text("Выберите страну для управления сервисами:", reply_markup=keyboard.as_markup())
    await state.update_data(current_menu="services")
    await call.answer()

@dp.callback_query(StateFilter(AdminPanel.pdf_admin_menu), F.data.startswith("admin:pdf:select_services:"))
async def admin_select_services(call: types.CallbackQuery, state: FSMContext):
    country_code = call.data.split(":")[-1]
    app_logger.info(f"Админ @{call.from_user.username} выбрал страну {country_code} для управления сервисами.")
    await state.update_data(selected_country_for_services=country_code)
    from database.query_orm import get_pdf_country_by_code, get_pdf_services_by_country_id
    country = await get_pdf_country_by_code(country_code)
    if not country:
        await call.message.edit_text("Страна не найдена.")
        app_logger.error(f"Страна {country_code} не найдена при выборе сервисов.")
        return
    services = await get_pdf_services_by_country_id(country.id)
    keyboard = get_pdf_services_keyboard(services, country.name)
    await call.message.edit_text(f"Сервисы для страны {country.name}:", reply_markup=keyboard)
    await call.answer()

@dp.callback_query(StateFilter(AdminPanel.pdf_admin_menu), F.data == "admin:pdf:add_service")
async def admin_add_service_prompt(call: types.CallbackQuery, state: FSMContext):
    app_logger.info(f"Админ @{call.from_user.username} выбрал добавление нового сервиса.")
    data = await state.get_data()
    country_code = data.get("selected_country_for_services")
    if not country_code:
        await call.answer("Страна не выбрана.", show_alert=True)
        app_logger.error("Добавление сервиса: не выбрана страна.")
        return
    await call.message.edit_text(
        "Введите данные для нового сервиса в формате:\nНазвание;JSON_поля_шаблона\nПример: Leboncoin;{\"field1\":\"Описание поля 1\", \"field2\":\"Описание поля 2\"}"
    )
    await state.set_state(AdminPanel.add_pdf_service)
    await call.answer()

@dp.message(StateFilter(AdminPanel.add_pdf_service))
async def admin_add_service_receive(message: types.Message, state: FSMContext):
    app_logger.info(f"Админ @{message.from_user.username} вводит данные для нового сервиса.")
    try:
        service_name, template_fields = map(str.strip, message.text.split(";", 1))
    except ValueError:
        await message.answer("Неверный формат. Используйте формат: Название;JSON_поля_шаблона")
        app_logger.error("Неверный формат ввода при добавлении сервиса.")
        return
    data = await state.get_data()
    country_code = data.get("selected_country_for_services")
    if not country_code:
        await message.answer("Ошибка: страна не выбрана.")
        app_logger.error("Добавление сервиса: отсутствует выбранная страна.")
        return
    country = await get_pdf_country_by_code(country_code)
    if not country:
        await message.answer("Страна не найдена.")
        app_logger.error(f"Страна {country_code} не найдена при добавлении сервиса.")
        return
    service = await create_pdf_service(name=service_name, country_id=country.id, template_fields=template_fields)
    await message.answer(f"Сервис добавлен: {service.name}")
    app_logger.info(f"Сервис {service.name} добавлен для страны {country.name}.")
    await state.clear()
    await show_pdf_admin_menu(message, state)

@dp.callback_query(StateFilter(AdminPanel.pdf_admin_menu), F.data.startswith("admin:pdf:edit_service:"))
async def admin_edit_service_prompt(call: types.CallbackQuery, state: FSMContext):
    try:
        service_id = int(call.data.split(":")[-1])
    except ValueError:
        await call.answer("Некорректный идентификатор сервиса.", show_alert=True)
        app_logger.error("Некорректный ID сервиса при редактировании.")
        return
    app_logger.info(f"Админ @{call.from_user.username} выбрал редактирование сервиса с ID {service_id}.")
    await state.update_data(edit_service_id=service_id)
    keyboard = get_service_edit_keyboard()
    await call.message.edit_text(f"Управление сервисом (ID: {service_id}). Выберите действие:", reply_markup=keyboard)
    await call.answer()

@dp.callback_query(StateFilter(AdminPanel.pdf_admin_menu), F.data == "admin:pdf:do_edit_service")
async def admin_do_edit_service(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    service_id = data.get("edit_service_id")
    if not service_id:
        await call.answer("Ошибка: сервис не выбран.", show_alert=True)
        app_logger.error("Редактирование сервиса: ID не найден.")
        return
    app_logger.info(f"Админ @{call.from_user.username} редактирует сервис с ID {service_id}.")
    await call.message.edit_text("Введите новые данные для сервиса в формате:\nНазвание;JSON_поля_шаблона")
    await state.set_state(AdminPanel.edit_pdf_service)
    await call.answer()

@dp.message(StateFilter(AdminPanel.edit_pdf_service))
async def admin_edit_service_receive(message: types.Message, state: FSMContext):
    app_logger.info(f"Админ @{message.from_user.username} вводит новые данные для сервиса.")
    try:
        new_name, new_template_fields = map(str.strip, message.text.split(";", 1))
    except ValueError:
        await message.answer("Неверный формат. Используйте формат: Название;JSON_поля_шаблона")
        app_logger.error("Неверный формат ввода при редактировании сервиса.")
        return
    data = await state.get_data()
    service_id = data.get("edit_service_id")
    if not service_id:
        await message.answer("Ошибка: сервис не выбран.")
        app_logger.error("Редактирование сервиса: отсутствует выбранный ID.")
        return
    service = await get_pdf_service_by_id(service_id)
    if not service:
        await message.answer("Сервис не найден.")
        app_logger.error(f"Сервис с ID {service_id} не найден.")
        return
    service.name = new_name
    service.template_fields = new_template_fields
    async with async_session() as session:
        session.add(service)
        await session.commit()
    await message.answer(f"Сервис обновлён: {new_name}")
    app_logger.info(f"Сервис с ID {service_id} успешно обновлён.")
    await state.clear()
    await show_pdf_admin_menu(message, state)

@dp.callback_query(StateFilter(AdminPanel.pdf_admin_menu), F.data == "admin:pdf:delete_service")
async def admin_delete_service(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    service_id = data.get("edit_service_id")
    if not service_id:
        await call.answer("Ошибка: сервис не выбран.", show_alert=True)
        app_logger.error("Удаление сервиса: отсутствует выбранный ID.")
        return
    async with async_session() as session:
        await session.execute("DELETE FROM pdf_services WHERE id = :id", {"id": service_id})
        await session.commit()
    await call.message.edit_text(f"Сервис с ID {service_id} удалён.")
    app_logger.info(f"Сервис с ID {service_id} удалён администратором.")
    await state.clear()
    await show_pdf_admin_menu(call.message, state)
    await call.answer()
