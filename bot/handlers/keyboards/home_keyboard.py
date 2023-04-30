from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton

home_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
home_keyboard.add(KeyboardButton('Список товаров'))
home_keyboard.add(KeyboardButton('Корзина'))
