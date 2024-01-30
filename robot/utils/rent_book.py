import logging
from asgiref.sync import sync_to_async
from robot.models import Book, Status, TelegramUser
from robot.utils.get_user import get_user
async def rent_book(product, user_id):
    user = await sync_to_async(TelegramUser.objects.get)(chat_id=user_id)
    
    product = await sync_to_async(Book.objects.get)(pk=product)
    print(f"user: {user}")
    print(product)

    # try:
    #     await Status.objects.create(
    #         book = product,
    #         borrower = user
    #     )
    #     return True
    # except Exception as e:
    #     logging.info("xatolik")
    #     logging.error(e)
