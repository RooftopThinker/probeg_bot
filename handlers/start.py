import sqlalchemy
from aiogram import Router, F, types
from aiogram.filters import CommandStart
from sqlalchemy.ext.asyncio import AsyncSession
from data import User, Application, Referral
from data.database_functions import get_user
from aiogram.fsm.context import FSMContext
from .fsm import RegisterUser
import re
from keyboards.all_keyboards import get_phone_number, agreement, approve_or_decline, check_sent_data_keyboard, \
    go_to_menu
from keyboards.functionable_keyboards import menu_keyboard
from typing import Union
from config import ADMINS_CHAT_ID, NEW_TOPIC_ID, SYSADMIN_ID
from data.http_functions import new_lead
router = Router()


@router.message(F.text == 'Вернуться в меню')
@router.message(CommandStart())
async def start_handler(update: Union[types.Message, types.CallbackQuery], state: FSMContext, session: AsyncSession):
    request = sqlalchemy.select(User).filter(User.telegram_id == update.from_user.id)
    result = list(await session.scalars(request))
    message = update if isinstance(update, types.Message) else update.message
    if not result:
        await message.answer(text='Отлично! Теперь пройди короткую регистрацию. Укажи свой номер',
                             reply_markup=get_phone_number())
        await state.set_state(RegisterUser.fetch_number)
        try:
            referral_id = message.text[7:]
            request = sqlalchemy.select(Referral).filter(Referral.telegram_id == int(referral_id)).limit(1)
            referral: User = list(await session.scalars(request))[0]
            await state.update_data(referral_telegram_id=referral.telegram_id)
        except (AttributeError, IndexError, ValueError):
            return

        referral_request = sqlalchemy.update(Referral).filter(Referral.id == referral.id).values(
            {'people_invited': Referral.people_invited + 1})
        await session.execute(referral_request)
        await session.commit()
    else:
        if not result[0].full_name:
            await state.set_state(RegisterUser.fetch_full_name)
            await message.answer('Закончи регистрацию. Отправь свои ФИО')
            return
        await message.answer('Меню', reply_markup=await menu_keyboard(update.from_user.id, session))


@router.message(RegisterUser.fetch_number, F.content_type == types.ContentType.CONTACT)
async def fetch_number(message: types.Message, session: AsyncSession, state: FSMContext):
    username = '@' + message.from_user.username if message.from_user.username else None
    name = message.from_user.full_name
    phone_number = message.contact.phone_number
    id = message.from_user.id
    referral_telegram_id = await state.get_value(key='referral_telegram_id', default=None)
    new_user = User(telegram_name=name, telegram_username=username, phone_number=phone_number, telegram_id=id,
                    invited_by=referral_telegram_id)
    session.add(new_user)
    await session.commit()
    await message.answer('Мы получили твой номер. Теперь отправь свои ФИО')
    await state.set_state(RegisterUser.fetch_full_name)


@router.message(RegisterUser.fetch_full_name)
async def fetch_full_name(message: types.Message, state: FSMContext):
    await state.update_data(full_name=message.text.capitalize())
    await message.answer('Отправь название своей компании')
    await state.set_state(RegisterUser.fetch_company_name)


@router.message(RegisterUser.fetch_company_name)
async def fetch_company_name(message: types.Message, state: FSMContext):
    await state.update_data(company_name=message.text)
    await message.answer('Твоя роль/должность в компании?')
    await state.set_state(RegisterUser.fetch_position)


@router.message(RegisterUser.fetch_position)
async def fetch_position(message: types.Message, state: FSMContext):
    await state.update_data(position=message.text)
    await message.answer('Укажи твой реальный e-mail на который мы будем отправлять '
                         'мероприятия в твой календарь, когда ты на них подпишешься.')
    await state.set_state(RegisterUser.fetch_email)


@router.message(RegisterUser.fetch_email)
async def fetch_email(message: types.Message, state: FSMContext):
    if not re.fullmatch("[^@]+@[^@]+\.[^@]+", message.text):
        await message.answer('Email невалидный! Попробуй ещё раз')
        return
    await state.update_data(email=message.text)
    await message.answer('Подтверди согласие на обработку персональных данных', reply_markup=agreement())
    await state.set_state(RegisterUser.agreement)


