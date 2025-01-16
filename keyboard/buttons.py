from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


main_menu = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text='Конвертировать видео в GIF')],[KeyboardButton(text='Помощь')]],
        resize_keyboard=True
    )