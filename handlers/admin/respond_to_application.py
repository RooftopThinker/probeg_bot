from aiogram import Router, F, types, Dispatcher
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy
from data import Application
from asyncio import sleep
from config import ADMINS_CHAT_ID
router = Router()
# router.message.filter(IsAdmin())
router.message.filter(F.text)

@router.message(F.chat.id == int(ADMINS_CHAT_ID), F.reply_to_message)
async def answer_to_application(message: types.Message, session: AsyncSession, dispatcher: Dispatcher):
    request = sqlalchemy.select(Application).filter(Application.message_id == message.reply_to_message.message_id)
    try:
        application = list(await session.scalars(request))[0]
    except IndexError:
        return
    try:
        await message.bot.copy_message(message_id=message.message_id, from_chat_id=ADMINS_CHAT_ID,
                                   chat_id=application.by_user)
    except (TelegramBadRequest,TelegramForbiddenError):
        await message.reply(text="Сообщение не было доставлено. Скорее всего, пользователь заблокировал бота")
        return
    await message.reply('Ответ на обращение доставлен пользователю')
    await message.bot.send_message(text='Ответ на Ваше обращение🔝', chat_id=application.by_user)




