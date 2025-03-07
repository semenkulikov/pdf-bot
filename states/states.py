from aiogram.fsm.state import StatesGroup, State


class AdminPanel(StatesGroup):
    """ FSM для админ панели """
    main = State()
    get_users = State()
    pdf_admin_menu = State()
    add_pdf_country = State()
    edit_pdf_country = State()
    add_pdf_service = State()
    edit_pdf_service = State()

class SubscribedState(StatesGroup):
    """ FSM для проверки подписки """
    subscribe = State()
