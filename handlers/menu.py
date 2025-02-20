import datetime

from aiogram import types, F, Router
import aiofiles
from data.database_functions import get_user
from sqlalchemy.ext.asyncio import AsyncSession
from filters.is_accepted import IsAccepted
from keyboards.all_keyboards import send_request, payment_options
from keyboards.functionable_keyboards import menu_keyboard

router = Router()


@router.message(F.text == 'Миссия и ценности сообщества')
async def mission_of_community(message: types.Message, session: AsyncSession):
    async with aiofiles.open('static/mission.txt', mode='r', encoding='utf-8') as f:
        await message.answer(await f.read(), reply_markup=await menu_keyboard(message.from_user.id, session))


@router.message(F.text == 'Правила сообщества')
async def mission_of_community(message: types.Message, session: AsyncSession):
    async with aiofiles.open('static/rules.txt', mode='r', encoding='utf-8') as f:
        await message.answer(await f.read(), reply_markup=await menu_keyboard(message.from_user.id, session))


@router.message(F.text == 'Бесплатные форматы', IsAccepted())
async def mission_of_community(message: types.Message, session: AsyncSession):
    async with aiofiles.open('static/free.txt', mode='r', encoding='utf-8') as f:
        await message.answer(await f.read(), reply_markup=await menu_keyboard(message.from_user.id, session))


@router.message(F.text == 'Членство PRO Бизнес и Спорт', IsAccepted())
async def mission_of_community(message: types.Message, session: AsyncSession):
    user = await get_user(message.from_user.id, session)
    if not user.is_accepted_to_paid_membership and not user.subscription_till:
        await message.answer('Для оформления членства в сообществе нам '
                             'потребуется более подробная информация про '
                             'тебя и про твой бизнес. Заполнить заявку можно '
                             'по ссылке [ссылка]. После заполнения нажми '
                             'кнопку Заявка отправлена".', reply_markup=send_request())
        return
    if user.subscription_till > datetime.datetime.today():
        await message.answer('Вы уже являетесь членом сообщества! [ссылка]')

    async with aiofiles.open('static/paid_accepted.txt', mode='r', encoding='utf-8') as f:
        await message.answer(text=await f.read(), reply_markup=payment_options(message.from_user.id))


@router.callback_query(F.data == 'gotomenu')
async def show_menu(callback: types.CallbackQuery, session: AsyncSession):
    await callback.message.edit_reply_markup()
    await callback.message.answer('Меню отобразилось на Вашей клавиатуре', reply_markup=await menu_keyboard(callback.from_user.id, session))
