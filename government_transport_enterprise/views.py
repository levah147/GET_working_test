from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def home(request):
    if request.user.is_authenticated:
        if request.user.is_company():
            return redirect('company_dashboard')
        elif request.user.is_administrator():
            return redirect('admin_dashboard')
    
    return render(request, 'home.html')
