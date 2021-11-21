from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path("show/", views.game_list, name="game-list"),
    path("show/<int:pk>", views.game_detail, name="game-detail"),
    # path('show/<int:pk>/vote/<str:up_or_down>/', views.vote, name='game-vote'),
    path('show/<int:pk>/vote/<int:fk>/<str:up_or_down>/', views.vote, name='game-vote'),
    path("add/", views.game_create, name="game-create"),
    path("delete/<int:pk>", views.game_delete, name="game-delete"),
    # url(r'^(?P<pk>\d+)/delete/', views.game_delete, name='game-delete'),
    path("show/<int:pk>/pdf", views.game_detail_pdf, name="game-detail-pdf"),
]
