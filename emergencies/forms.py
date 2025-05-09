from django import forms
from .models import Emergency

class EmergencyForm(forms.ModelForm):
    class Meta:
        model = Emergency
        fields = ['emergency_type', 'description', 'location']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }