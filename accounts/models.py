from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', 'Administrator'),
        ('company', 'Transport Company'),
    )
    
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    phone_number = models.CharField(max_length=15, blank=True)
    
    def is_administrator(self):
        return self.user_type == 'admin'
    
    def is_company(self):
        return self.user_type == 'company'

# Add this to your existing accounts/models.py file

class AdministratorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='administrator_profile')
    department = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=50, unique=True)
    position = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    
    def __str__(self):
        return f"{self.user.username} - {self.position}"

    # Add this method to your existing User model in accounts/models.py

    # def is_administrator(self):
    #     """Check if the user is an administrator."""
    #     return hasattr(self, 'administrator_profile')

    # # Add this method to your User model
    # User.add_to_class('is_administrator', is_administrator)

    # Add this method to your User model in accounts/models.py

    # Make sure this method is correctly defined in your User model

# def is_company(self):
#     """Check if the user is associated with a company."""
#     return hasattr(self, 'company')

# # Add this method to your User model
# User.add_to_class('is_company', is_company)