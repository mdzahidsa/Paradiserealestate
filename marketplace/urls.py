from django.urls import path
from . import views

urlpatterns = [

    path('', views.marketplace, name='marketplace'),
    path('<slug:owner_slug>/', views.owner_detail, name='owner_detail'),
    path('<slug:owner_slug>/listing/<int:listing_id>/', views.view_detail_listing, name='view_detail_listing'),
]