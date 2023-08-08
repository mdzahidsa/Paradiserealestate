from django import forms
from .models import Owner


class OwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = ['owner_fullname','owner_ID','owner_addressproof']