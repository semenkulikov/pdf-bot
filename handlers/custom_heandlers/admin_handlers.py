from aiogram import types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from sqlalchemy.future import select

from config_data.config import ALLOWED_USERS
from database.engine import async_session
from database.models import User
from handlers.custom_heandlers.admin_pdf_handlers import show_pdf_admin_menu
from keyboards.inline.accounts import users_markup
from keyboards.inline.admin_keyboards import get_admin_main_keyboard
from loader import dp, app_logger
from states.states import AdminPanel


@dp.message(Command('admin_panel'))
async def admin_panel(message: types.Message, state: FSMContext):
    if int(message.from_user.id) in ALLOWED_USERS:
        app_logger.info(f"Администратор @{message.from_user.username} вошел в админ панель.")
        keyboard = get_admin_main_keyboard()
        await message.answer("Выберите режим администрирования:", reply_markup=keyboard)
        await state.set_state(AdminPanel.main)
    else:
        await message.answer("У вас недостаточно прав")


@dp.callback_query(StateFilter(AdminPanel.main), F.data == "admin:users")
async def admin_manage_users(call: types.CallbackQuery, state: FSMContext):
    app_logger.info(f"Администратор @{call.from_user.username} выбрал управление пользователями.")
    markup = await users_markup()
    await call.message.edit_text("Все пользователи базы данных:", reply_markup=markup)
    await state.set_state(AdminPanel.get_users)
    await call.answer()

@dp.callback_query(StateFilter(AdminPanel.main), F.data == "admin:pdf")
async def admin_manage_pdf(call: types.CallbackQuery, state: FSMContext):
    app_logger.info(f"Администратор @{call.from_user.username} выбрал управление PDF.")
    await show_pdf_admin_menu(call.message, state)
    await call.answer()


@dp.callback_query(StateFilter(AdminPanel.get_users))
async def admin_get_user(call: types.CallbackQuery, state: FSMContext):
    app_logger.info(f"Администратор @{call.from_user.username} получил список пользователей.")
    await call.answer()
    if call.data == "Выход":
        await call.message.answer("Вы успешно вышли из админ панели.")
        await state.clear()
        app_logger.info(f"Администратор @{call.from_user.username} вышел из админ панели.")
    else:
        async with async_session() as session:
            result = await session.execute(select(User).where(User.id == int(call.data)))
            user_obj = result.scalars().first()
        if user_obj:
            text = f"Имя: {user_obj.full_name}\nТелеграм: @{user_obj.username}\n"
            await call.message.answer(text)
            app_logger.info(f"Информация о пользователе {user_obj.username} передана администратору.")
        else:
            await call.message.answer("Пользователь не найден")
            app_logger.warning("Попытка нахождения несуществующего пользователя.")
