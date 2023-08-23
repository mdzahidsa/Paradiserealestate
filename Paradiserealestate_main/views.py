from django.shortcuts import render
from django.http import HttpResponse
from owner.models import Owner
from listings.models import Listings

def home(request):

    listings = Listings.objects.filter(is_approved=True, owner__user__is_active=True)[:4]
    context = {
        'listings' : listings
    }
    return render(request, 'home.html', context)
