

from aiogram.dispatcher.filters.state import StatesGroup, State


class AddProduct(StatesGroup):
    name = State()
    cost = State()
    image = State()


class EditProduct(StatesGroup):
    name = State()
    cost = State()
    image = State()
