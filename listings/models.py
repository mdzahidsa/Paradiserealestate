from django.db import models
from owner.models import Owner
from django.core.mail import send_mail
from django.template.loader import render_to_string

from django.conf import settings
# Create your models here.
class Category(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=50, unique=False)
    description = models.TextField(max_length=250, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    def __str__(self):
        return self.category_name
    
class Listings(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    listing_title = models.CharField(max_length=50)
    description = models.TextField(max_length=250, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.CharField(max_length=250, blank=True, null=True)
    latitude = models.CharField(max_length=20, blank=True, null=True)
    longitude = models.CharField(max_length=20, blank=True, null=True)
    image1 = models.ImageField(upload_to='listingimages')
    image2 = models.ImageField(upload_to='listingimages')
    image3 = models.ImageField(upload_to='listingimages')
    is_available = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.listing_title

    def save(self, *args, **kwargs):
        if self.pk is not None:
            orig = Listings.objects.get(pk=self.pk)
            if orig.is_approved != self.is_approved or orig.is_rejected != self.is_rejected:
                owner_email = self.owner.user.email
                
                mail_template = 'accounts/emails/listing_approved.html'
                context = {
                    'owner_fullname': self.owner.owner_fullname,
                    'listing_title': self.listing_title,
                    'is_rejected': self.is_rejected,
                    'is_approved': self.is_approved,

                }
                message = render_to_string(mail_template, context)

                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [owner_email]

                if self.is_approved:
                    mail_subject = "Congratulations, Your listing has been approved."
                elif self.is_rejected:
                    mail_subject = "We Regret to inform, Your listing could not be created."
                else:
                    mail_subject = "Your listing is under review."

                send_mail(mail_subject, message, from_email, recipient_list, fail_silently=False)

        super(Listings, self).save(*args, **kwargs)