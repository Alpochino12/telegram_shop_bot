from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.core.config import config
from bot.misc import dp
from bot.states.admin import AdminState


@dp.message_handler(commands=['admin'], state='*')
async def admin(message: types.Message, state: FSMContext):
    if message.from_user.id != config.ADMIN_ID:
        return
    await AdminState.admin.set()
    await message.answer('success')
