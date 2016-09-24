from django.contrib import admin
from .models import Book, BookPublishing
from django.utils.safestring import mark_safe
from django.core import urlresolvers

# Register your models here.


class BookAdmin(admin.ModelAdmin):
    readonly_fields = ('resource', 'resource_url')
    list_display = ("pk", "name", "resource", "isbn", "page_number", "info")

    def resource_url(self, obj):
        print(obj)
        change_url = urlresolvers.reverse('admin:biblishelf_main_resource_change', args=(obj.resource.pk,))
        return mark_safe('<a href="%s" tager="_blank">resource:%s</a>' % (change_url, obj.resource.name))
    resource_url.short_description = 'Resource'


class BookPublishingAdmin(admin.ModelAdmin):
    pass


admin.site.register(Book, BookAdmin)
admin.site.register(BookPublishing, BookPublishingAdmin)