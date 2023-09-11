from django.urls import path
from accounts import views as Accountviews
from . import views

urlpatterns = [

    path('', Accountviews.tenantDashboard, name='tenant'),
    path('profile/', views.tprofile, name='tprofile'),
    path('finalized-deals/', views.tenant_finalized_deals, name='tenant_finalized_deals'),
    path('rent-payment/<int:listing_id>/', views.rent_payment_form, name='rent_payment_form'),
    path('paypal/execute/', views.execute_payment, name='execute_payment'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('download-agreement/<int:request_id>/', views.download_agreement, name='download_agreement'),

    path('view-paid-rents/<int:listing_id>/', views.tenant_view_paid_rents, name='tenant_view_paid_rents'),
    path('view-rent-receipt/<int:payment_id>/', views.view_rent_receipt, name='view_rent_receipt'),


]