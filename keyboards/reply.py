from aiogram import types

get_file = types.ReplyKeyboardMarkup(
    keyboard=[
        [
            types.KeyboardButton(text="Загрузить файл"),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
    )
