from django.urls import path, include

from . import api

urlpatterns = [
    path(r'repo/<str:db>/book/', api.book.BookListApiView.as_view()),
]