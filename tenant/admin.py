from django.contrib import admin
from .models import RentPayment

# Register your models here.
@admin.register(RentPayment)
class RentPaymentAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'listing', 'payment_month', 'payment_date', 'payment_number')
    list_filter = ('payment_month', 'payment_date', 'payment_number')
    search_fields = ('tenant__username', 'listing__listing_title', 'payment_number')