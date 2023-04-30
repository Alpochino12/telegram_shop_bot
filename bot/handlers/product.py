from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from bot.db.models import Product
from bot.misc import dp, bot


@dp.message_handler(text='Список товаров')
async def product_list(message: types.Message, state: FSMContext):
    products = await Product.all()
    keyboard_markup = InlineKeyboardMarkup()
    for product in products:
        button = InlineKeyboardButton(f"{product.name}", callback_data=f"product_{product.id}")
        keyboard_markup.add(button)
    await message.answer("Продукты:\n\n" + "\n".join([f"{product.name}" for product in products]), reply_markup=keyboard_markup)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('product_'))
async def process_product_callback(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    basket = data.get('basket', [])
    _, product_id = callback_query.data.split('_')
    product = await Product.filter(id=product_id).first()
    image = InputFile.from_url(product.image)
    caption = f"ID: {product.id}\nНазвание: {product.name}\nЦена: ${product.cost}"
    keyboard_markup = InlineKeyboardMarkup()
    if product.id in basket:
        basket_button = InlineKeyboardButton("Удалить из корзины",
                                             callback_data=f"remove_from_basket_{product.id}")
    else:
        basket_button = InlineKeyboardButton("Добавить в корзину",
                                             callback_data=f"add_to_basket_{product.id}")
    keyboard_markup.row(basket_button)
    await bot.send_photo(callback_query.from_user.id, image, caption=caption, reply_markup=keyboard_markup)
