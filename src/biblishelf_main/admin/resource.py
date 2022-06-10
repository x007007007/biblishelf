import os
import re

from django.contrib import admin
from django.utils.safestring import mark_safe
from biblishelf_main.models import ResourceModel


@admin.register(ResourceModel)
class ResourceModelAdmin(admin.ModelAdmin):
    readonly_fields = (
        'size',
        'sha1',
        'md5',
        'ed2k_hash',
        'mime_type',
        # 'show_all_resource_path',
    )
    search_fields = ('md5', 'sha1', 'mime_type')
    list_display = ('md5', 'sha1', 'size')
    list_filter = ('mime_type',)

    # def show_all_resource_path(self, obj):
    #     rm_list = []
    #     for rm in obj.Map.all():
    #         change_url = urlresolvers.reverse('admin:biblishelf_main_resourcemap_change', args=(rm.pk,))
    #         rm_list.append(
    #             '<a href="{}" tager="_blank">path:{}</a>'.format(change_url, rm.get_abs_path())
    #         )
    #     return mark_safe("<br />".join(rm_list))


