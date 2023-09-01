from owner.models import Owner
from django.conf import settings
from accounts.models import UserProfile
def get_owner(request):
    try:
        owner = Owner.objects.get(user=request.user)
    except:
        owner = None
    return dict(owner=owner)

def get_user_profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except:
        user_profile = None
    return dict(user_profile=user_profile)

def get_google_api(request):
    return {'GOOGLE_API_KEY': settings.GOOGLE_API_KEY}