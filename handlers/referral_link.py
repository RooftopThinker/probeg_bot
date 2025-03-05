from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
router = Router()


@router.callback_query(F.data == 'referral_link')
@router.callback_query(Command('referral_link'))
async def subscription(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(f"Ваша ссылка - https://t.me/TgApp2011Bot?start={callback.from_user.id}")
