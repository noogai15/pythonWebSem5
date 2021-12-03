from datetime import date
from django.contrib.auth.models import User
from django.test import TestCase
from .models import Book


class SubtitleTests(TestCase):
    def setUp(self):
        Book.objects.create(
            title = 'Test Title',
            subtitle = 'Test Subtitle',
            author = 'Test Author',
            pages = 123,
            date_published = date(2001,2,3),
            type = 'P',
            user = User.objects.create_user(
                username='test_user'
            ),
        )

    def test_subtitle(self):
        book = Book.objects.get(title='Test Title')
        self.assertEqual(book.subtitle, 'Test Subtitle')

    def test_get_full_title(self):
        book = Book.objects.get(title='Test Title')
        self.assertEqual(book.get_full_title(), 'Test Title: Test Subtitle')


class AuthorTest(TestCase):
    def setUp(self):
        Book.objects.create(
            title = 'Test Title 2',
            subtitle = 'Test Subtitle 2',
            author = 'Test Author 2',
            pages = 456,
            date_published = date(2004,5,6),
            type = 'H',
            user=User.objects.create_user(
                username='test_user'
            ),
        )

    def test_author(self):
        book = Book.objects.get(title='Test Title 2')
        self.assertEqual(book.subtitle.split(), ['Test', 'Subtitle', '2'])


class DatePublishedTest(TestCase):
    def setUp(self):
        Book.objects.create(
            title = 'Test Title 3',
            subtitle = 'Test Subtitle 3',
            author = 'Test Author 3',
            pages = 789,
            date_published = date(2070,8,9),
            type = 'E',
            user=User.objects.create_user(
                username='test_user'
            ),
        )

    def test_date_pubished(self):
        book = Book.objects.get(title='Test Title 3')
        self.assertFalse(book.check_date_published())
