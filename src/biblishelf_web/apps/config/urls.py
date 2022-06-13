from django.urls import path, include

from . import api

urlpatterns = [
    path(r'repo/', api.repo.RepoListApiView.as_view()),
    path(r'repo/<int:pk>/', api.repo.RepoRetrieveUpdateDestroyAPIView.as_view()),
]