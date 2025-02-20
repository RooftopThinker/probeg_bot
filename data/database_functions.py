from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from data import User, Application
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy
import asyncio
from config import APPROVED_TOPIC_ID, DECLINED_TOPIC_ID, ADMINS_CHAT_ID
from keyboards.all_keyboards import application_approved, application_declined


async def get_user(telegram_id: int, session: AsyncSession) -> User:
    request = sqlalchemy.select(User).filter(User.telegram_id == telegram_id)
    try:
        user: User = list(await session.scalars(request))[0]
    except IndexError:
        return None
    return user


async def delete_application_by_user_id(user_id, bot: Bot, session, approve=True):
    topic = APPROVED_TOPIC_ID if approve else DECLINED_TOPIC_ID
    request = sqlalchemy.select(Application).filter(Application.by_user == user_id)
    result: List[Application] = list(await session.scalars(request))
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
            keyboard = application_approved() if approve else application_declined()
            try:
                await bot.edit_message_reply_markup(chat_id=ADMINS_CHAT_ID, message_id=i.message_id,
                                                    reply_markup=keyboard)
            except (TelegramBadRequest, TelegramForbiddenError):
                pass
    request = sqlalchemy.delete(Application).filter(Application.by_user == user_id)
    await session.execute(request)
    await session.commit()


