from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from accounts.views import check_role_owner,check_role_tenant


from listings.models import Listings,Category,Request
from owner.models import Owner
from accounts.models import User
from django.db.models import Prefetch
from django.http import HttpResponse
from django.contrib import messages
from listings.forms import RequestForm
# Create your views here.
def marketplace(request):
    listings = Listings.objects.filter(is_approved=True, owner__user__is_active=True)
    listings_per_page = 9
    paginator = Paginator(listings, listings_per_page)
    
    page = request.GET.get('page')  # Get the current page number
    try:
        listings = paginator.page(page)
    except PageNotAnInteger:
        listings = paginator.page(1)
    except EmptyPage:
        listings = paginator.page(paginator.num_pages)

    listings_count = paginator.count
   # listings_count = listings.count()
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

def search(request):
    address = request.GET['address']
    latitude = request.GET['lat']
    longitude = request.GET['lng']
    radius = request.GET['radius']
    keyword = request.GET['keyword']
    listings = Listings.objects.filter(listing_title__icontains=keyword, is_approved=True, is_available=True, owner__user__is_active=True)
    listings_count = listings.count()
    context = {
        'listings' : listings,
        'listings_count' : listings_count,
    }
    return render(request, 'marketplace/listings.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_tenant)
def place_request(request, listing_id):
    listing = get_object_or_404(Listings, id=listing_id)

    # Check the user's request count for listings
    user_request_count = Request.objects.filter(user=request.user, listing__isnull=False).count()

    request_limit = 3  # Set the request limit

    if user_request_count >= request_limit:
        messages.error(request, "You have reached the maximum request limit of 3 listings.")
        return render(request, 'marketplace/upgradeplan.html')

    if request.method == 'POST':
        form = RequestForm(request.user, request.POST, request.FILES)  # Pass user instance and uploaded files to the form
        if form.is_valid():
            request_instance = form.save(commit=False)
            request_instance.user = request.user
            request_instance.listing = listing
            request_instance.save()
            messages.success(request, 'Your request has been placed successfully!')
            return redirect('marketplace')
    else:
        form = RequestForm(user=request.user)  # Pass user instance to the form

    return render(request, 'tenant/request_form.html', {'form': form, 'listings': listing})
@login_required(login_url='login')
@user_passes_test(check_role_owner)
def owner_received_requests(request, owner_slug):
    owner = get_object_or_404(Owner, owner_slug=owner_slug)

    # Retrieve the listings owned by the owner
    owner_listings = owner.listings_set.all()  # Assuming you have used "listings" as related_name

    # Filter requests for the owner's listings
    received_requests = Request.objects.filter(listing__in=owner_listings)
    # Pagination
    paginator = Paginator(received_requests, 6)  # Display 6 requests per page
    page = request.GET.get('page')  # Get the current page number
    try:
        received_requests = paginator.page(page)
    except PageNotAnInteger:
        received_requests = paginator.page(1)
    except EmptyPage:
        received_requests = paginator.page(paginator.num_pages)

    context = {
        'owner': owner,
        'received_requests': received_requests,
    }
    return render(request, 'owner/owner_received_requests.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_owner)
def approve_request(request, request_id):
    request_instance = get_object_or_404(Request, id=request_id)
    request_instance.is_ownerapproved = True
    if request_instance.is_adminapproved:
        request_instance.is_deal_finalized = True
    request_instance.save()
    
    return redirect('owner_received_requests', owner_slug=request_instance.listing.owner.owner_slug)

@login_required(login_url='login')
@user_passes_test(check_role_owner)
def reject_request(request, request_id):
    request_instance = get_object_or_404(Request, id=request_id)
    request_instance.is_ownerrejected = True
    request_instance.save()
    return redirect('owner_received_requests', owner_slug=request_instance.listing.owner.owner_slug)

@login_required(login_url='login')
@user_passes_test(check_role_tenant)
def tenant_sent_requests(request, user_identifier):
    user = get_object_or_404(User, id=user_identifier)  # Or use username instead of ID

    # Get the distinct listings associated with the user's requests
    requested_listings = Listings.objects.filter(request__user=user).distinct()
    sent_requests = Request.objects.filter(user=user, listing__in=requested_listings)

    context = {
        'requested_listings': requested_listings,
        'user_identifier': user_identifier,
        'sent_requests':sent_requests,
    }
    return render(request, 'tenant/tenant_sent_requests.html', context)

def admin_approve_request(request, request_id):
    request_instance = get_object_or_404(Request, id=request_id)
    request_instance.is_adminapproved = True
    
    if request_instance.is_ownerapproved:
        request_instance.is_deal_finalized = True

    request_instance.save()
   

