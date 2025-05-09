from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CompanyRegistrationForm

def register_company(request):
    if request.method == 'POST':
        form = CompanyRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}. You can now log in.')
            return redirect('login')
    else:
        form = CompanyRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

# Add this to your accounts/views.py file


from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    """Custom logout view that accepts both GET and POST requests."""
    logout(request)
    return redirect('home')



@login_required
def profile(request):
    return render(request, 'accounts/profile.html')


# Add this to your existing accounts/views.py file

@login_required
def profile_view(request):
    """Display the user's profile."""
    return render(request, 'accounts/profile.html')

@login_required
def edit_profile(request):
    """Edit the user's profile."""
    if request.method == 'POST':
        # Handle form submission
        if request.user.is_company():
            # Update company information
            company = request.user.company
            company.name = request.POST.get('name', company.name)
            company.contact_person = request.POST.get('contact_person', company.contact_person)
            company.phone_number = request.POST.get('phone_number', company.phone_number)
            company.address = request.POST.get('address', company.address)
            company.save()
        
        # Update user information
        user = request.user
        user.email = request.POST.get('email', user.email)
        user.save()
        
        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')
    
    return render(request, 'accounts/edit_profile.html')