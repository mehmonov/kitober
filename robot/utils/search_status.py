from robot.models import Status, TelegramUser, Book
from asgiref.sync import sync_to_async
@sync_to_async
def search_status(query):
        books = Status.objects.filter(
            borrower=query
        )
        book_name = []
        user_fullname =[]
        for book in books:
            
            user_fullname.append(book.borrower.full_name)
            book_name.append(book.book.name)
             
        result = [i for i in books]
        return result, book_name, user_fullname