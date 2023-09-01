from django import forms

from accounts.validators import allow_only_image
from .models import Category,Listings,Request

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

class RequestForm(forms.ModelForm):   
    full_name = forms.CharField(max_length=100, initial='Default Full Name',disabled=True)
    email = forms.EmailField(initial='default@example.com',disabled=True)
    message = forms.CharField(widget=forms.Textarea)
    user_IDproof = forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info w-100'}), validators=[allow_only_image])
    user_addressproof = forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info w-100'}), validators=[allow_only_image])
    class Meta:
        model = Request  
        fields = ['full_name','email','message','user_IDproof','user_addressproof']  

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['full_name'].initial = f"{user.first_name} {user.last_name}"
        self.fields['email'].initial = user.email