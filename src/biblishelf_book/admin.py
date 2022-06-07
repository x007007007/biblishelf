from django.contrib import admin
from .models import Book, BookPublishing
from django.utils.safestring import mark_safe
from django.shortcuts import resolve_url

# Register your models here.


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    readonly_fields = ('resource_url',)
    list_display = ("pk", "name", "isbn", "page_number", "info")

    def resource_url(self, obj):
        print(obj)
        change_url = resolve_url('admin:biblishelf_main_resource_change', args=(obj.resource.pk,))
        return mark_safe('<a href="%s" tager="_blank">resource:%s</a>' % (change_url, obj.resource.name))
    resource_url.short_description = 'Resource'


@admin.register(BookPublishing)
class BookPublishingAdmin(admin.ModelAdmin):
    pass

