from django.db import models

class Passenger(models.Model):
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    blood_type = models.CharField(max_length=5, blank=True, null=True)
    next_of_kin = models.CharField(max_length=100)
    next_of_kin_phone = models.CharField(max_length=15)
    
    def __str__(self):
        return self.full_name