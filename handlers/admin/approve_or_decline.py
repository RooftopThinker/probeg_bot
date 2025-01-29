from aiogram import Router, F, types
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy
from data import User
router = Router()

@router.callback_query(F.data.startswith('accept'))
async def approve_review(callback: types.CallbackQuery, session: AsyncSession):
    data = int(callback.data.split('_')[1])
    # await callback.message.edit_reply_markup(reply_markup=review_approved())
    await delete_review_by_user_id(data, callback.bot, session)
    request = sqlalchemy.update(User).filter(User.telegram_id == data).values()
    await session.execute(request)
    await session.commit()
    await callback.bot.send_message(text='Ваш отзыв принят! Мы начислили Вам бонусы для следующих покупок.', chat_id=data)


@router.callback_query(F.data.startswith('decline'))
async def decline_review(callback: types.CallbackQuery, session: AsyncSession):
    data = int(callback.data.split('_')[1])
    request = sqlalchemy.update(User).filter(User.telegram_id == data).values()
    await delete_review_by_user_id(data, callback.bot, session, False)
    await session.execute(request)
    await session.commit()
    await callback.bot.send_message(text='К сожалению, мы не можем принять этот отзыв.', chat_id=data)