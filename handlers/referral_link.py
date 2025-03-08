from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from typing import Union
router = Router()


@router.callback_query(F.data == 'referral_link')
@router.message(Command('referral_link'))
@router.message(F.text == 'Реферальная ссылка')
async def subscription(update: Union[types.CallbackQuery, types.Message], state: FSMContext):
    message = update if isinstance(update, types.Message) else update.message
    await message.answer(f"Ваша ссылка - https://t.me/TgApp2011Bot?start={update.from_user.id}")
