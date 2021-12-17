from django.db.models import Q
from Books.models import Book

print("----- title__startswith='Django' -----")
books = Book.objects.filter(
    Q(title__startswith='Django')
)
print('Books found:')
for book in books:
    print(repr(book))

print("----- title__startswith='Django' & ~author__endswith='Cat'-----")
books = Book.objects.filter(
    Q(title__startswith='Django') &
    ~Q(author__endswith='Cat')
)
print('Books found:')
for book in books:
    print(repr(book))