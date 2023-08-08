from django.db import models
from accounts.models import User,UserProfile

# Create your models here.
class Owner(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name='userprofile', on_delete=models.CASCADE)
    owner_fullname=models.CharField(max_length=50)
    owner_ID = models.ImageField(upload_to="owner/ID")
    owner_addressproof = models.ImageField(upload_to="owner/addressproof")
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.owner_fullname