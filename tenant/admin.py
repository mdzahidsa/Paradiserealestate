from django.contrib import admin
from .models import RentPayment

# Register your models here.
@admin.register(RentPayment)
class RentPaymentAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'listing', 'payment_month', 'payment_date')
    list_filter = ('payment_month', 'payment_date')
    search_fields = ('tenant__username', 'listing__listing_title')