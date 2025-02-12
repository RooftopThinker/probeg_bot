from aiogram import types



def get_phone_number():
    buttons = [[types.KeyboardButton(text='Оставить номер', request_contact=True)]]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons, one_time_keyboard=True)
    return keyboard


def go_to_menu():
    buttons = [[types.InlineKeyboardButton(text='В меню', callback_data='gotomenu')]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def agreement():
    buttons = [[types.InlineKeyboardButton(text='Согласен', callback_data='agree')]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def check_sent_data_keyboard():
    buttons = [[types.InlineKeyboardButton(text='Всё верно✅', callback_data='allcorrect')],
               [types.InlineKeyboardButton(text='Изменить ФИО', callback_data='change_full_name')],
               [types.InlineKeyboardButton(text='Изменить email', callback_data='change_email')],
               [types.InlineKeyboardButton(text='Изменить номер телефона', callback_data='change_phone_number')],
               [types.InlineKeyboardButton(text='Изменить название компании', callback_data='change_company_name')],
               [types.InlineKeyboardButton(text='Изменить должность', callback_data='change_position')]]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def rules_and_missions():
    buttons = [[types.InlineKeyboardButton(text='Миссия и ценности сообщества', callback_data='mission')],
               [types.InlineKeyboardButton(text='Правила сообщества', callback_data='rules')]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def approve_or_decline(user_id):
    buttons = [[types.InlineKeyboardButton(text='Принять', callback_data=f'accept_{user_id}')],
               [types.InlineKeyboardButton(text='Отклонить', callback_data=f'decline_{user_id}')]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def admin_menu():
    buttons = [[types.InlineKeyboardButton(text='Статистика', callback_data='stats')], #TODO
               [types.InlineKeyboardButton(text='Рассылка', callback_data='mailing')],
               [types.InlineKeyboardButton(text="Выгрузить пользователей в Excel", callback_data='export')],
               [types.InlineKeyboardButton(text="Выгрузить пользователей в Excel", callback_data='changemissiontext')]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def cancel_admin():
    buttons = [[types.InlineKeyboardButton(text="Отмена", callbxack_data='admin_cancel')]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def yes_or_no():
    buttons = [[types.InlineKeyboardButton(text='Да✅', callback_data='yes')],
               [types.InlineKeyboardButton(text='Нет❌', callback_data='no')]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def cancel():
    buttons = [[types.InlineKeyboardButton(text="Отмена", callback_data='cancel')]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def send_request():
    buttons = [[types.InlineKeyboardButton(text="Заявка отправлена", callback_data='request')]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def application_approved():
    buttons = [[types.InlineKeyboardButton(text='Запрос одобрен✅', callback_data='_')]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def application_declined():
    buttons = [[types.InlineKeyboardButton(text='Запрос отклонён❌', callback_data='_')]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard