from django.urls import path
from . import views

urlpatterns = [
    path('show/', views.computer_list, name='computer-list'),
    path('show/<int:pk>/', views.computer_detail, name='computer-detail'),
    path('add/', views.computer_create, name='computer-create'),
]