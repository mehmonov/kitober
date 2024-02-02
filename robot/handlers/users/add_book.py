from aiogram import types
from aiogram.dispatcher import FSMContext
from robot.keyboards.default.menu import menu
from robot.states.add_book import AddBook
from loader import dp, bot
from robot.models import Book, TelegramUser

from robot.keyboards.default.cancel import cs
from aiogram.dispatcher.filters import Text

@dp.message_handler(text="Kitob joylash ➕")
async def add_book(message: types.Message, state: FSMContext):
    
    await AddBook.name.set()
    await message.answer("Ajoyib! \n\n Siz bilan hozir yangi kitob joylaymiz. Bizga kitob haqidagi ma'lumotlarni kiritishingiz kerak. Biz esa ularni boshqa foydalanuvchilarga ko'rsatamiz. Siz ham yangi kitoblarni ijaraga olishingiz mumkin. \n\n Demak boshladik-mi?  \nIltimos, Kitob nomini kiriting",reply_markup=cs)


@dp.message_handler(state=AddBook.name)
async def add_book(message: types.Message, state: FSMContext):
    await AddBook.next()
    await message.answer("Ajoyib. Endi esa kitob muallifini kiriting",reply_markup=cs)

    await state.update_data(name=message.text)



@dp.message_handler(state=AddBook.author)
async def add_book(message: types.Message, state: FSMContext):
    await AddBook.next()

    await message.answer("Iltimos, kitob janrini kiriting", )
    await state.update_data(author=message.text)

@dp.message_handler(state=AddBook.genre)
async def add_book(message: types.Message, state: FSMContext):
    await AddBook.next()

    await message.answer("Kitob haqida biroz ma'lumot yozing. Nima sababdan almashmoqchisiz, kitob holati qanday?")
    await state.update_data(genre=message.text)

@dp.message_handler(state=AddBook.desc)
async def add_book(message: types.Message, state: FSMContext):
    await AddBook.next()

    await message.answer("Iltimos, kitobni rasmini joylang. Iloji boricha sifatliroq rasm joylashingizni tavsiya qilamiz")
    await state.update_data(desc=message.text)


from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


@dp.message_handler(state=AddBook.image, content_types=types.ContentType.PHOTO)
async def add_book(message: types.Message, state: FSMContext):


    # Agar rasm jo'natilsa, uning ID sini olish
    photo_id = message.photo[-1].file_id
    await state.update_data(image=photo_id)

    # Ma'lumotlarni olish
    book = await state.get_data()

    # Kitob ma'lumotlarini tuzib chiqish
    check_post = f"📚 <b>Kitob</b>: {book['name']}\n"
    check_post += f"👨‍🏫 <b>Muallifi</b>: {book['author']}\n"  
    check_post += f"🏷️ <b>Janr</b>: {book['genre']}\n"  
    check_post += f"📝 <b>Tavsif</b>: <i>{book['desc']} </i>\n"


    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    # Tugmalar
    confirm_button = KeyboardButton("Tasdiqlash ✅")
    retry_button = KeyboardButton("Bekor qilish")

    # Tugmalarni keyboardga qo'shish
    keyboard.add(confirm_button, retry_button)

    # Xabarni yuborish va tugmani qo'shish
    await message.answer_photo(photo=book['image'], caption=check_post, parse_mode='HTML', reply_markup=keyboard)

@dp.message_handler(text='Tasdiqlash ✅', state=AddBook.image)
async def add_book(message: types.Message, state: FSMContext):
    data = await state.get_data()
    telegram_user = await TelegramUser.objects.aget(chat_id=message.from_user.id)  
    try:
        book = await Book.objects.acreate(
            name = data['name'],
            author = data['author'],
            genre = data['genre'],
            desc = data['desc'],
            owner = telegram_user,
            image = data['image']
        )   
        post = f"📚 <b>Kitob</b>: {data['name']}\n"
        post += f"👨‍🏫 <b>Muallifi</b>: {data['author']}\n"  
        post += f"🏷️ <b>Janr</b>: {data['genre']}\n"  
        post += f"📝 <b>Tavsif</b>: <i>{data['desc']} </i>\n\n"
        post += f"<b>Kitob almashing. Biz bilan qoling @kitoberUZ</b> \n"

        await bot.send_photo(chat_id="-1002078251087",photo=data['image'] , caption=post, parse_mode='HTML')

        await message.answer("Ajoyib. Biz bu kitobni  telegram kanalimiz va botga yubordik. \n\nTelegram kanalga kirish: @kitoberUZ", reply_markup=menu)

        await state.finish()
    except Exception as e:
        print(e)

        print(f"data: {data}")

@dp.message_handler(state=AddBook.author,commands='Bekor qilish')
@dp.message_handler(Text(equals='Bekor qilish', ignore_case=True),state='*')
async def add_book(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text="Mayli. Bekor qilamiz", reply_markup=menu)

