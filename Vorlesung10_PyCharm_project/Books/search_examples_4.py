from django.db.models import Avg, Max, Min
from Books.models import Book

print("----- count() -----")
book_count = Book.objects.count()
print(book_count)

print("----- filter().count() -----")
book_filter_count = Book.objects.filter(author__contains='Cat').count()
print(book_filter_count)

print("----- aggregate(Avg()) -----")
book_avg = Book.objects.all().aggregate(Avg('pages'))
print(book_avg)

print("----- aggregate(Max()) -----")
book_max = Book.objects.all().aggregate(Max('pages'))
print(book_max)

print("----- aggregate(Min()) -----")
book_min = Book.objects.all().aggregate(Min('pages'))
print(book_min)
