from aiogram import types, F, Router
from handlers.fsm import ChangeMissionText
from aiogram.fsm.context import FSMContext
from keyboards.all_keyboards import cancel_admin
import aiofiles
router = Router()


@router.callback_query(F.data == 'changemissiontext')
async def start_changing_mission_text(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Пришлите изменённое сообщение', reply_markup=cancel_admin())
    await state.set_state(ChangeMissionText.change_text)


@router.message(F.text, ChangeMissionText.change_text)
async def change_mission_text(message: types.Message):
    async with aiofiles.open('static/mission.txt', 'w') as out:
        await out.write(message.text)
        await out.flush()
    await message.answer('Готово! Текст для миссии изменён')