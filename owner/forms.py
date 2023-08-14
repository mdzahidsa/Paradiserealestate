from django import forms
from .models import Owner

from accounts.validators import allow_only_image

class OwnerForm(forms.ModelForm):
    owner_ID = forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info'}), validators=[allow_only_image])
    owner_addressproof = forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info'}), validators=[allow_only_image])
    owner_fullname = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = Owner
        fields = ['owner_fullname','owner_ID','owner_addressproof']