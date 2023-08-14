from django.shortcuts import redirect,render,get_object_or_404
from .forms import OwnerForm
from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from django.contrib import messages
from .models import Owner
from django.contrib.auth.decorators import login_required,user_passes_test
from accounts.views import check_role_owner



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