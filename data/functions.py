from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from data import User
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy
import asyncio
from keyboards.all_keyboards import get_phone_number

async def get_user(user_id, session):
    request = sqlalchemy.select(User).filter(User.telegram_id == user_id)
    user: User = list(await session.scalars(request))[0]
    return user


async def delete_application_by_user_id(id, bot: Bot, session, approve=True):
    topic = APPROVED_TOPIC_ID if approve else DECLINED_TOPIC_ID
    request = sqlalchemy.select(Appeal).filter(Appeal.by_user == id, Appeal.is_review == True)
    result: List[Appeal] = list(await session.scalars(request))
    for i in result:
        try:
            await bot.forward_message(chat_id=ADMINS_CHAT_ID, from_chat_id=ADMINS_CHAT_ID,
                                               message_thread_id=topic, message_id=i.message_id)
            await asyncio.sleep(0.1)
        except (TelegramBadRequest, TelegramForbiddenError):
            pass
        try:
            await bot.delete_message(chat_id=ADMINS_CHAT_ID, message_id=i.message_id)
        except (TelegramBadRequest, TelegramForbiddenError):
            keyboard = review_approved() if approve else review_declined()
            try:
                await bot.edit_message_reply_markup(chat_id=ADMINS_CHAT_ID, message_id=i.message_id, reply_markup=keyboard)
            except (TelegramBadRequest, TelegramForbiddenError):
                pass
    request = sqlalchemy.delete(Appeal).filter(Appeal.by_user == id, Appeal.is_review == True)
    await session.execute(request)
    await session.commit()