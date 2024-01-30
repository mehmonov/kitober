from aiogram import types


menu  = types.ReplyKeyboardMarkup(
    keyboard=[
        [
            types.KeyboardButton('Kitob joylash ➕ '),
            types.KeyboardButton('Biz haqimizda 👁️'),
        ],
        [
            types.KeyboardButton("Kitob qidirish 📘"),
            types.KeyboardButton("Profil 👤"),
        ],
            
    ],
        resize_keyboard=True,
)
