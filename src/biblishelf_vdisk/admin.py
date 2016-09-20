from django.contrib import admin
from .models import VDisk
# Register your models here.


class VDiskAdmin(admin.ModelAdmin):
    pass


admin.site.register(VDisk, VDiskAdmin)