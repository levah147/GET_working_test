from django.db import models
from django.conf import settings

class Company(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='company_profile')
    name = models.CharField(max_length=100)
    address = models.TextField()
    registration_number = models.CharField(max_length=50, unique=True)
    contact_person = models.CharField(max_length=100)
    contact_phone = models.CharField(max_length=15)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name