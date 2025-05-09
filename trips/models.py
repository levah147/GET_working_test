from django.db import models
from companies.models import Company
from passengers.models import Passenger

class Vehicle(models.Model):
    VEHICLE_TYPES = (
        ('bus', 'Bus'),
        ('minibus', 'Minibus'),
        ('car', 'Car'),
        ('van', 'Van'),
        ('truck', 'Truck'),
        ('other', 'Other'),
    )
    
    company = models.ForeignKey('companies.Company', on_delete=models.CASCADE, related_name='vehicles')
    plate_number = models.CharField(max_length=20, unique=True)
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPES)
    capacity = models.PositiveIntegerField()
    model = models.CharField(max_length=100, null=True, blank=True)
    year = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    
    def total_passengers(self):
        """Return the total number of passengers this vehicle has transported."""
        from django.db.models import Sum
        return self.trips.aggregate(Sum('passenger_count'))['passenger_count__sum'] or 0
    
    def total_trips(self):
        """Return the total number of trips this vehicle has made."""
        return self.trips.count()
    
    def __str__(self):
        return f"{self.plate_number} - {self.company.name} ({self.get_vehicle_type_display()})"

class Trip(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='trips')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='trips')
    departure_time = models.DateTimeField()
    destination = models.CharField(max_length=100)
    fee_per_passenger = models.DecimalField(max_digits=10, decimal_places=2, default=500.00)
    is_completed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.company.name} - {self.destination} - {self.departure_time}"
    
    def total_passengers(self):
        return self.passengers.count()
    
    def total_fee(self):
        return self.total_passengers() * self.fee_per_passenger

class TripPassenger(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='passengers')
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE, related_name='trips')
    seat_number = models.CharField(max_length=10, blank=True, null=True)
    
    class Meta:
        unique_together = ('trip', 'passenger')