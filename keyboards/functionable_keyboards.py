import datetime

from data import User, Receipt
from data.database_functions import get_user
from data.http_functions import init_payment
from aiogram import types


async def menu_keyboard(telegram_id, session):
    user: User = await get_user(telegram_id, session)
    buttons = [[types.KeyboardButton(text='Миссия и ценности сообщества')],
               [types.KeyboardButton(text='Правила сообщества')]]
    if user.is_accepted:
        buttons.insert(0, [types.KeyboardButton(text='Бесплатные форматы')])
        buttons.append([types.KeyboardButton(text='Членство PRO Бизнес и Спорт')])
    if user.role > 0:
        buttons.insert(0, [types.KeyboardButton(text='Реферальная ссылка')])
    keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    return keyboard


async def pay_with_card(telegram_id, session):
    data, params = await init_payment(telegram_id)
    buttons = [[types.InlineKeyboardButton(text='Перейти на страницу оплаты', url=data['PaymentURL'])]]
    receipt = Receipt(telegram_id=telegram_id, order_id=params['OrderId'],
                      date=datetime.datetime.now())
    session.add(receipt)
    await session.commit()
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
