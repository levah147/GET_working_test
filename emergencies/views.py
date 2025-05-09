from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from .models import Emergency
from .forms import EmergencyForm
from trips.models import Trip

@login_required
def report_emergency(request):
    # Ensure the user is a company
    if not request.user.is_company():
        messages.error(request, "You don't have permission to access this page.")
        return redirect('home')
    
    company = request.user.company_profile
    
    # Get active trips for this company
    active_trips = Trip.objects.filter(
        company=company,
        departure_time__lte=timezone.now(),
        is_completed=False
    ).order_by('-departure_time')
    
    if request.method == 'POST':
        form = EmergencyForm(request.POST)
        trip_id = request.POST.get('trip')
        
        if form.is_valid() and trip_id:
            try:
                trip = Trip.objects.get(id=trip_id, company=company)
                emergency = form.save(commit=False)
                emergency.trip = trip
                emergency.save()
                
                messages.success(request, "Emergency reported successfully. Authorities have been notified.")
                return redirect('emergency_detail', pk=emergency.id)
            except Trip.DoesNotExist:
                messages.error(request, "Invalid trip selected.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = EmergencyForm()
    
    context = {
        'form': form,
        'active_trips': active_trips,
    }
    
    return render(request, 'emergencies/report_emergency.html', context)

@login_required
def emergency_list(request):
    # Ensure the user is a company
    if not request.user.is_company():
        messages.error(request, "You don't have permission to access this page.")
        return redirect('home')
    
    company = request.user.company_profile
    
    # Filter options
    status = request.GET.get('status', 'all')
    
    # Base queryset
    emergencies = Emergency.objects.filter(trip__company=company).order_by('-reported_time')
    
    # Apply filters
    if status == 'reported':
        emergencies = emergencies.filter(status='reported')
    elif status == 'in_progress':
        emergencies = emergencies.filter(status='in_progress')
    elif status == 'resolved':
        emergencies = emergencies.filter(status='resolved')
    
    context = {
        'emergencies': emergencies,
        'status': status,
    }
    
    return render(request, 'emergencies/emergency_list.html', context)

@login_required
def emergency_detail(request, pk):
    # Ensure the user is a company
    if not request.user.is_company():
        messages.error(request, "You don't have permission to access this page.")
        return redirect('home')
    
    company = request.user.company_profile
    emergency = get_object_or_404(Emergency, pk=pk, trip__company=company)
    
    context = {
        'emergency': emergency,
    }
    
    return render(request, 'emergencies/emergency_detail.html', context)