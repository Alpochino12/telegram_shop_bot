from tortoise import Tortoise
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from bot.core.config import config


storage = MemoryStorage()
bot = Bot(token=config.TELEGRAM_TOKEN)
dp = Dispatcher(bot, storage=storage)


async def database_init():
    db_url = f'sqlite://{config.DB_NAME}'

    await Tortoise.init(
        db_url=db_url,
        modules={'models': ['bot.db.models']}
    )


def setup():
    import bot.handlers.home
    import bot.handlers.admin.admin
    import bot.handlers.admin.add_product
    import bot.handlers.admin.edit_product
    import bot.handlers.admin.product
    import bot.handlers.product
    import bot.handlers.basket
