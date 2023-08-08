from django.contrib import admin
from .models import Owner


class OwnerAdmin(admin.ModelAdmin):
    list_display = ('user','owner_fullname','is_approved','created_at')
    list_display_links =('user','owner_fullname')
# Register your models here.
admin.site.register(Owner,OwnerAdmin)
