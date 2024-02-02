from loader import dp
from aiogram import types
from robot.keyboards.default.menu import menu
from robot.keyboards.default.profil_keyboard import pr
from robot.models import Status, TelegramUser, Book
from asgiref.sync import sync_to_async
from robot.utils.search_status import search_status
from robot.utils.search_status_obj import search_status_obj
from robot.utils.my_requested import my_requested
from robot.utils.my_requested import my_requested_item
from loader import bot
from robot.utils.get_book import get_book

@dp.message_handler(text="Profil 👤")
async def profil(message: types.Message):
    await message.answer("Profilga hush kelibsiz. Quyidagi bo'limlardan foydalaning", reply_markup=pr)
    

@dp.message_handler(text='Mening kitoblarim')
async def my_books(message: types.Message):
    telegram_user = await TelegramUser.objects.aget(chat_id=message.from_user.id)
    books = await sync_to_async(list)(Book.objects.filter(owner=telegram_user))
    i_kb = types.InlineKeyboardMarkup()
    for book in books:
        button = types.InlineKeyboardButton(book.name, callback_data=f"bookinfo_{book.pk}")
        i_kb.add(button)
    await message.answer("sizning kitoblaringiz", reply_markup=i_kb)

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('bookinfo'))
async def my_books_info(query: types.CallbackQuery):
    book_id = query.data.split('_')[1]  
    book = await get_book(id=book_id)
    
    post = f"📚 <b>Kitob</b>: {book.name}\n"
    post += f"👨‍🏫 <b>Muallifi</b>: {book.author}\n"  
    post += f"🏷️ <b>Janr</b>: {book.genre}\n"  
    post += f"📝 <b>Tavsif</b>: <i>{book.desc} </i>\n"
    if book.image !=None or '':
        await query.message.answer_photo(photo=book.image, caption=post, parse_mode='HTML', reply_markup=pr)
    else:
        await query.message.answer(text=post, parse_mode='HTML', reply_markup=pr)





@dp.message_handler(text='So\'rov yuborgan kitoblarim')
async def my_books_status(message: types.Message):
    telegram_user = await TelegramUser.objects.aget(chat_id=message.from_user.id)
    result, book_name, user_fullname = await search_status(telegram_user)

    keyboard = types.InlineKeyboardMarkup()
    for name, r in zip(book_name, result):
        keyboard.add(types.InlineKeyboardButton(name, callback_data=f"status_{r.pk}"))

    await message.answer("Sizning kitoblaringiz:", reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('status'))
async def get_status(query: types.CallbackQuery):
    status_id = query.data.split('_')[1]  
    status = await search_status_obj(status_id)

    # Wrap synchronous calls in sync_to_async
    book_name = await sync_to_async(lambda: status.book.name)()
    author = await sync_to_async(lambda: status.book.author)()
    genre = await sync_to_async(lambda: status.book.genre)()
    desc = await sync_to_async(lambda: status.book.desc)()
    borrowed_date = await sync_to_async(lambda: status.borrowed_date)()
    return_date = await sync_to_async(lambda: status.return_date)()
    provision = await sync_to_async(lambda: status.provision)()
    owner = await sync_to_async(lambda: status.book.owner.full_name)()
    location = await sync_to_async(lambda: status.book.owner.location)()
    username = await sync_to_async(lambda: status.book.owner.username)()

    post = f"📚 <b>Kitob</b>: {book_name}\n"
    post += f"👨‍🏫 <b>Muallifi</b>: {author}\n"  
    post += f"🏷️ <b>Janr</b>: {genre}\n"  
    post += f"📝 <b>Tavsif</b>: <i>{desc} </i>\n"
    post += f"<b>---------------</b>\n"
    post += f"⏰ <b>Ijaraga olingan vaqt</b>: <i>{borrowed_date.strftime('%Y-%m-%d %H:%M:%S')} </i>\n"
    post += f"👨‍🏫 <b>Ijara bergan inson</b>: <i>{owner} </i>\n"
    if status.status == 'rejected':
        post += f"🧩 <b>Holat</b>: <i>Rad etilgan</i>\n"
    elif status.status == 'requested':
        post += f"🧩 <b>Holat</b>: <i>So'ralgan</i>\n"
    elif status.status == 'accepted':
        post += f"🧩 <b>Holat</b>: <i>Qabul qilingan</i>\n"
 
    elif status.status == 'completed':
        post += f"🧩 <b>Holat</b>: <i>Tugallangan</i>\n"

    post += f"🔮 <b>Qaytarish muddati</b>: <i>{return_date.strftime('%Y-%m-%d %H:%M:%S')} </i>\n"
    if provision == 'self':
        post += f"🧲 <b>Yetkazish sharti</b>: <i>O'zim yetkazaman </i>\n"
    
    elif provision ==  'post':
        post += f"🧲 <b>Yetkazish sharti</b>: <i>Pochta orqali </i>\n"
    
    elif provision == 'pickup':
        post += f"🧲 <b>Yetkazish sharti</b>: <i>O'zingiz kelib olib ketasiz</i>\n"
        
    if status.status == 'accepted':
        post += f"📍 <b>Manzil</b>: <i>{location}</i>\n"
        post += f"<b>Username</b>: <i>{username}</i>\n"
        
        
    if status.book.image != None or '':
        await query.message.answer_photo(photo=status.book.image, caption=post, parse_mode='HTML', reply_markup=pr)
    else:
        await query.message.answer(text=post, parse_mode='HTML', reply_markup=pr)

