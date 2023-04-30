import asyncio

from bot.misc import setup, dp, bot, database_init


setup()
loop = asyncio.get_event_loop()
loop.create_task(dp.start_polling())
loop.create_task(database_init())
loop.run_forever()
