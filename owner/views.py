from django.shortcuts import redirect,render,get_object_or_404
from .forms import OwnerForm
from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from django.contrib import messages
from .models import Owner
from django.contrib.auth.decorators import login_required,user_passes_test
from accounts.views import check_role_owner
from listings.models import Category,Listings
from listings.forms import CategoryForm,ListingForm
def get_owner(request):
    owner = Owner.objects.get(user=request.user)
    return owner

# Create your views here.
@login_required(login_url='login')
@user_passes_test(check_role_owner)
def oprofile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    owner = get_object_or_404(Owner, user=request.user)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        owner_form = OwnerForm(request.POST, request.FILES, instance=owner)
        if profile_form.is_valid() and owner_form.is_valid():
            profile_form.save()
            owner_form.save()
            messages.success(request, 'Settings updated')
            return redirect('oprofile')
        else:
            print(profile_form.errors)
            print(owner_form.errors)
    else:
        profile_form = UserProfileForm(instance = profile)
        owner_form = OwnerForm(instance = owner)

    context = {
        'profile_form':profile_form,
        'owner_form':owner_form,
        'profile':profile,
        'owner':owner

    }
    return render(request, 'owner/oprofile.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_owner)
def create_listings(request):
    owner = get_owner(request)
    categories = Category.objects.filter(owner=owner).order_by('created_at')
    context = {
        'categories': categories,
    }
    return render(request, 'owner/create_listings.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_owner)
def listings_by_category(request, pk=None):
    owner = get_owner(request)
    category = get_object_or_404(Category, pk=pk)
    listings = Listings.objects.filter(owner=owner, category=category)
    context = {
        'listings':listings,
        'category': category,
    }
    return render(request, 'owner/listings_by_category.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_owner)
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.owner = get_owner(request)
            form.save()
            messages.success(request, 'Category added successfully')
            return redirect('create_listings')
        else:
            print(form.errors)
    else:  
        form = CategoryForm()
    context = {
        'form': form,
    }
    return render(request, 'owner/add_category.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_owner)
def edit_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.owner = get_owner(request)
            form.save()
            messages.success(request, 'Category updated successfully')
            return redirect('create_listings')
        else:
            print(form.errors)
    else:  
        form = CategoryForm(instance=category)
    context = {
        'form': form,
        'category':category,
    }
    return render(request, 'owner/edit_category.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_owner)
def delete_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, 'Category has been deleted successfully.')
    return redirect('create_listings')

@login_required(login_url='login')
@user_passes_test(check_role_owner)
def add_listings(request):
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing_title = form.cleaned_data['listing_title']
            listing = form.save(commit=False)
            listing.owner = get_owner(request)
           
            form.save()
            
            messages.success(request, 'Listing submitted for approval successfully')
            return redirect('listings_by_category', listing.category.id)
        else:
            print(form.errors)
    else:      
        form = ListingForm()
        form.fields['category'].queryset = Category.objects.filter(owner=get_owner(request))
    context = {
        'form': form,
        
    }
    return render(request, 'owner/add_listings.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_owner)
def edit_listings(request, pk=None):
    listing = get_object_or_404(Listings, pk=pk)
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            listingtitle = form.cleaned_data['listing_title']
            listing = form.save(commit=False)
            listing.owner = get_owner(request)
        
            form.save()
            messages.success(request, 'Listing updated successfully')
            return redirect('listings_by_category', listing.category.id)
        else:
            print(form.errors)
    else:  
        form = ListingForm(instance=listing)
        form.fields['category'].queryset = Category.objects.filter(owner=get_owner(request))
    context = {
        'form': form,
        'listing':listing,
    }
    return render(request, 'owner/edit_listings_main.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_owner)
def delete_listings(request, pk=None):
    listing = get_object_or_404(Listings, pk=pk)
    listing.delete()
    messages.success(request, 'Listing has been removed successfully.')
    return redirect('listings_by_category', listing.category.id)

@login_required(login_url='login')
@user_passes_test(check_role_owner)
def viewdetail_listings(request, pk=None):
    listing = get_object_or_404(Listings, pk=pk)
    form = ListingForm(instance=listing)
    context = {
        'form': form,
        'listing':listing,
    }
    return render(request, 'owner/view_listing_details.html', context)