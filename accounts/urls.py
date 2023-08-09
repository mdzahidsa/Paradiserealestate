from django.urls import path
from . import views

urlpatterns = [
    path('registerUser/', views.registerUser, name='registerUser'),
    path('registerOwner/', views.registerOwner, name='registerOwner'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('myAccount/',views.myAccount,name='myAccount'),
    path('ownerDashboard/',views.ownerDashboard,name='ownerDashboard'),
    path('tenantDashboard/',views.tenantDashboard,name='tenantDashboard'),
    path('activate/<uidb64>/<token>/',views.activate, name='activate'),
]