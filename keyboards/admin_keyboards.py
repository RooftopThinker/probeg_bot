from aiogram import types


def admin_keyboard()-> types.InlineKeyboardMarkup:
    buttons = [[types.InlineKeyboardButton(text='Сформировать таблицу Excel с пользователями',
                                           callback_data='export')],
               [types.InlineKeyboardButton(text='Рассылка',
                                           callback_data='mailing')],
               [types.InlineKeyboardButton(text='Изменить текст миссий',
                                           callback_data='changemissiontext')]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard