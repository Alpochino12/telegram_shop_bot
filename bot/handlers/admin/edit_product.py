from aiogram import types
from aiogram.dispatcher import FSMContext
from bot.db.models import Product
from bot.handlers.keyboards.change_product_keyboard import change_product_keyboard
from bot.misc import dp
from bot.states.add_product import EditProduct
from bot.states.admin import AdminState


async def update_product(data: dict):
    product = await Product.filter(id=data['product_id']).first()
    await product.update_from_dict(data)
    await product.save()


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('edit_'), state=AdminState.admin)
async def edit_product(callback_query: types.CallbackQuery, state: FSMContext):
    await EditProduct.name.set()
    await state.update_data(product_id=int(callback_query.data.split('_')[1]))
    await callback_query.message.answer('Введите новое название', reply_markup=change_product_keyboard)


@dp.message_handler(state=EditProduct.name)
async def process_name(message: types.Message, state: FSMContext):
    if message.text != 'Пропустить':
        await state.update_data(name=message.text)
    await EditProduct.next()
    await message.answer("Введите новую цену", reply_markup=change_product_keyboard)


@dp.message_handler(state=EditProduct.cost)
async def process_cost(message: types.Message, state: FSMContext):
    print(message.text)
    print(message.text != 'Пропустить')
    if message.text != 'Пропустить':
        await state.update_data(cost=int(message.text))
    await EditProduct.next()
    await message.answer("Отправьте изображение", reply_markup=change_product_keyboard)


@dp.message_handler(state=EditProduct.image, content_types=['photo', 'text'])
async def process_image(message: types.Message, state: FSMContext):
    if message.text != 'Пропустить':
        await state.update_data(image=(await message.photo[-1].get_url()))
    await update_product(await state.get_data())
    await state.finish()
    await AdminState.admin.set()
    await message.answer("Товар был успешно изменен.")


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('delete_'), state=AdminState.admin)
async def process_delete_callback(callback_query: types.CallbackQuery, state: FSMContext):
    print('deleting')
    _, product_id = callback_query.data.split('_')
    product = await Product.filter(id=product_id).first()
    await product.delete()
    await callback_query.message.answer("Товар удален")
