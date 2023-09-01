from django.db import models

# Create your models here.
from accounts.models import User
from listings.models import Listings
from django.utils import timezone

class RentPayment(models.Model):
    tenant = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE)
    payment_month = models.CharField(max_length=20)
    payment_date = models.DateTimeField(default=timezone.now)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=50, unique=True)
    payment_number = models.CharField(max_length=20, unique=True)
    payment_mode = models.CharField(max_length=20)
    is_successful = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.tenant.username} - {self.listing.listing_title} - {self.payment_month}  - {self.payment_number}"