@dp.message_handler(text="Menga kelgan so'rovlar")
async def my_requestes(message: types.Message):
    statuses, book_names, user_fullnames = await my_requested(message.from_user.id)

    keyboard = types.InlineKeyboardMarkup()
    
    for i, (book_name, user_fullname) in enumerate(zip(book_names, user_fullnames), start=1):
        callback_data = f"myrequested_{statuses[i-1].pk}"  
        button_text = f"{i}. {book_name} - {user_fullname}"
        keyboard.add(types.InlineKeyboardButton(button_text, callback_data=callback_data))

    await message.answer("Sizga kelgan so'rovlar", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('myrequested'))
async def get_status(query: types.CallbackQuery):
    status_id = query.data.split('_')[1]  
    status = await search_status_obj(status_id)

    # Wrap synchronous calls in sync_to_async
    book_name = await sync_to_async(lambda: status.book.name)()
    author = await sync_to_async(lambda: status.book.author)()
    genre = await sync_to_async(lambda: status.book.genre)()
    desc = await sync_to_async(lambda: status.book.desc)()
    borrowed_date = await sync_to_async(lambda: status.borrowed_date)()
    return_date = await sync_to_async(lambda: status.return_date)()
    provision = await sync_to_async(lambda: status.provision)()
    owner = await sync_to_async(lambda: status.book.owner.full_name)()
    location = await sync_to_async(lambda: status.book.owner.location)()
    username = await sync_to_async(lambda: status.book.owner.username)()

    post = f"📚 <b>Kitob</b>: {book_name}\n"
    post += f"👨‍🏫 <b>Muallifi</b>: {author}\n"  
    post += f"🏷️ <b>Janr</b>: {genre}\n"  
    post += f"📝 <b>Tavsif</b>: <i>{desc} </i>\n"
    post += f"<b>---------------</b>\n"
    post += f"⏰ <b>Ijaraga olingan vaqt</b>: <i>{borrowed_date.strftime('%Y-%m-%d %H:%M:%S')} </i>\n"
    post += f"👨‍🏫 <b>Ijara bergan inson</b>: <i>{owner} </i>\n"
    if status.status == 'rejected':
        post += f"🧩 <b>Holat</b>: <i>Rad etilgan</i>\n"
    elif status.status == 'requested':
        post += f"🧩 <b>Holat</b>: <i>So'ralgan</i>\n"
    elif status.status == 'accepted':
        post += f"🧩 <b>Holat</b>: <i>Qabul qilingan</i>\n"
 
    elif status.status == 'completed':
        post += f"🧩 <b>Holat</b>: <i>Tugallangan</i>\n"

    post += f"🔮 <b>Qaytarish muddati</b>: <i>{return_date.strftime('%Y-%m-%d %H:%M:%S')} </i>\n"
    if provision == 'self':
        post += f"🧲 <b>Yetkazish sharti</b>: <i>O'zim yetkazaman </i>\n"
    
    elif provision == 'post':
        post += f"🧲 <b>Yetkazish sharti</b>: <i>Pochta orqali </i>\n"
    
    elif provision == 'pickup':
        post += f"🧲 <b>Yetkazish sharti</b>: <i>O'zingiz kelib olib ketasiz</i>\n"
        
    if status.status == 'accepted':
        post += f"📍 <b>Manzil</b>: <i>{location}</i>\n"
        post += f"<b>Username</b>: <i>{username}</i>\n"
        
        
    post += f"<b>-------------------</b>\n\n\n"
    if status.status == 'accepted' or status.status == 'rejected' or status.status == 'completed':
        await query.message.answer("Bu kitob bilan allaqachon nimadir sodir bo'lgan")
       
    else:
        post += f"<i>Ushbu userga ijaraga berasizmi kitobni? quyidagi tugmalar orqali tasdiqlang</i>\n"

        inline_keyboard = types.InlineKeyboardMarkup(row_width=2)
        inline_keyboard.add(
            types.InlineKeyboardButton("Ha", callback_data=f"confirm_{status.pk}"),
            types.InlineKeyboardButton("Yo'q", callback_data=f"reject_{status.pk}")
        )

        if status.book.image != None or '':
            await query.message.answer_photo(photo=status.book.image, caption=post, parse_mode='HTML', reply_markup=inline_keyboard)
        else:
            await query.message.answer(post, parse_mode='HTML', reply_markup=inline_keyboard)
    
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('confirm'))
async def accept_or_reject(query: types.CallbackQuery): 
    status_id = query.data.split('_')[1]  
    status = await sync_to_async(Status.objects.get)(id=status_id)
    status.status = 'accepted'
    
    await sync_to_async(status.save)()
    book_name = await sync_to_async(lambda: status.book.name)()
    chat_id = await sync_to_async(lambda: status.borrower.chat_id)()
    await bot.send_message(chat_id=chat_id, text=f"Sizni kitobingiz tasdiqlandi! \n\nKitob: {book_name}")
    await query.message.answer("Ajoyib, kitob tasdiqlandi")
    
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('reject'))
async def accept_or_reject(query: types.CallbackQuery): 
    status_id = query.data.split('_')[1]  
    status = await sync_to_async(Status.objects.get)(id=status_id)
    book_name = await sync_to_async(lambda: status.book.name)()
    
    chat_id = await sync_to_async(lambda: status.borrower.chat_id)()
    await bot.send_message(chat_id=chat_id, text=f"Sizni kitobingiz tasdiqlanmadi! \n\nKitob: {book_name}")
    
    await query.message.answer("Ajoyib, bu habarni yetkazamiz")
    