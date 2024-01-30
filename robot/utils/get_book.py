from asgiref.sync import sync_to_async
from robot.models import Book


@sync_to_async
def get_book(id):
    book = Book.objects.get(id=id)
    return book
