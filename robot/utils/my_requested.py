from robot.models import Status, TelegramUser, Book
from asgiref.sync import sync_to_async
@sync_to_async
def my_requested(owner_id):
    statuses = Status.objects.filter(book__owner__chat_id=owner_id)
    
    book_names = [status.book.name for status in statuses]
    user_fullnames = [status.borrower.full_name for status in statuses]
    
    return statuses, book_names, user_fullnames

@sync_to_async
def my_requested_item(status_id):
    statuse = Status.objects.get(id=status_id)
    return statuse
