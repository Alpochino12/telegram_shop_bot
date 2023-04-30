from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from bot.handlers.keyboards.home_keyboard import home_keyboard
from bot.misc import dp


@dp.message_handler(commands=['start'], state='*')
async def home(message: Message, state: FSMContext):
    await state.finish()
    await message.answer('Добро пожаловать этот бот продает товары', reply_markup=home_keyboard)

