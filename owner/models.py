from django.db import models
from accounts.models import User,UserProfile
from accounts.utils import send_notification
# Create your models here.
class Owner(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name='userprofile', on_delete=models.CASCADE)
    owner_fullname=models.CharField(max_length=50)
    owner_slug = models.SlugField(max_length=100, unique=True)
    owner_ID = models.ImageField(upload_to="owner/ID")
    owner_addressproof = models.ImageField(upload_to="owner/addressproof")
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.owner_fullname
    
    def save(self, *args, **kwargs):
        if self.pk is not None:
            #Update
            orig = Owner.objects.get(pk=self.pk)
            if orig.is_approved != self.is_approved:
                mail_template = 'accounts/emails/admin_approval_email.html'
                context = {
                        'user': self.user,
                        'is_approved':self.is_approved,
                    }
                if self.is_approved == True:
                    #send email
                    mail_subject = "Congratulations,Your account has been approved."
                  
                    send_notification(mail_subject, mail_template, context)
                else:
                    mail_subject = "We Regret to inform,Your account could not be created."
                   
                    send_notification(mail_subject, mail_template, context)


        return super(Owner,self).save(*args, **kwargs)
        