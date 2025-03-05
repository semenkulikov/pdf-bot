from aiogram import types, F
from aiogram.fsm.context import FSMContext

from keyboards.inline.inline_keyboards import is_subscribed_markup
from keyboards.reply.handlers_reply import handlers_reply
from loader import bot, dp, app_logger
from config_data.config import ALLOWED_USERS, DEFAULT_COMMANDS, ADMIN_COMMANDS, CHANNEL_ID
from database.query_orm import get_user_by_user_id, create_user, get_group_by_group_id, create_group, set_is_subscribed
from aiogram.filters import Command, StateFilter

from states.states import SubscribedState
from utils.functions import is_subscribed


@dp.message(Command('start'))
async def bot_start(message: types.Message, state: FSMContext):

    if message.chat.type == 'private':
        is_sub = True if message.from_user.id in ALLOWED_USERS else False
        cur_user = await get_user_by_user_id(str(message.from_user.id))
        if cur_user is None:
            cur_user = await create_user(
                user_id=str(message.from_user.id),
                full_name=message.from_user.full_name,
                username=message.from_user.username,
                is_premium=getattr(message.from_user, 'is_premium', None),
                is_subscribed=is_sub
            )
            app_logger.info(f"Новый пользователь: {message.from_user.full_name} — {message.from_user.username}")
        commands = [f"/{cmd} - {desc}" for cmd, desc in DEFAULT_COMMANDS]
        if int(message.from_user.id) in ALLOWED_USERS:
            commands.extend([f"/{cmd} - {desc}" for cmd, desc in ADMIN_COMMANDS])
            markup = await handlers_reply()
            await message.answer(
                f"Здравствуйте, {message.from_user.full_name}! Вы в списке администраторов бота. \n"
                f"Вам доступны следующие команды:\n" + "\n".join(commands),
                reply_markup=markup
            )
        else:
            is_subscribed_res = await is_subscribed(CHANNEL_ID, message.from_user.id)
            if is_subscribed_res:
                # Если пользователь подписан на канал, тогда ему можно пользоваться ботом.
                markup = await handlers_reply()
                await message.answer(
                    f"""🪧 Добро пожаловать в DopeGlue!

👥 Поздравляем, ты подписан на наш канал!
Генерация PDF теперь доступна для тебя! 
Ты можешь начать прямо сейчас: 👇""",
                    reply_markup=markup
                )
                await set_is_subscribed(cur_user.user_id, True)

            else:
                markup = await is_subscribed_markup()
                await message.answer("""🪧 Добро пожаловать в DopeGlue!

📡 Ой, кажется, ты не подписан на канал.
Подпишись, чтобы продолжить и получить доступ к сервису!""",
                                 reply_markup=markup
                                     )
                await set_is_subscribed(cur_user.user_id, True)
                await state.set_state(SubscribedState.subscribe)
    else:
        await message.answer(
            "Здравствуйте! Я — телеграм-бот, модератор каналов и групп. "
            "Чтобы получить больше информации, обратитесь к администратору или напишите мне в личку"
        )
        group = await get_group_by_group_id(str(message.chat.id))
        if group is None:
            await create_group(
                group_id=str(message.chat.id),
                title=message.chat.title,
                description=message.chat.description,
                bio=getattr(message.chat, 'bio', None),
                invite_link=getattr(message.chat, 'invite_link', None),
                location=getattr(message.chat, 'location', None),
                username=message.chat.username
            )
        # Также регистрируем пользователя, если его ещё нет
        cur_user = await get_user_by_user_id(str(message.from_user.id))
        if cur_user is None:
            await create_user(
                user_id=str(message.from_user.id),
                full_name=message.from_user.full_name,
                username=message.from_user.username,
                is_premium=getattr(message.from_user, 'is_premium', None)
            )
        app_logger.info(f"Новый пользователь: {message.from_user.full_name} — {message.from_user.username}")


@dp.callback_query(StateFilter(SubscribedState.subscribe))
async def is_subscribed_handler(call: types.CallbackQuery, state: FSMContext):
    """ Callback хендлер для проверки подписки """
    await call.answer()

    is_subscribed_res = await is_subscribed(CHANNEL_ID, call.from_user.id)
    if is_subscribed_res:
        app_logger.info(f"Пользователь {call.from_user.full_name} подписался на канал!")

        await set_is_subscribed(call.from_user.id, True)
        markup = await handlers_reply()
        await call.message.answer(callback_query_id=call.id,
                                  text=f"""🪧 Добро пожаловать в DopeGlue!

👥 Поздравляем, ты подписан на наш канал!
Генерация PDF теперь доступна для тебя! 
Ты можешь начать прямо сейчас: 👇""",
                                  reply_markup=markup
                                  )
        await state.clear()
    else:
        markup = await is_subscribed_markup()
        await call.message.answer(callback_query_id=call.id, text="""🪧 Добро пожаловать в DopeGlue!

📡 Ой, кажется, ты не подписан на канал.
Подпишись, чтобы продолжить и получить доступ к сервису!""",
                             reply_markup=markup
                             )
        await set_is_subscribed(call.from_user.id, True)
