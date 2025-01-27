import sqlalchemy
from aiogram import types
from sqlalchemy.ext.asyncio import AsyncSession
from data import get_user, User



def get_phone_number():
    buttons = [[types.KeyboardButton(text='Оставить номер', request_contact=True)]]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons, one_time_keyboard=True)
    return keyboard


async def menu(telegram_id, session, rejected=False):
    user: User = await get_user(telegram_id, session)
    buttons = [[types.KeyboardButton(text='Миссия и ценности сообщества')],
               [types.KeyboardButton(text='Правила сообщества')]]
    if user.is_accepted:
        buttons.insert(0, [types.KeyboardButton(text='Бесплатные форматы')])
        buttons.append([types.KeyboardButton(text='Членство PRO бизнес и спорт')])
    keyboard = types.ReplyKeyboardMarkup(keyboard=buttons)
    return keyboard


def agreement():
    buttons = [[types.InlineKeyboardButton(text='Согласен', callback_data='agree')]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def check_sent_data():
    buttons = [[types.InlineKeyboardButton(text='Всё верно✅', callback_data='allcorrect')],
               [types.InlineKeyboardButton(text='Изменить ФИО', callback_data='change_full_name')],
               [types.InlineKeyboardButton(text='Изменить email', callback_data='change_email')],
               [types.InlineKeyboardButton(text='Изменить номер телефона', callback_data='change_phone')]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def rules_and_missions():
    buttons = [[types.InlineKeyboardButton(text='Миссия и ценности сообщества', callback_data='mission')],
               [types.InlineKeyboardButton(text='Правила сообщества', callback_data='rules')]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard