from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.states.add_product import AddProduct
from bot.db.models import Product
from bot.misc import dp
from bot.states.admin import AdminState


@dp.message_handler(commands=['add_product'], state=AdminState.admin)
async def cmd_add_product(message: types.Message, state: FSMContext):
    await AddProduct.name.set()
    await message.answer("Введите название")


@dp.message_handler(state=AddProduct.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await AddProduct.next()
    await message.answer("Введите цену")


@dp.message_handler(state=AddProduct.cost)
async def process_cost(message: types.Message, state: FSMContext):
    await state.update_data(cost=int(message.text))

    await AddProduct.next()
    await message.answer("Отправтье изображение")


@dp.message_handler(state=AddProduct.image, content_types=['photo'])
async def process_image(message: types.Message, state: FSMContext):
    print(message.photo)
    await state.update_data(image=(await message.photo[-1].get_url()))
    await save_product(await state.get_data())
    await state.finish()
    await AdminState.admin.set()
    await message.answer("Товар успешно добавлен!")


async def save_product(data):
    product = Product(**data)
    await product.save()
