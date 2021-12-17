import datetime
from django.core.exceptions import ObjectDoesNotExist
from Books.models import Book

# get()
print('----- get() -----')
book = Book.objects.get(id=3)
print('id=3', book)

try:
    book = Book.objects.get(id=9999)
except ObjectDoesNotExist:
    print('id=9999, Book not found')
    book = None
print('id=9999', book)

# filter()
print('----- filter() -----')
books = Book.objects.filter(id__gt=2)

if books: # Pruefen, ob mindestens 1 Objekt gefunden ist
    print(len(books), 'yes books found')
else:
    print(len(books), 'no books found')

# exclude()
print('----- exclude() -----')
books = Book.objects.exclude(author__endswith='Cat')
print('Books found:')
for book in books:
    print(repr(book))

# Suchen verketten
print('----- verketten -----')
books = Book.objects.filter(author__endswith='Cat')\
    .filter(date_published__gt=datetime.date(2015,2,15))
print('Books found:')
for book in books:
    print(repr(book))
