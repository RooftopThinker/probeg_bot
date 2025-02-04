from aiogram import types, F, Router
import aiofiles
router = Router()


@router.callback_query(F.data == 'changemissiontext')
async def change_mission_text(callback: types.CallbackQuery):
    await callback.message.edit_text('Пришлите изменённое сообщение')