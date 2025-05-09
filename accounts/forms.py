from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from companies.models import Company

class CompanyRegistrationForm(UserCreationForm):
    company_name = forms.CharField(max_length=100)
    address = forms.CharField(widget=forms.Textarea)
    registration_number = forms.CharField(max_length=50)
    contact_person = forms.CharField(max_length=100)
    contact_phone = forms.CharField(max_length=15)
    logo = forms.ImageField(required=False)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'company'
        
        if commit:
            user.save()
            Company.objects.create(
                user=user,
                name=self.cleaned_data['company_name'],
                address=self.cleaned_data['address'],
                registration_number=self.cleaned_data['registration_number'],
                contact_person=self.cleaned_data['contact_person'],
                contact_phone=self.cleaned_data['contact_phone'],
                logo=self.cleaned_data.get('logo')
            )
        
        return user