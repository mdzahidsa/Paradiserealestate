from django.contrib import admin
from listings.models import Category,Listings
# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('category_name',)}
    list_display = ('category_name', 'owner','updated_at')
    search_fields = ('category_name', 'owner__owner_fullname')

class listingsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('listing_title',)}
    list_display = ('listing_title', 'category', 'owner', 'price', 'is_available', 'modified_at', 'is_approved')
    search_fields = ('listing_title', 'category__category_name', 'owner__owner_fullname')
    list_filter = ('is_available', 'is_approved')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Listings, listingsAdmin)