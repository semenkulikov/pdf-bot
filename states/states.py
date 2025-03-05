from aiogram.fsm.state import StatesGroup, State


class AdminPanel(StatesGroup):
    """ FSM для админ панели """
    get_users = State()

class SubscribedState(StatesGroup):
    """ FSM для проверки подписки """
    subscribe = State()
