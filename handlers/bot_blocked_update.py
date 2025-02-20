import sqlalchemy
from aiogram.filters import ChatMemberUpdatedFilter, KICKED, MEMBER
from aiogram import Router
from aiogram.types import ChatMemberUpdated
from sqlalchemy.ext.asyncio import AsyncSession
from data.database_functions import get_user
from data import User
router = Router()


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def user_blocked_bot(event: ChatMemberUpdated, session: AsyncSession):
    user = await get_user(event.from_user.id, session)
    update_request = sqlalchemy.update(User).filter(User.id == user.id).values({'is_bot_blocked': True})
    await session.execute(update_request)
    await session.commit()


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=MEMBER))
async def user_unblocked_bot(event: ChatMemberUpdated, session: AsyncSession):
    user = await get_user(event.from_user.id, session)
    update_request = sqlalchemy.update(User).filter(User.id == user.id).values({'is_bot_blocked': False})
    await session.execute(update_request)
    await session.commit()

