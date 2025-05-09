from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count
from django.db.models import Count, Q

from django.utils import timezone
from datetime import timedelta

from companies.models import Company
from emergencies.models import Emergency
from trips.models import Trip, Vehicle
from passengers.models import Passenger
from payments.models import Payment

@login_required
def company_dashboard(request):
    # Ensure the user is a company
    if not request.user.is_company():
        messages.error(request, "You don't have permission to access this page.")
        return redirect('home')
    
    company = request.user.company_profile
    # company = request.user.company  # Make sure this is correct
    
    # Get today's date
    today = timezone.now().date()
    
    # Get statistics
    total_vehicles = Vehicle.objects.filter(company=company).count()
    
    # Today's trips
    today_trips = Trip.objects.filter(
        company=company,
        departure_time__date=today
    )
    today_trip_count = today_trips.count()
    
    # Today's passengers
    today_passenger_count = sum(trip.total_passengers() for trip in today_trips)
    
    # Today's revenue
    today_revenue = sum(trip.total_fee() for trip in today_trips)
    
    # Recent trips (last 5)
    recent_trips = Trip.objects.filter(company=company).order_by('-departure_time')[:5]
    
    # Upcoming trips
    upcoming_trips = Trip.objects.filter(
        company=company,
        departure_time__gt=timezone.now(),
        is_completed=False
    ).order_by('departure_time')[:5]
    
    context = {
        'company': company,
        'total_vehicles': total_vehicles,
        'today_trip_count': today_trip_count,
        'today_passenger_count': today_passenger_count,
        'today_revenue': today_revenue,
        'recent_trips': recent_trips,
        'upcoming_trips': upcoming_trips,
    }
    
    return render(request, 'dashboard/company_dashboard.html', context)


@login_required
def admin_dashboard(request):
    # Ensure the user is an administrator
    if not request.user.is_administrator():
        messages.error(request, "You don't have permission to access this page.")
        return redirect('home')
    
    # Get statistics
    total_companies = Company.objects.count()
    total_vehicles = Vehicle.objects.count()
    
    # Today's date
    today = timezone.now().date()
    
    # Today's trips
    today_trips = Trip.objects.filter(departure_time__date=today)
    today_trip_count = today_trips.count()
    
    # Today's passengers
    today_passenger_count = sum(trip.total_passengers() for trip in today_trips)
    
    # Today's revenue
    today_revenue = sum(trip.total_fee() for trip in today_trips)
    
    # Recent trips (last 10)
    recent_trips = Trip.objects.all().order_by('-departure_time')[:10]
    
    # Recent emergencies (last 5)
    recent_emergencies = Emergency.objects.all().order_by('-reported_time')[:5]
    
    # Companies with most trips this month
    month_start = today.replace(day=1)
    
    # Fixed line - changed 'trip' to 'trips' to match the related_name in the model
    companies_with_most_trips = Company.objects.annotate(
        trip_count=Count('trips', filter=Q(trips__departure_time__gte=month_start))
    ).order_by('-trip_count')[:5]
    
    context = {
        'total_companies': total_companies,
        'total_vehicles': total_vehicles,
        'today_trip_count': today_trip_count,
        'today_passenger_count': today_passenger_count,
        'today_revenue': today_revenue,
        'recent_trips': recent_trips,
        'recent_emergencies': recent_emergencies,
        'companies_with_most_trips': companies_with_most_trips,
    }
    
    return render(request, 'dashboard/admin_dashboard.html', context)

@login_required
def company_list(request):
    # Ensure the user is an administrator
    if not request.user.is_administrator():
        messages.error(request, "You don't have permission to access this page.")
        return redirect('home')
    
    # Get search query
    query = request.GET.get('q', '')
    
    if query:
        companies = Company.objects.filter(
            Q(name__icontains=query) | 
            Q(registration_number__icontains=query) |
            Q(user__email__icontains=query)
        )
    else:
        companies = Company.objects.all()
    
    context = {
        'companies': companies,
        'query': query,
    }
    
    return render(request, 'dashboard/company_list.html', context)

@login_required
def company_detail(request, pk):
    # Ensure the user is an administrator
    if not request.user.is_administrator():
        messages.error(request, "You don't have permission to access this page.")
        return redirect('home')
    
    company = get_object_or_404(Company, pk=pk)
    
    # Get company statistics
    total_vehicles = Vehicle.objects.filter(company=company).count()
    total_trips = Trip.objects.filter(company=company).count()
    
    # Recent trips
    recent_trips = Trip.objects.filter(company=company).order_by('-departure_time')[:10]
    
    # Recent emergencies - fixed to use trips__company instead of trip__company
    recent_emergencies = Emergency.objects.filter(trip__company=company).order_by('-reported_time')[:5]
    
    # Monthly trip counts
    today = timezone.now().date()
    month_start = today.replace(day=1)
    monthly_trips = Trip.objects.filter(
        company=company,
        departure_time__gte=month_start
    ).count()
    
    context = {
        'company': company,
        'total_vehicles': total_vehicles,
        'total_trips': total_trips,
        'monthly_trips': monthly_trips,
        'recent_trips': recent_trips,
        'recent_emergencies': recent_emergencies,
    }
    
    return render(request, 'dashboard/company_detail.html', context)

