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
