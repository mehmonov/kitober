import logging
from aiogram import types
from aiogram.dispatcher import FSMContext
from robot.keyboards.default.menu import menu
from robot.states.search_book import SearchBook
from loader import dp
from robot.models import Status
from asgiref.sync import sync_to_async
from robot.utils.get_user import get_user

from robot.utils.get_book import get_book
from robot.utils.search_books import search_books

@dp.message_handler(text="Kitob qidirish 📘")
async def search_book(message: types.Message, state: FSMContext):
    await SearchBook.name.set()
    await message.answer("Iltimos, kitob nomi yoki muallifni kiriting")

@dp.message_handler(state=SearchBook.name)
async def get_books(message: types.Message, state: FSMContext):
    query = message.text
    books = await search_books(query)
    if not books:
        await message.answer("Uzr, hech nima topilmadi.")
    user_id = message.from_user.id
    # print(user_id.pk)
    await state.update_data(user_id=user_id)
    
    i_kb = types.InlineKeyboardMarkup()
    for book in books:
        button = types.InlineKeyboardButton(book.name, callback_data=f"book_{book.pk}")
        i_kb.add(button)

        response_message = f"Sizning so'rovingiz bo'yicha {len(books)} dona kitob topdik "
        await message.answer(response_message, reply_markup=i_kb)
        await SearchBook.result.set()

@dp.callback_query_handler(state=SearchBook.result)
async def allquery(query: types.CallbackQuery, state: FSMContext):
    await SearchBook.product.set()
    
    book_id = int(query.data[5:])
    book = await get_book(book_id)

    post = f"📚 <b>Kitob</b>: {book.name}\n"
    post += f"👨‍🏫 <b>Muallifi</b>: {book.author}\n"  
    post += f"🏷️ <b>Janr</b>: {book.genre}\n"  
    post += f"📝 <b>Tavsif</b>: <i>{book.desc} </i>\n"
    i_kb = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton("Ha 💪", callback_data=f"rent_{book.pk}")
    button2 = types.InlineKeyboardButton("Yo'q 🤷‍♂️", callback_data=f"rent_")
    i_kb.add(button, button2)
    if book.image !=None or '':
        await query.message.answer_photo(photo=book.image, caption=post, parse_mode='HTML')
    else:
        await query.message.answer(text=post, parse_mode='HTML')
    
    await query.message.answer("Ushbu kitobni ijaraga olmoqchimisiz?", reply_markup=i_kb)
    
@dp.callback_query_handler(state=SearchBook.product)
async def rent(query: types.CallbackQuery, state: FSMContext):
    try:
        book_id_str = query.data[5:]
        if book_id_str:
            book_id = int(book_id_str)
            data = await state.get_data()
            user_id = data['user_id']
            # print(f"book: {book}")
          
            book = await get_book(id=book_id)
            user = await get_user(user_id)
          
            # Agar topilgan Status obyekti bor bo'lsa, uni olish
            # Kitob va user bo'yicha Status obyektini izlash yoki yaratish
            status, created = await sync_to_async(Status.objects.get_or_create)(
                book=book,
                borrower=user,
                defaults={'provision': 'post'},  
            )

            if created:
                await query.message.answer("Ajoyib, kitob uchun so'rov yuborildi. Endi javobini kutamiz", reply_markup=menu)
            
            else:
                
                if status.status == 'requested':
                    await query.message.answer("Kitob uchun avval so'rov yuborgansiz. Iltimos kuting")
                elif status.status == 'rejected':
                    await query.message.answer("Uzr, foydalanuvchi bu kitobni ijaraga berishni hohlamadi. Boshqa kitob izlab ko'ramizmi?")
                elif status.status == 'completed':
                    await query.message.answer("Iya, avval ijaraga olgan ekanmiz-ku bu kitobni.Balki boshqa kitob izlab ko'rarmiz?")
            await state.finish()
        else:
            # Agar book_id_str bo'sh bo'lsa, qandaydir xatolik yuzaga keldi.
            print("Error: book_id_str is empty.")

    except ValueError as e:
        # Agar int() funktsiyasi xatolik yuzaga kelsa.
        print(f"Error converting book_id_str to integer: {e}")

