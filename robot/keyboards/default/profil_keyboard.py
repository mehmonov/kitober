from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

pr = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Mening kitoblarim"),
        ],
        [
            KeyboardButton("So'rov yuborgan kitoblarim"),
        ],
        [
            KeyboardButton("Menga kelgan so'rovlar"),
        ],
        [
            KeyboardButton('Bosh menyu')
        ]
    ],
    resize_keyboard=True
)