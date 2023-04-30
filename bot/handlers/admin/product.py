from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from bot.db.models import Product
from bot.misc import dp, bot
from bot.states.admin import AdminState


@dp.message_handler(commands=['products'], state=AdminState.admin)
async def product_list(message: types.Message, state: FSMContext):
    products = await Product.all()
    keyboard_markup = InlineKeyboardMarkup()
    for product in products:
        button = InlineKeyboardButton(f"{product.id}", callback_data=f"product_{product.id}")
        keyboard_markup.add(button)
    await message.answer("Продукты:\n\n" + "\n".join([f"{product.name}" for product in products]), reply_markup=keyboard_markup)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('product_'), state=AdminState.admin)
async def process_product_callback(callback_query: types.CallbackQuery, state: FSMContext):
    _, product_id = callback_query.data.split('_')
    product = await Product.filter(id=product_id).first()
    image = InputFile.from_url(product.image)
    caption = f"ID: {product.id}\nНазвание: {product.name}\nЦена: ${product.cost}"
    keyboard_markup = InlineKeyboardMarkup()
    edit_button = InlineKeyboardButton("Edit", callback_data=f"edit_{product.id}")
    delete_button = InlineKeyboardButton("Delete", callback_data=f"delete_{product.id}")
    keyboard_markup.row(edit_button, delete_button)
    await bot.send_photo(callback_query.from_user.id, image, caption=caption, reply_markup=keyboard_markup)


