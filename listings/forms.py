from django import forms

from accounts.validators import allow_only_image
from .models import Category,Listings

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name', 'description']

class ListingForm(forms.ModelForm):
    image1 = forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info w-100'}), validators=[allow_only_image])
    image2 = forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info w-100'}), validators=[allow_only_image])

    image3 = forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info w-100'}), validators=[allow_only_image])

    class Meta:
        model = Listings    
        fields =['category', 'listing_title', 'description', 'price', 'address', 'latitude', 'longitude','image1', 'image2', 'image3', 'is_available']