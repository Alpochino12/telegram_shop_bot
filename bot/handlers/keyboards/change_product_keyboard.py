from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton

change_product_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
change_product_keyboard.add(KeyboardButton('Пропустить'))
