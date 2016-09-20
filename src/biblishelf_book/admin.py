from django.contrib import admin
from .models import Book, BookPublishing
# Register your models here.


class BookAdmin(admin.ModelAdmin):
    pass


class BookPublishingAdmin(admin.ModelAdmin):
    pass


admin.site.register(Book, BookAdmin)
admin.site.register(BookPublishing, BookPublishingAdmin)