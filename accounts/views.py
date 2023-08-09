from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import UserForm
from .models import User,UserProfile
from django.contrib import messages,auth
from owner.forms import OwnerForm
from .utils import detectUser,send_verification_email
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required,user_passes_test
# Create your views here.

#restrict owners from gaining access to tenant dashboard
def check_role_owner(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied
#restrict tenant from gaining access to tenant dashboard
def check_role_tenant(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied

def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request,'You are already logged in!.')
        return redirect('tenantDashboard')
    elif request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user = form.save(commit=False)
            user.set_password(password)
            user.role = User.TENANT
            form.save()
            #verification/activate User email

            send_verification_email(request, user)
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
    if request.user.is_authenticated:
        messages.warning(request,'You are already logged in!.')
        return redirect('ownerDashboard')
    elif request.method =='POST':
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
            send_verification_email(request, user)

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

def activate(request,uidb64,token):
    #Set is_active status to true
    return

def login(request):
    if request.user.is_authenticated:
        messages.warning(request,'You are already logged in!.')
        return redirect('myAccount')
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request,"You are now logged in")
            return redirect('myAccount')
        else:
            messages.error(request,"Invalid login credentials.Please try again.")
            return redirect('login')
    return render(request,'accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.info(request,'You are now logged out.')
    return redirect('login')

@login_required(login_url='login')
def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)

@login_required(login_url='login')
@user_passes_test(check_role_owner)
def ownerDashboard(request):
    return render(request, 'accounts/ownerDashboard.html')

@login_required(login_url='login')
@user_passes_test(check_role_tenant)
def tenantDashboard(request):
    return render(request, 'accounts/tenantDashboard.html')