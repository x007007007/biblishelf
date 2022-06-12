from django.contrib import admin
from .models import BookModel, BookPublishing
from django.utils.safestring import mark_safe
from django.shortcuts import resolve_url

# Register your models here.

@admin.register(BookModel)
class BookAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "isbn", "page_number", "info")



@admin.register(BookPublishing)
class BookPublishingAdmin(admin.ModelAdmin):
    pass
