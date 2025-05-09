from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CompanyRegistrationForm

@login_required
def register_company(request):
    """Register a new company for the current user."""
    # Check if the user already has a company
    if hasattr(request.user, 'company'):
        messages.info(request, "You already have a registered company.")
        return redirect('company_dashboard')
    
    if request.method == 'POST':
        form = CompanyRegistrationForm(request.POST)
        if form.is_valid():
            company = form.save(commit=False)
            company.user = request.user
            company.save()
            messages.success(request, "Company registered successfully!")
            return redirect('company_dashboard')
    else:
        form = CompanyRegistrationForm()
    
    return render(request, 'companies/register_company.html', {'form': form}) 
