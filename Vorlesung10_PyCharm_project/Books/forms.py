from django import forms
from .models import Book, Comment


class BookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = ['title', 'subtitle', 'author', 'type', 'pages', 'date_published']
        widgets = {
            'type': forms.Select(choices=Book.BOOK_TYPES),
            'myuser': forms.HiddenInput(),
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'myuser': forms.HiddenInput(),
            'book': forms.HiddenInput(),
        }


class SearchForm(forms.ModelForm):

    title = forms.CharField(required=False)

    class Meta:
        model = Book
        fields = ['author', 'title']
