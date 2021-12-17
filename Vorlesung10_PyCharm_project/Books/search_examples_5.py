from django.db.models import Count
from Useradmin.models import MyUser

print("----- annotate(Count()) -----")
# Objekt = MyUser
# Spontane Eigenschaft = book_count
myusers_with_counts = MyUser.objects.annotate(book_count=Count('book_created_by'))
for myuser_with_counts in myusers_with_counts:
    print(myuser_with_counts.username, ':', myuser_with_counts.book_count)