@router.callback_query(RegisterUser.agreement, F.data == 'agree')
async def agreement_handler(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    user = await get_user(callback.from_user.id, session)
    await callback.message.edit_text('Отлично, это последний шаг! Если все верно заполнено, то '
                                     'отправь заявку и присоединяйся к открытым форматам нашего сообщества!\n\n'
                                     'Твои данные:\n'
                                     f'{data['full_name']}\n'
                                     f'{user.telegram_username if user.telegram_username else
                                     "Отображаемое имя:" + user.telegram_name}\n'
                                     f'{data["email"]}\n'
                                     f'{user.phone_number if not data.get('phone_number') else data.get('phone_number')}\n'
                                     f'{data["company_name"]}\n'
                                     f'{data["position"]}\n', reply_markup=check_sent_data_keyboard()
                                     )
    await state.set_state(RegisterUser.check_sent_data)


@router.callback_query(RegisterUser.check_sent_data)
async def check_sent_data(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    if callback.data == 'allcorrect':
        data = await state.get_data()
        await callback.message.edit_text(text='Мы получили твою заявку, скоро мы ее проверим и вам станут'
                                         ' доступны открытые форматы нашего сообщества. Как все '
                                         'будет готово, мы тебе напишем! Пока ты можешь ознакомиться с ценностями сообщества,'
                                         ' нашей миссией и правилами.',
                                         reply_markup=go_to_menu())
        data['full_name'] = data['full_name'].capitalize()
        if data.get('field_to_change'):
            del data['field_to_change']
        update_request = sqlalchemy.update(User).filter(User.telegram_id == callback.from_user.id).values(data)
        await session.execute(update_request)
        user: User = await get_user(callback.from_user.id, session)
        phone_number = user.phone_number if not data.get('phone_number') else data.get('phone_number')
        text = (f'Новый лид хочет стать участником открытых форматов\n\n'
                f'ID пользователя: {user.id}\n'
                f'{data['full_name']}\n'
                f'{user.telegram_username if user.telegram_username else
                                     "Отображаемое имя:" + user.telegram_name}\n'
                f'{data["email"]}\n'
                f'{phone_number}\n'
                f'{data["company_name"]}\n'
                f'{data["position"]}\n')
        request_to_crm = new_lead(data['full_name'], phone_number, data['email'], user.telegram_id, user.telegram_username,
                        None, None, None,
                           data['company_name'], data['position'])
        referrer: User = await get_user(user.invited_by, session)
        if referrer:
            request_to_crm = new_lead(data['full_name'], phone_number, data['email'], user.telegram_id, user.telegram_username,
                           referrer.telegram_id, referrer.full_name, referrer.telegram_username,
                           data['company_name'], data['position'])

        try:
            await request_to_crm
        except Exception as e:
            await callback.bot.send_message(text='Error while accessing API to add a lead:\n' + str(e),
                                            chat_id=ADMINS_CHAT_ID)

        info = await callback.bot.send_message(chat_id=ADMINS_CHAT_ID,
                                               reply_markup=approve_or_decline(callback.from_user.id),
                                               text=text,
                                               message_thread_id=NEW_TOPIC_ID)
        application = Application(message_id=info.message_id, by_user=callback.from_user.id)
        session.add(application)
        await session.commit()
        await state.clear()
        return
    field_to_change = '_'.join(callback.data.split('_')[1:])
    fields = {'full_name':'ФИО', 'email': 'Email', 'phone_number': 'Номер телефона',
              'company_name': "Название компании", 'position': 'Должность'}
    await callback.message.edit_text(f'Отправь новые данные для поля "{fields[field_to_change]}"', reply_markup=None)
    await state.update_data(field_to_change=field_to_change)
    await state.set_state(RegisterUser.change_sent_data)


@router.message(RegisterUser.change_sent_data)
async def change_sent_data(message: types.Message, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    user = await get_user(message.from_user.id, session)
    if data['field_to_change'] == 'phone_number' and \
            not re.fullmatch("^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$", message.text):
        await message.answer('Телефон указан в неверном формате. Попробуй ещё раз')
        return
    if data['field_to_change'] == 'email' and \
            not re.fullmatch("[^@]+@[^@]+\.[^@]+", message.text):
        await message.answer('Email невалидный! Попробуй ещё раз')
        return
    data[f'{data["field_to_change"]}'] = message.text
    await state.set_data(data)
    await message.answer('Отлично, теперь данные верны? Если все верно заполнено, то '
                         'отправь заявку и присоединяйся к открытым форматам нашего сообщества!\n\n'
                         'Твои данные:\n'
                         f'{data['full_name']}\n'
                         f'{user.telegram_username if user.telegram_username else
                         "Отображаемое имя:" + user.telegram_name}\n'
                         f'{data["email"]}\n'
                         f'{user.phone_number if not data.get('phone_number') else data.get('phone_number')}\n'
                         f'{data["company_name"]}\n'
                         f'{data["position"]}\n', reply_markup=check_sent_data_keyboard()
                         )
    await state.set_state(RegisterUser.check_sent_data)
