import sqlalchemy
from aiogram import types, F, Router
import aiofiles
from sqlalchemy.ext.asyncio import AsyncSession
from filters.is_accepted import IsAccepted
from data.database_functions import get_user
from data import Application, User
from config import ADMINS_CHAT_ID, NEW_TOPIC_ID
from keyboards.all_keyboards import approve_or_decline_paid, accept_application, application_accepted
from keyboards.functionable_keyboards import pay_with_card
from data.utils import get_formatted_date

router = Router()


@router.callback_query(F.data == 'request_sent')
async def notify_managers(callback: types.CallbackQuery, session: AsyncSession):
    await callback.message.edit_text('Спасибо! Мы уже взяли в работу вашу заявку и совсем скоро вернёмся с решением.')
    user = await get_user(callback.from_user.id, session)
    text = (f'Участник заполнил заявку на вступление в платное сообщество\n\n'
            f'ID пользователя: {user.id}\n'
            f'{user.full_name}\n'
            f'{user.telegram_username if user.telegram_username else
            "Отображаемое имя:" + user.telegram_name}\n'
            f'{user.email}\n'
            f'{user.phone_number}\n'
            f'{user.company_name}\n'
            f'{user.position}\n')
    update_request = sqlalchemy.update(User).filter(User.id == user.id).values({'applied_to_paid_membership': True})
    await session.execute(update_request)
    info = await callback.bot.send_message(chat_id=ADMINS_CHAT_ID,
                                           reply_markup=approve_or_decline_paid(callback.from_user.id),
                                           text=text,
                                           message_thread_id=NEW_TOPIC_ID)
    application = Application(message_id=info.message_id, by_user=callback.from_user.id)
    session.add(application)
    await session.commit()


@router.callback_query(F.data.startswith('contact_'))
async def contact_requested(callback: types.CallbackQuery, session: AsyncSession):
    data = int(callback.data.split('_')[1])
    user = await get_user(data, session)
    text = (f'Участник интересуется вступлением в сообщество и просит связаться с ним!\n\n'
            f'ID пользователя: {user.id}\n'
            f'{user.full_name}\n'
            f'{user.telegram_username if user.telegram_username else
            "Отображаемое имя:" + user.telegram_name}\n'
            f'{user.email}\n'
            f'{user.phone_number}\n'
            f'{user.company_name}\n'
            f'{user.position}\n\n'
            'Пожалуйста, свяжитесь с ним в течение 30 минут')

    info = await callback.bot.send_message(chat_id=ADMINS_CHAT_ID,
                                           reply_markup=accept_application(),
                                           text=text,
                                           message_thread_id=NEW_TOPIC_ID)
    application = Application(message_id=info.message_id, by_user=callback.from_user.id)
    session.add(application)
    await session.commit()


@router.callback_query(F.data == 'take')
async def application_taken(callback: types.CallbackQuery, session: AsyncSession):
    data = int(callback.data.split('_')[1])
    user = await get_user(data, session)
    text = (f'Заявка "связаться с пользователем" принята в работу менеджером {callback.from_user.username} \n\n'
            f'Дата: {get_formatted_date()}'
            f'ID пользователя: {user.id}\n'
            f'{user.full_name}\n'
            f'{user.telegram_username if user.telegram_username else
            "Отображаемое имя:" + user.telegram_name}\n'
            f'{user.email}\n'
            f'{user.phone_number}\n'
            f'{user.company_name}\n'
            f'{user.position}\n\n')

    await callback.message.edit_text(reply_markup=application_accepted(callback.from_user.username), text=text)


@router.callback_query(F.data.startswith('request_bill_'))
async def bill_requested(callback: types.CallbackQuery, session: AsyncSession):
    data = int(callback.data.split('_')[1])
    user = await get_user(data, session)
    text = (f'Участник запросил счет на оплату по Б/Н\n\n'
            f'ID пользователя: {user.id}\n'
            f'{user.full_name}\n'
            f'{user.telegram_username if user.telegram_username else
            "Отображаемое имя:" + user.telegram_name}\n'
            f'{user.email}\n'
            f'{user.phone_number}\n'
            f'{user.company_name}\n'
            f'{user.position}\n\n')

    info = await callback.bot.send_message(chat_id=ADMINS_CHAT_ID,
                                           reply_markup=accept_application(),
                                           text=text,
                                           message_thread_id=NEW_TOPIC_ID)
    application = Application(message_id=info.message_id, by_user=callback.from_user.id)
    session.add(application)
    await session.commit()


@router.callback_query(F.data.startswith('paywithcard_'))
async def bill_requested(callback: types.CallbackQuery, session: AsyncSession):
    await callback.message.edit_text(text='Для оплаты картой нажмите на кнопку ↓',
                                     reply_markup=await pay_with_card(callback.from_user.id, session))
