from django.urls import path
from . import views

urlpatterns = [
    path('show/', views.BookListView.as_view(), name='book-list'),
    #path('show/', views.book_list, name='book-list'),
    #path('show/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('show/<int:pk>/', views.book_detail, name='book-detail'),
    path('show/<int:pk>/vote/<str:up_or_down>/', views.vote, name='book-vote'),
    path('add/', views.BookCreateView.as_view(), name='book-create'),
    path('search/', views.book_search, name='book-search'),
]
