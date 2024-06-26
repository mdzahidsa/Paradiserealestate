from django.urls import path, include
from . import views
from accounts import views as AccountViews


urlpatterns = [
    path('profile/', views.oprofile, name='oprofile'),
    path('', AccountViews.ownerDashboard, name='owner'),
    path('create-listings/', views.create_listings, name='create_listings'),
    path('create-listings/category/<int:pk>/', views.listings_by_category, name='listings_by_category'),
# add category
    path('create-listings/category/add/', views.add_category, name='add_category'),
    path('create-listings/category/edit/<int:pk>/', views.edit_category, name='edit_category'),
    path('create-listings/category/delete/<int:pk>/', views.delete_category, name='delete_category'),
    path('create-listings/listings/add/', views.add_listings, name='add_listings'),
    path('create-listings/listings/edit/<int:pk>/', views.edit_listings, name='edit_listings'),
    path('create-listings/listings/delete/<int:pk>/', views.delete_listings, name='delete_listings'),
    path('create-listings/listings/viewdetail/<int:pk>/', views.viewdetail_listings, name='viewdetail_listings'),
    path('finalized-deals/', views.owner_finalized_deals, name='owner_finalized_deals'),
    path('rents-received/<int:listing_id>/', views.owner_view_rents_received, name='owner_view_rents_received'),


]