from aiogram import types, Bot
from aiogram.filters import Filter
from sqlalchemy.ext.asyncio import AsyncSession

from data import User
from data.database_functions import get_user


class IsAccepted(Filter):
    async def __call__(self, message: types.Message, bot: Bot, session: AsyncSession):
        user: User = await get_user(message.from_user.id, session)
        if user.is_accepted:
            return True
        return False