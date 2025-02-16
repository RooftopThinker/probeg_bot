from data import User
from data.database_functions import get_user
from data.http_functions import create_payment_link
from aiogram import types


async def menu_keyboard(telegram_id, session):
    user: User = await get_user(telegram_id, session)
    buttons = [[types.KeyboardButton(text='Миссия и ценности сообщества')],
               [types.KeyboardButton(text='Правила сообщества')]]
    if user.is_accepted:
        buttons.insert(0, [types.KeyboardButton(text='Бесплатные форматы')])
        buttons.append([types.KeyboardButton(text='Членство PRO Бизнес и Спорт')])
    keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    return keyboard


async def pay_with_card(telegram_id):



