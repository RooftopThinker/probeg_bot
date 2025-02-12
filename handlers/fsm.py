from aiogram.fsm.state import State, StatesGroup


class RegisterUser(StatesGroup):
    fetch_number = State()
    fetch_full_name = State()
    fetch_company_name = State()
    fetch_position = State()
    fetch_email = State()
    agreement = State()
    check_sent_data = State()
    change_sent_data = State()


class SendMailing(StatesGroup):
    approve = State()
    send_mailing = State()


class ChangeMissionText(StatesGroup):
    change_text = State()
