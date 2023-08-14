from django.urls import path, include
from . import views
from accounts import views as AccountViews


urlpatterns = [
    path('profile/', views.oprofile, name='oprofile'),
    path('', AccountViews.ownerDashboard, name='owner'),

]