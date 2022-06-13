from django.urls import path, include

from . import views

urlpatterns = [
    path(r'portable/storage/<str:db_key>/<path:path>/', views.portable_static),
    path(r'portable/download/<str:db_key>/<int:path_id>/', views.portable_path),
]