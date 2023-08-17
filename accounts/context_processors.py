from owner.models import Owner
from django.conf import settings
def get_owner(request):
    try:
        owner = Owner.objects.get(user=request.user)
    except:
        owner = None
    return dict(owner=owner)

def get_google_api(request):
    return {'GOOGLE_API_KEY': settings.GOOGLE_API_KEY}