from django.db.models import F
from Books.models import Book

print("----- Am Anfang -----")
book = Book.objects.get(id=3)
print('author:', book.author)
print('pages:', book.pages)

print("----- F('pages') -----")
book.pages = F('pages') + 100
book.save()
print('author:', book.author)
# print('pages:', book.pages)  # Zeigt pages als F() + Value()
print('pages:', Book.objects.get(id=3).pages)  # Zeigt pages als Zahl

print("----- author aendern -----")
book.author = 'Sleepy Cat'
book.save()
print('author:', book.author)
print('pages:', Book.objects.get(id=3).pages)
