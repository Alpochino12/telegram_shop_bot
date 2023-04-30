from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot.db.models import Product
from bot.misc import dp, bot


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('add_to_basket'))
async def add_to_basket(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    basket = data.get('basket', [])
    product_id = callback_query.data.split('_')[-1]
    product = await Product.filter(id=product_id).first()
    if product.id in basket:
        await callback_query.message.answer('Товар уже в корзине')
    basket.append(product.id)
    await state.update_data(basket=basket)
    keyboard_markup = InlineKeyboardMarkup()
    basket_button = InlineKeyboardButton("Удалить из корзины",
                                         callback_data=f"remove_from_basket_{product.id}")
    keyboard_markup.row(basket_button)
    await callback_query.message.edit_reply_markup(keyboard_markup)
    await callback_query.message.answer('Добавлено в корзину')


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('remove_from_basket'))
async def remove_from_basket(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    basket = data.get('basket', [])
    product_id = callback_query.data.split('_')[-1]
    product = await Product.filter(id=product_id).first()
    if product.id not in basket:
        await callback_query.message.answer('Товара нет в корзине')
        return
    basket.remove(product.id)
    await state.update_data(basket=basket)
    keyboard_markup = InlineKeyboardMarkup()
    basket_button = InlineKeyboardButton("Добавить в корзину",
                                         callback_data=f"add_to_basket_{product.id}")
    keyboard_markup.row(basket_button)
    await callback_query.message.edit_reply_markup(keyboard_markup)
    await callback_query.message.answer('Удалено из корзины')


@dp.message_handler(text='Корзина')
async def basket_list(message: types.Message, state: FSMContext):
    data = await state.get_data()
    basket = data.get('basket', [])
    products = await Product.filter(id__in=basket).all()
    print(basket)
    keyboard_markup = InlineKeyboardMarkup()
    for product in products:
        button = InlineKeyboardButton(f"{product.name}", callback_data=f"product_{product.id}")
        keyboard_markup.add(button)
    keyboard_markup.add(InlineKeyboardButton('Очистить корзину', callback_data='clear_basket'))
    keyboard_markup.add(InlineKeyboardButton('Купить', callback_data='buy'))
    await message.answer("Корзина:\n\n" + "\n".join([f"{product.name}" for product in products]),
                         reply_markup=keyboard_markup)


@dp.callback_query_handler(lambda c: c.data and (c.data == 'clear_basket' or c.data == 'buy'))
async def finish_shoping(callback_query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    if callback_query.data == 'clear_basket':
        await callback_query.message.answer('Корзина очищена')
    elif callback_query.data == 'buy':
        await callback_query.message.answer('Куплено')
