from aiogram import Router, F, types, Dispatcher
from filters.is_a_member_of_admin_chat import IsAdmin
from data import User
import sqlalchemy
import datetime
from sqlalchemy.ext.asyncio import AsyncSession
router = Router()


@router.callback_query(F.data == 'stats', IsAdmin())
async def stats(callback: types.CallbackQuery, session: AsyncSession):
    alive_users = await session.scalar(sqlalchemy.select(sqlalchemy.func.count(User.id).filter(User.is_bot_blocked == False)))
    all_users = await session.scalar(sqlalchemy.select(sqlalchemy.func.count(User.id)))
    users_registered = await session.scalar(sqlalchemy.select(sqlalchemy.func.count(User.id).filter(
            User.full_name != None,
            User.full_name != ''
        )
    ))

    users_in_paid_membership = await session.scalar(sqlalchemy.select(sqlalchemy.func.count(User.id).filter(
            User.subscription_till != None,
            User.subscription_till >= datetime.datetime.today()
        )
    ))

    users_applied = await session.scalar(sqlalchemy.select(sqlalchemy.func.count(User.id).filter(User.applied_to_paid_membership == True)))
    users_approved = await session.scalar(sqlalchemy.select(sqlalchemy.func.count(User.id).filter(User.is_accepted_to_paid_membership == True)))
    await callback.message.answer(f'Живых пользователей: {alive_users} из {all_users},\n'
                                  f'Зарегестрировшихся пользователей: {users_registered} из {all_users},\n\n'
                                  f'Пользователей, подавших заявку на платное членство: {users_applied},\n'
                                  f'Из них допущено: {users_approved},\n'
                                  f'Сейчас состоит в платном сообществе: {users_in_paid_membership}')
