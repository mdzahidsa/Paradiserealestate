from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import UserForm
from .models import User,UserProfile
from django.contrib import messages
from owner.forms import OwnerForm
# Create your views here.
def registerUser(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user = form.save(commit=False)
            user.set_password(password)
            user.role = User.TENANT
            form.save()
            messages.success(request,"Your account has been registered successfully.")
            return redirect('registerUser')
        else:
            print('Invalid form')
    else: 
        form = UserForm()
    context = {
        'form' : form,
    }
    return render(request, 'accounts/registerUser.html', context)

def registerOwner(request):
    if request.method =='POST':
        form = UserForm(request.POST)
        o_form = OwnerForm(request.POST, request.FILES)
        if form.is_valid() and o_form.is_valid:
            password = form.cleaned_data['password']
            user = form.save(commit=False)
            user.set_password(password)
            user.role = User.OWNER
            user.save()
            owner = o_form.save(commit=False)
            owner.user = user
            user_profile = UserProfile.objects.get(user=user)
            owner.user_profile = user_profile
            owner.save()
            messages.success(request,"Your account has been registered successfully.Please wait for approval")
            return redirect('registerOwner')
        else:
            print('form.error')
    else:
        form = UserForm()
        o_form = OwnerForm()

    context = {
        'form' : form,
        'o_form':o_form,

    }
    return render(request,'accounts/registerOwner.html', context)