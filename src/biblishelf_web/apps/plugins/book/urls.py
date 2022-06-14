from django.urls import path, include

from . import api

urlpatterns = [
    path(r'repo/<str:db_key>/book/', api.book.BookListApiView.as_view()),
    path(r'repo/<str:db_key>/book/<int:pk>/', api.book.BookRetrieveUpdateDestroyAPIView.as_view()),
]