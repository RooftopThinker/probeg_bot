from aiogram import Router, F, types
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy
from sqlalchemy.util import await_fallback

from data import User
from data.functions import delete_application_by_user_id
from keyboards.functionable_keyboards import menu_keyboard
import aiofiles
router = Router()

@router.callback_query(F.data.startswith('accept'))
async def approve_request(callback: types.CallbackQuery, session: AsyncSession):
    data = int(callback.data.split('_')[1])
    # await callback.message.edit_reply_markup(reply_markup=review_approved())
    request = sqlalchemy.update(User).filter(User.telegram_id == data).values(is_accepted=True)
    await session.execute(request)
    await session.commit()
    await delete_application_by_user_id(callback.from_user.id, callback.bot, session)
    async with aiofiles.open('static/accepted.txt', mode='r', encoding='utf-8') as f:
        await callback.bot.send_message(text=await f.read(), chat_id=data, reply_markup=await menu_keyboard(data, session))


@router.callback_query(F.data.startswith('decline'))
async def decline_request(callback: types.CallbackQuery, session: AsyncSession):
    data = int(callback.data.split('_')[1])
    await delete_application_by_user_id(callback.from_user.id, callback.bot, session, False)
    await callback.bot.send_message(text='Сожалеем, но сейчас не готовы принять вас в сообщество.', chat_id=data)