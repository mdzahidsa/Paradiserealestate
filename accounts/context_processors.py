from owner.models import Owner

def get_owner(request):
    try:
        owner = Owner.objects.get(user=request.user)
    except:
        owner = None
    return dict(owner=owner)
