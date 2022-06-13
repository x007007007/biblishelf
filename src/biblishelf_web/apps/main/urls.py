from django.urls import path, include

from . import views

urlpatterns = [
    path(r'portable/storage/<str:repo_id>/<path:path>/', views.portable_static),
]