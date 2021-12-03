from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from . import views
from .views import CS_CommentDeleteView, CS_CommentEditForm, CS_CommentEditView

urlpatterns = [
    path("delete/", views.CS_CommentDeleteView.as_view(), name="cs-comment-delete"),
    path("edit/<int:pk>", views.CS_CommentEditView, name="cs-comment-edit"),
    path(
        "editdelete/<int:pk>", views.comment_edit_delete, name="cs-comment-edit-delete"
    ),
    path("allreports/", views.get_all_reports, name="all_reports"),
    path(
        "comments/delete-confirm/<int:pk>/",
        views.delete_comment,
        name="comment-delete-confirm",
    ),
]

# ALL COMMENTS ?
# SHOW ALL CUSTOMER SERVICE RELATED BUTTONS
#
