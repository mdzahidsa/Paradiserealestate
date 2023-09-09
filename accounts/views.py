from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import UserForm
from .models import User,UserProfile
from django.contrib import messages,auth
from owner.forms import OwnerForm
from listings.models import Listings
from tenant.models import RentPayment
from owner.models import Owner
from django.contrib.auth.tokens import default_token_generator
from .utils import detectUser,send_verification_email
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.decorators import login_required,user_passes_test
from django.template.defaultfilters import slugify
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
            mail_subject = 'Welcome to Paradise-Realestate.Please activate your account.'
            email_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request, user, mail_subject, email_template)

            messages.success(request,"Your account has been registered successfully.Please check your email to activate it.")
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
            owner_fullname = o_form.cleaned_data['owner_fullname']
            owner.owner_slug = slugify(owner_fullname)+'-'+str(user.id)
            user_profile = UserProfile.objects.get(user=user)
            owner.user_profile = user_profile
            owner.save()
            mail_subject = 'Welcome to Paradise-Realestate.Please activate your account.'
            email_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request, user, mail_subject, email_template)
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

def activate(request, uidb64, token):
    #Set is_active status to true
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Thank you for activating your account.')
        return redirect('myAccount')
    else:
        messages.error(request, 'Invalid activation link.')
        return redirect('Myaccount')


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

def get_owner(request):
    owner = Owner.objects.get(user=request.user)
    return owner

@login_required(login_url='login')
@user_passes_test(check_role_owner)
def ownerDashboard(request):
    owner = get_owner(request)
    
    # Retrieve listings owned by the owner
    owner_listings = Listings.objects.filter(owner=owner)
    
    # Retrieve recent rent payments for these listings
    recent_rent_payments = RentPayment.objects.filter(
        listing__in=owner_listings,
        is_successful=True
    ).order_by('-payment_date')[:10]  # Limit to the most recent 10 payments
    
    context = {
        'recent_rent_payments': recent_rent_payments,
    }
    return render(request, 'accounts/ownerDashboard.html')

@login_required(login_url='login')
@user_passes_test(check_role_tenant)
def tenantDashboard(request):
    return render(request, 'accounts/tenantDashboard.html')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)
            #send reset pwd to mail.
           
            mail_subject = 'Reset your password.'
            email_template = 'accounts/emails/reset_password_email.html'
            send_verification_email(request, user, mail_subject, email_template)
            messages.success(request, "Password reset link has been sent to your email.")
            return redirect('login')
        else:
            messages.error(request, "Account to this email does not exist.")
            return redirect('forgot_password')
    return render(request, 'accounts/forgot_password.html')

def reset_password_validate(request, uidb64, token):
    #validate user and secode token.
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request, 'Please reset your password.')
        return redirect('reset_password')
    else:
        messages.error(request, 'The link has been expired.')
        return redirect('myAccount')

    return

def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            pk = request.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, 'Password reset successfully.')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match.')
            return redirect('reset_password')
    return render(request, 'accounts/reset_password.html')