from aiogram import types, F
from aiogram.fsm.context import FSMContext
from loader import dp, app_logger
from keyboards.inline.pdf_keyboards import pdf_country_markup, pdf_service_markup


@dp.message(F.text == "📂 Генерация PDF")
async def pdf_generation_start(message: types.Message, state: FSMContext):
    """
    Обработчик кнопки «📂 Генерация PDF».
    Выводит пользователю клавиатуру с выбором страны.
    """
    app_logger.info(f"Пользователь {message.from_user.full_name} выбрал кнопку Генерация PDF")
    markup = await pdf_country_markup()
    await message.answer("Выберите страну для генерации PDF:", reply_markup=markup)


@dp.callback_query(F.text.startswith("country:"))
async def handle_country_selection(call: types.CallbackQuery, state: FSMContext):
    """
    Обработчик выбора страны.
    Сохраняет выбранную страну в состоянии и выводит клавиатуру для выбора сервиса.
    """
    country_code = call.data.split(":", 1)[1]
    # Сохраним выбранную страну в FSMContext для дальнейшего использования
    await state.update_data(selected_country=country_code)
    markup = await pdf_service_markup(country_code)
    if not markup.inline_keyboard:
        await call.message.edit_text("Выбранная страна не имеет доступных сервисов.")
        return
    app_logger.info(f"Пользователь {call.from_user.full_name} выбрал страну {country_code}")
    await call.message.edit_text("Выберите сервис:", reply_markup=markup)
    await call.answer()


@dp.callback_query(F.text.startswith("service:"))
async def handle_service_selection(call: types.CallbackQuery, state: FSMContext):
    """
    Обработчик выбора сервиса.
    Сохраняет выбранный сервис в состоянии и переходит к следующему этапу ввода данных для PDF.
    """
    try:
        service_id = int(call.data.split(":", 1)[1])
    except ValueError:
        await call.answer("Некорректный идентификатор сервиса.", show_alert=True)
        return

    # Сохраним выбранный сервис в состоянии
    await state.update_data(selected_service=service_id)
    app_logger.info(f"Пользователь {call.from_user.full_name} выбрал сервис {service_id}")

    # Здесь можно добавить вызов следующего шага для ввода данных,
    # например, отправку формы для заполнения полей шаблона.
    await call.message.edit_text("Сервис выбран. Введите необходимые данные для генерации PDF...")
    await call.answer()
