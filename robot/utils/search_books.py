from django.db.models import Q
from asgiref.sync import sync_to_async
from robot.models import Book

@sync_to_async
def search_books(query):
    books = Book.objects.filter(
        Q(name__icontains=query) | Q(author__icontains=query)
    )
    
    result = [i for i in books]
    return result