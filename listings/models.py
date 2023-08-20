from django.db import models
from owner.models import Owner
from django.core.mail import send_mail
from django.template.loader import render_to_string

from django.conf import settings
# Create your models here.
class Category(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
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
    slug = models.SlugField(max_length=100, unique=True)
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
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.listing_title

    def save(self, *args, **kwargs):
        # Check if is_approved field has changed to True
        if self.pk is not None:
            orig = Listings.objects.get(pk=self.pk)
            if orig.is_approved != self.is_approved:
                owner_email = self.owner.user.email  # Get owner's email from User model
                
                mail_template = 'accounts/emails/listing_approved.html'  # Path to your HTML template
                context = {
                    'owner_fullname':self.owner.owner_fullname,
                    'listing_title': self.listing_title,
                    'is_approved':self.is_approved,
                }
                message = render_to_string(mail_template, context)  # Render the HTML template

                from_email = settings.DEFAULT_FROM_EMAIL  # Set your sender email here
                recipient_list = [owner_email]

                if self.is_approved == True:
                    #send email
                    mail_subject = "Congratulations,Your account has been approved."
                  
                    send_mail(mail_subject, message, from_email, recipient_list, fail_silently=False)
                else:
                    mail_subject = "We Regret to inform,Your account could not be created."
                   
                    send_mail(mail_subject, message, from_email, recipient_list, fail_silently=False)
                # Send the email notification
        super(Listings, self).save(*args, **kwargs)