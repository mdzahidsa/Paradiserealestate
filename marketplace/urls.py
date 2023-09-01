from django.urls import path
from . import views

urlpatterns = [

    path('', views.marketplace, name='marketplace'),
    path('<slug:owner_slug>/', views.owner_detail, name='owner_detail'),
    path('<slug:owner_slug>/listing/<int:listing_id>/', views.view_detail_listing, name='view_detail_listing'),
    path('place-request/<int:listing_id>/', views.place_request, name='place_request'),
    path('<slug:owner_slug>/received-requests/', views.owner_received_requests, name='owner_received_requests'),
    path('approve-request/<int:request_id>/', views.approve_request, name='approve_request'),
    path('reject-request/<int:request_id>/', views.reject_request, name='reject_request'),
    path('sent-requests/<str:user_identifier>/', views.tenant_sent_requests, name='tenant_sent_requests'),

]