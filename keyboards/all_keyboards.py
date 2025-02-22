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
    buttons = [[types.InlineKeyboardButton(text='Статистика', callback_data='stats')],
               [types.InlineKeyboardButton(text='Рассылка', callback_data='mailing')],
               [types.InlineKeyboardButton(text="Выгрузить базу данных в Excel", callback_data='export')],
               [types.InlineKeyboardButton(text="Изменить текст миссии", callback_data='changemissiontext')]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def cancel_admin():
    buttons = [[types.InlineKeyboardButton(text="Отмена", callback_data='admin_cancel')]]
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
    buttons = [[types.InlineKeyboardButton(text="Заявка отправлена", callback_data='request_sent')]]
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


def approve_or_decline_paid(user_id):
    buttons = [[types.InlineKeyboardButton(text='Принять', callback_data=f'paidaccept_{user_id}')],
               [types.InlineKeyboardButton(text='Отклонить', callback_data=f'paiddecline_{user_id}')]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def application_accepted(manager_username):
    buttons = [[types.InlineKeyboardButton(text=f'Обрабатывается менеджером {manager_username}', callback_data='_')]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def accept_application(telegram_id):
    buttons = [[types.InlineKeyboardButton(text='Взять заявку в работу', callback_data=f'take_{telegram_id}')]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def payment_options(telegram_id):
    buttons = [[types.InlineKeyboardButton(text='Оплатить картой', callback_data=f'paywithcard_{telegram_id}')],
               [types.InlineKeyboardButton(text='Запросить счёт на оплату', callback_data=f'request_bill_{telegram_id}')],
               [types.InlineKeyboardButton(text='Связаться с менеджером', callback_data=f'contact_{telegram_id}')]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
