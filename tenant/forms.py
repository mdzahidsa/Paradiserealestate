from django import forms
from .models import RentPayment
class RentPaymentForm(forms.ModelForm):
    class Meta:
        model = RentPayment
        fields = ['payment_month'] 