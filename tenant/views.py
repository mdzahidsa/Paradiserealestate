from django.shortcuts import render,get_object_or_404,redirect
from django .contrib.auth.decorators import login_required
from accounts.forms import UserProfileForm,UserInfoForm
from django.contrib import messages
import uuid
from decimal import Decimal
from django.utils import timezone
from django.conf import settings
from paypalrestsdk import Payout

import paypalrestsdk

from accounts.models import UserProfile
from listings.models import Request,Listings
from tenant.models import RentPayment
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied


def download_agreement(request, request_id):
    # Retrieve the request object
    request_obj = get_object_or_404(Request, pk=request_id)

    # Ensure that only the tenant associated with the request can download the agreement
    if request.user != request_obj.user:
        raise PermissionDenied

    # Check if the request has an agreement file attached
    if not request_obj.agreement_file:
        return HttpResponse("No agreement file available for download.")

    # Open and serve the agreement file for download
    with open(request_obj.agreement_file.path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{request_obj.agreement_file.name}"'
        return response
# Create your views here.
@login_required(login_url='login')
def tprofile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        user_form = UserInfoForm(request.POST, instance=request.user)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            messages.success(request, 'Profile Updated')
            return redirect('tprofile')
        else:
            print(profile_form.errors)
            print(user_form.errors)
    else:
        profile_form = UserProfileForm(instance=profile)
        user_form = UserInfoForm(instance=request.user)
    context = {
        'profile_form':profile_form,
        'profile':profile,
        'user_form':user_form,
    }
    return render(request, 'tenant/tprofile.html', context)

def tenant_finalized_deals(request):
    user = request.user
    finalized_deals = Request.objects.filter(
        user=user,
        is_deal_finalized=True
    )
    context = {
        'finalized_deals': finalized_deals,
    }
    return render(request, 'tenant/tenant_finalized_deals.html', context)


def generate_unique_transaction_id():
    return str(uuid.uuid4())

def generate_unique_payment_number():
    timestamp_str = timezone.now().strftime('%Y%m%d%H%M%S')
    uuid_portion = uuid.uuid4().hex[:6]
    payment_number = f"PAY{timestamp_str}{uuid_portion}"
    
    # Trim payment number if it's longer than 20 characters
    if len(payment_number) > 20:
        payment_number = payment_number[:20]
    
    return payment_number

def transfer_money_to_owner(owner_paypal_email, payment_amount):
    paypalrestsdk.configure({
        'mode': settings.PAYPAL_MODE,
        'client_id': settings.PAYPAL_CLIENT_ID,
        'client_secret': settings.PAYPAL_CLIENT_SECRET,
    })

    # Create a Payout item for transferring money to the owner
    payout_item = {
        "recipient_type": "EMAIL",
        "amount": {
            "value": str(payment_amount),
            "currency": "USD"
        },
        "receiver": owner_paypal_email,
        "note": "Rent payment transfer",
    }

    payout = paypalrestsdk.Payout({
        "sender_batch_header": {
            "sender_batch_id": generate_unique_transaction_id(),  # Unique batch ID
            "email_subject": "Rent payment transfer"
        },
        "items": [payout_item]
    })

    return payout.create()  # This will return the API response from PayPal


def rent_payment_form(request, listing_id):
    listing = get_object_or_404(Listings, id=listing_id)
    user_request = get_object_or_404(Request, listing=listing, user=request.user, is_deal_finalized=True)
    
    if request.method == 'POST':
        payment_month = request.POST.get('payment_month')
        payment_amount = Decimal(listing.price)
        owner_paypal_email = listing.owner.user.email  # Assuming owner has a user associated with it
        
        transaction_id = generate_unique_transaction_id()
        payment_number = generate_unique_payment_number()
    
        rent_payment = RentPayment.objects.create(
            tenant=request.user,
            listing=listing,
            payment_month=payment_month,
            payment_amount=payment_amount,
            transaction_id=transaction_id,
            payment_number=payment_number,
            payment_mode='PayPal'
        )

        paypalrestsdk.configure({
            'mode': settings.PAYPAL_MODE,
            'client_id': settings.PAYPAL_CLIENT_ID,
            'client_secret': settings.PAYPAL_CLIENT_SECRET,
        })

        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "transactions": [{
                "amount": {
                    "total": str(payment_amount),
                    "currency": "EUR"
                },
                "description": f"Rent payment for {payment_month}"
            }],
            "redirect_urls": {
                "return_url": "http://Google.com/",
                "cancel_url": "http://yourwebsite.com/cancel/"
            }
        })

        if payment.create():
            for link in payment.links:
                if link.method == 'REDIRECT':
                    redirect_url = str(link.href)
                    transfer_response = transfer_money_to_owner(owner_paypal_email, payment_amount)

                    if transfer_response:
                        rent_payment.is_successful = True
                        rent_payment.save()
                        return redirect(redirect_url)
                    else:
                        # Handle transfer failure
                        return redirect('rent_payment_form', listing_id=listing.id)
        else:
            # Handle payment creation failure
            return redirect('rent_payment_form', listing_id=listing.id)
        
        context = {
            'rent_payment': rent_payment,
        }
        return render(request, 'tenant/view_rent_receipt.html', context)
    
    context = {
        'listing': listing,
        'request': user_request,
    }
    return render(request, 'tenant/rent_payment_form.html', context)

def payment_success(request):
    rent_payment_id = request.GET.get('rent_payment_id')
    rent_payment = RentPayment.objects.get(id=rent_payment_id)

    paypalrestsdk.configure({
        'mode': settings.PAYPAL_MODE,
        'client_id': settings.PAYPAL_CLIENT_ID,
        'client_secret': settings.PAYPAL_CLIENT_SECRET,
    })

    payout = Payout({
        "sender_batch_header": {
            "sender_batch_id": rent_payment.payment_number,
            "email_subject": "Rent Payment",
        },
        "items": [
            {
                "recipient_type": "EMAIL",
                "amount": {
                    "value": str(rent_payment.payment_amount),
                    "currency": "USD",
                },
                "receiver": rent_payment.listing.owner_paypal_email,  # Owner's PayPal email
                "note": "Rent payment",
            }
        ],
    })

    payout_create_response = payout.create()

    if payout_create_response.success():
        # Payout request was successful
        rent_payment.is_successful = True
        rent_payment.save()

        return render(request, 'tenant/payment_success.html')
    else:
        # Handle payout request failure
        return render(request, 'tenant/payment_failure.html')


def tenant_view_paid_rents(request, listing_id):
    listing = get_object_or_404(Listings, id=listing_id)
    rents_paid = RentPayment.objects.filter(listing=listing, tenant=request.user)
    
    context = {
        'listing': listing,
        'rents_paid': rents_paid,
    }
    return render(request, 'tenant/tenant_view_paid_rents.html', context)

def view_rent_receipt(request, payment_id):
    payment = get_object_or_404(RentPayment, id=payment_id)
    
    # Retrieve the associated Request for this payment
    tenant_request = get_object_or_404(Request, listing=payment.listing, user=request.user)
    
    context = {
        'payment': payment,
        'tenant_full_name': tenant_request.full_name,
    }
    
    return render(request, 'tenant/view_rent_receipt.html', context)

def execute_payment(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    payment = paypalrestsdk.Payment.find(payment_id)
    if payment.execute({"payer_id": payer_id}):
        # Payment successful
        return render(request, 'tenant/payment_success.html')
    else:
        # Payment failed
        return render(request, 'tenant/payment_failed.html')