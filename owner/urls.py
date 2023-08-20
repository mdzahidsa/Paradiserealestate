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

]