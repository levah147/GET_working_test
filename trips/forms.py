from django import forms
from .models import Trip, Vehicle
from passengers.models import Passenger

class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['vehicle', 'departure_time', 'destination', 'fee_per_passenger']
        widgets = {
            'departure_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
    
    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company', None)
        super().__init__(*args, **kwargs)
        
        if company:
            # Limit vehicle choices to those belonging to the company
            self.fields['vehicle'].queryset = Vehicle.objects.filter(company=company)

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['plate_number', 'vehicle_type', 'capacity', 'model', 'year', 'description']

class AddPassengerToTripForm(forms.Form):
    passenger = forms.ModelChoiceField(
        queryset=Passenger.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    seat_number = forms.CharField(
        max_length=10, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    def __init__(self, *args, **kwargs):
        trip = kwargs.pop('trip', None)
        super().__init__(*args, **kwargs)
        
        if trip:
            # Get passengers already on this trip
            existing_passengers = trip.passengers.all().values_list('passenger_id', flat=True)
            
            # Exclude passengers already on this trip
            self.fields['passenger'].queryset = Passenger.objects.exclude(id__in=existing_passengers)
            
            # If no passengers are available, add a message
            if not self.fields['passenger'].queryset.exists():
                self.fields['passenger'].empty_label = "No available passengers"