@login_required
def system_statistics(request):
    # Ensure the user is an administrator
    if not request.user.is_administrator():
        messages.error(request, "You don't have permission to access this page.")
        return redirect('home')
    
    # Get date range
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    
    # Default to last 30 days if no dates provided
    if not date_from or not date_to:
        date_to = timezone.now().date()
        date_from = date_to - timedelta(days=30)
    
    # Get trips in date range
    trips = Trip.objects.filter(
        departure_time__date__gte=date_from,
        departure_time__date__lte=date_to
    )
    
    # Calculate statistics
    total_trips = trips.count()
    total_passengers = sum(trip.total_passengers() for trip in trips)
    total_revenue = sum(trip.total_fee() for trip in trips)
    
    # Trips by company - fixed to use 'trips' instead of 'trip'
    trips_by_company = Company.objects.annotate(
        trip_count=Count('trips', filter=Q(
            trips__departure_time__date__gte=date_from,
            trips__departure_time__date__lte=date_to
        ))
    ).order_by('-trip_count')
    
    # Emergencies by type
    emergencies = Emergency.objects.filter(
        reported_time__date__gte=date_from,
        reported_time__date__lte=date_to
    )
    emergencies_by_type = emergencies.values('emergency_type').annotate(count=Count('id'))
    
    context = {
        'date_from': date_from,
        'date_to': date_to,
        'total_trips': total_trips,
        'total_passengers': total_passengers,
        'total_revenue': total_revenue,
        'trips_by_company': trips_by_company,
        'emergencies_by_type': emergencies_by_type,
    }
    
    return render(request, 'dashboard/system_statistics.html', context)

@login_required
def emergency_monitoring(request):
    # Ensure the user is an administrator
    if not request.user.is_administrator():
        messages.error(request, "You don't have permission to access this page.")
        return redirect('home')
    
    # Filter options
    status = request.GET.get('status', 'all')
    
    # Base queryset
    emergencies = Emergency.objects.all().order_by('-reported_time')
    
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
    
    return render(request, 'dashboard/emergency_monitoring.html', context)

@login_required
def update_emergency_status(request, pk):
    # Ensure the user is an administrator
    if not request.user.is_administrator():
        messages.error(request, "You don't have permission to access this page.")
        return redirect('home')
    
    emergency = get_object_or_404(Emergency, pk=pk)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['reported', 'in_progress', 'resolved']:
            emergency.status = new_status
            emergency.save()
            messages.success(request, f"Emergency status updated to {emergency.get_status_display()}.")
        else:
            messages.error(request, "Invalid status selected.")
        
        return redirect('emergency_detail_admin', pk=emergency.id)
    
    context = {
        'emergency': emergency,
    }
    
    return render(request, 'dashboard/update_emergency_status.html', context)

@login_required
def emergency_detail_admin(request, pk):
    # Ensure the user is an administrator
    if not request.user.is_administrator():
        messages.error(request, "You don't have permission to access this page.")
        return redirect('home')
    
    emergency = get_object_or_404(Emergency, pk=pk)
    
    context = {
        'emergency': emergency,
    }
    
    return render(request, 'dashboard/emergency_detail_admin.html', context)




# //////////////////////////////////////////////////////////////////////////
@login_required
def admin_trip_list(request):
    # Ensure the user is an administrator
    if not request.user.is_administrator():
        messages.error(request, "You don't have permission to access this page.")
        return redirect('home')
    
    # Filter options
    status = request.GET.get('status', 'all')
    company_id = request.GET.get('company', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    
    # Base queryset
    trips = Trip.objects.all().order_by('-departure_time')
    
    # Apply filters
    if status == 'upcoming':
        trips = trips.filter(departure_time__gt=timezone.now(), is_completed=False)
    elif status == 'completed':
        trips = trips.filter(is_completed=True)
    elif status == 'today':
        today = timezone.now().date()
        trips = trips.filter(departure_time__date=today)
    
    if company_id:
        trips = trips.filter(company_id=company_id)
    
    if date_from:
        trips = trips.filter(departure_time__date__gte=date_from)
    
    if date_to:
        trips = trips.filter(departure_time__date__lte=date_to)
    
    # Get all companies for the filter dropdown
    companies = Company.objects.all()
    
    context = {
        'trips': trips,
        'status': status,
        'company_id': company_id,
        'date_from': date_from,
        'date_to': date_to,
        'companies': companies,
    }
    
    return render(request, 'dashboard/admin_trip_list.html', context)