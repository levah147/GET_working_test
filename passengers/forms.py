from django import forms
from .models import Passenger

class PassengerForm(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = ['full_name', 'phone_number', 'address', 'blood_type', 'next_of_kin', 'next_of_kin_phone']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'blood_type': forms.Select(choices=[
                ('', 'Select Blood Type'),
                ('A+', 'A+'),
                ('A-', 'A-'),
                ('B+', 'B+'),
                ('B-', 'B-'),
                ('AB+', 'AB+'),
                ('AB-', 'AB-'),
                ('O+', 'O+'),
                ('O-', 'O-'),
            ]),
        }