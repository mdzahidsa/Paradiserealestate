from django.shortcuts import render,get_object_or_404
from listings.models import Listings,Category
from owner.models import Owner
from django.db.models import Prefetch
# Create your views here.
def marketplace(request):
    listings = Listings.objects.filter(is_approved=True, owner__user__is_active=True)
    
    listings_count = listings.count()
    context = {
        'listings' : listings,
        'listings_count' : listings_count,
    }
    return render(request, 'marketplace/listings.html', context)

def owner_detail(request, owner_slug):
    owner = get_object_or_404(Owner, owner_slug=owner_slug)
    categories = Category.objects.filter(owner=owner).prefetch_related(
        Prefetch(
            'listings',
            queryset = Listings.objects.filter()

        )
        )
    context = {
        'owner' : owner,
        'categories':categories,
    }
    return render(request, 'marketplace/owner_detail.html', context)

def view_detail_listing(request, owner_slug, listing_id):
    owner = get_object_or_404(Owner, owner_slug=owner_slug)
    listings = get_object_or_404(Listings, id=listing_id)
    ownerlistings = Listings.objects.filter(owner=owner)
    context = {
        'owner': owner,
        'listings': listings,
        'ownerlisting':ownerlistings,
    }
    return render(request, 'marketplace/view_marketplacedetail_listing.html', context)
