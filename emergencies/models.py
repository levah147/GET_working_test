from django.db import models
from trips.models import Trip

class Emergency(models.Model):
    EMERGENCY_TYPE_CHOICES = (
        ('accident', 'Accident'),
        ('breakdown', 'Vehicle Breakdown'),
        ('medical', 'Medical Emergency'),
        ('other', 'Other'),
    )
    
    EMERGENCY_STATUS_CHOICES = (
        ('reported', 'Reported'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    )
    
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='emergencies')
    emergency_type = models.CharField(max_length=10, choices=EMERGENCY_TYPE_CHOICES)
    description = models.TextField()
    location = models.CharField(max_length=255)
    reported_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=15, choices=EMERGENCY_STATUS_CHOICES, default='reported')
    
    def __str__(self):
        return f"{self.trip.company.name} - {self.emergency_type} - {self.reported_time}"