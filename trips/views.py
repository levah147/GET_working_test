from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q

from .models import Trip, Vehicle, TripPassenger
from .forms import TripForm, VehicleForm, AddPassengerToTripForm
from passengers.models import Passenger
from payments.models import Payment
import uuid

@login_required
def vehicle_list(request):
    """Display a list of vehicles for the company."""
    # Check if the user has a company
    try:
        # Determine which attribute to use based on your model structure
        # Use either company or company_profile consistently
        if hasattr(request.user, 'company'):
            company = request.user.company
        elif hasattr(request.user, 'company_profile'):
            company = request.user.company_profile
        else:
            messages.error(request, "You don't have a company profile. Please register your company first.")
            return redirect('home')
        
        vehicles = Vehicle.objects.filter(company=company)
        
        context = {
            'vehicles': vehicles,
        }
        
        return render(request, 'trips/vehicle_list.html', context)
    
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('home')

@login_required
def add_vehicle(request):
    """Add a new vehicle for the company."""
    # Check if the user has a company
    try:
        # Use the same attribute as in vehicle_list
        if hasattr(request.user, 'company'):
            company = request.user.company
        elif hasattr(request.user, 'company_profile'):
            company = request.user.company_profile
        else:
            messages.error(request, "You don't have a company profile. Please register your company first.")
            return redirect('home')
        
        if request.method == 'POST':
            plate_number = request.POST.get('plate_number')
            vehicle_type = request.POST.get('vehicle_type')
            capacity = request.POST.get('capacity')
            model = request.POST.get('model')
            year = request.POST.get('year')
            description = request.POST.get('description')
            
            # Validate data
            if not all([plate_number, vehicle_type, capacity]):
                messages.error(request, "Please fill in all required fields.")
                return render(request, 'trips/add_vehicle.html')
            
            # Check if plate number already exists
            if Vehicle.objects.filter(plate_number=plate_number).exists():
                messages.error(request, "A vehicle with this plate number already exists.")
                return render(request, 'trips/add_vehicle.html')
            
            # Create the vehicle
            vehicle = Vehicle.objects.create(
                company=company,
                plate_number=plate_number,
                vehicle_type=vehicle_type,
                capacity=capacity,
                model=model,
                year=year,
                description=description
            )
            
            messages.success(request, f"Vehicle {vehicle.plate_number} added successfully.")
            return redirect('vehicle_list')
        
        return render(request, 'trips/add_vehicle.html')
    
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('home')

@login_required
def create_trip(request):
    # Check if the user has a company
    try:
        # Use the same attribute as in other views
        if hasattr(request.user, 'company'):
            company = request.user.company
        elif hasattr(request.user, 'company_profile'):
            company = request.user.company_profile
        else:
            messages.error(request, "You don't have a company profile. Please register your company first.")
            return redirect('home')
        
        if request.method == 'POST':
            form = TripForm(request.POST, company=company)
            if form.is_valid():
                trip = form.save(commit=False)
                trip.company = company
                trip.save()
                messages.success(request, f"Trip to {trip.destination} created successfully.")
                return redirect('trip_detail', pk=trip.id)
        else:
            form = TripForm(company=company)
        
        context = {
            'form': form,
        }
        
        return render(request, 'trips/create_trip.html', context)
    
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('home')

@login_required
def trip_list(request):
    # Check if the user has a company
    try:
        # Use the same attribute as in other views
        if hasattr(request.user, 'company'):
            company = request.user.company
        elif hasattr(request.user, 'company_profile'):
            company = request.user.company_profile
        else:
            messages.error(request, "You don't have a company profile. Please register your company first.")
            return redirect('home')
        
        # Filter options
        status = request.GET.get('status', 'all')
        date_from = request.GET.get('date_from', '')
        date_to = request.GET.get('date_to', '')
        
        # Base queryset
        trips = Trip.objects.filter(company=company).order_by('-departure_time')
        
        # Apply filters
        if status == 'upcoming':
            trips = trips.filter(departure_time__gt=timezone.now(), is_completed=False)
        elif status == 'completed':
            trips = trips.filter(is_completed=True)
        elif status == 'today':
            today = timezone.now().date()
            trips = trips.filter(departure_time__date=today)
        
        if date_from:
            trips = trips.filter(departure_time__date__gte=date_from)
        
        if date_to:
            trips = trips.filter(departure_time__date__lte=date_to)
        
        context = {
            'trips': trips,
            'status': status,
            'date_from': date_from,
            'date_to': date_to,
        }
        
        return render(request, 'trips/trip_list.html', context)
    
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('home')

@login_required
def trip_detail(request, pk):
    # Check if the user has a company
    try:
        # Use the same attribute as in other views
        if hasattr(request.user, 'company'):
            company = request.user.company
        elif hasattr(request.user, 'company_profile'):
            company = request.user.company_profile
        else:
            messages.error(request, "You don't have a company profile. Please register your company first.")
            return redirect('home')
        
        trip = get_object_or_404(Trip, pk=pk, company=company)
        
        # Get passengers for this trip
        trip_passengers = TripPassenger.objects.filter(trip=trip).select_related('passenger')
        
        # Check if payment exists
        try:
            payment = Payment.objects.get(trip=trip)
        except Payment.DoesNotExist:
            payment = None
        
        context = {
            'trip': trip,
            'trip_passengers': trip_passengers,
            'payment': payment,
        }
        
        return render(request, 'trips/trip_detail.html', context)
    
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('home')

@login_required
def edit_vehicle(request, pk):
    """Edit an existing vehicle."""
    # Check if the user has a company
    try:
        # Use the same attribute as in other views
        if hasattr(request.user, 'company'):
            company = request.user.company
        elif hasattr(request.user, 'company_profile'):
            company = request.user.company_profile
        else:
            messages.error(request, "You don't have a company profile. Please register your company first.")
            return redirect('home')
        
        # Get the vehicle and ensure it belongs to the company
        vehicle = get_object_or_404(Vehicle, pk=pk)
        if vehicle.company != company:
            messages.error(request, "You don't have permission to edit this vehicle.")
            return redirect('vehicle_list')
        
        if request.method == 'POST':
            plate_number = request.POST.get('plate_number')
            vehicle_type = request.POST.get('vehicle_type')
            capacity = request.POST.get('capacity')
            model = request.POST.get('model')
            year = request.POST.get('year')
            description = request.POST.get('description')
            
            # Validate data
            if not all([plate_number, vehicle_type, capacity]):
                messages.error(request, "Please fill in all required fields.")
                return render(request, 'trips/edit_vehicle.html', {'vehicle': vehicle})
            
            # Check if plate number already exists (excluding this vehicle)
            if Vehicle.objects.filter(plate_number=plate_number).exclude(pk=pk).exists():
                messages.error(request, "A vehicle with this plate number already exists.")
                return render(request, 'trips/edit_vehicle.html', {'vehicle': vehicle})
            
            # Update the vehicle
            vehicle.plate_number = plate_number
            vehicle.vehicle_type = vehicle_type
            vehicle.capacity = capacity
            vehicle.model = model
            vehicle.year = year
            vehicle.description = description
            vehicle.save()
            
            messages.success(request, f"Vehicle {vehicle.plate_number} updated successfully.")
            return redirect('vehicle_list')
        
        context = {
            'vehicle': vehicle,
        }
        
        return render(request, 'trips/edit_vehicle.html', context)
    
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('home')

@login_required
def delete_vehicle(request, pk):
    """Delete a vehicle."""
    # Check if the user has a company
    try:
        # Use the same attribute as in other views
        if hasattr(request.user, 'company'):
            company = request.user.company
        elif hasattr(request.user, 'company_profile'):
            company = request.user.company_profile
        else:
            messages.error(request, "You don't have a company profile. Please register your company first.")
            return redirect('home')
        
        # Get the vehicle and ensure it belongs to the company
        vehicle = get_object_or_404(Vehicle, pk=pk)
        if vehicle.company != company:
            messages.error(request, "You don't have permission to delete this vehicle.")
            return redirect('vehicle_list')
        
        # Check if the vehicle is used in any trips
        if vehicle.trips.exists():
            messages.error(request, "This vehicle cannot be deleted because it is used in one or more trips.")
            return redirect('vehicle_list')
        
        if request.method == 'POST':
            plate_number = vehicle.plate_number
            vehicle.delete()
            messages.success(request, f"Vehicle {plate_number} deleted successfully.")
            return redirect('vehicle_list')
        
        context = {
            'vehicle': vehicle,
        }
        
        return render(request, 'trips/delete_vehicle.html', context)
    
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('home')

# Implement the remaining functions (add_passenger_to_trip, complete_trip) with the same pattern
@login_required
def add_passenger_to_trip(request, trip_id):
    # Check if the user has a company
    try:
        # Use the same attribute as in other views
        if hasattr(request.user, 'company'):
            company = request.user.company
        elif hasattr(request.user, 'company_profile'):
            company = request.user.company_profile
        else:
            messages.error(request, "You don't have a company profile. Please register your company first.")
            return redirect('home')
        
        trip = get_object_or_404(Trip, pk=trip_id, company=company)
        
        if request.method == 'POST':
            form = AddPassengerToTripForm(request.POST, trip=trip)
            if form.is_valid():
                passenger = form.cleaned_data['passenger']
                seat_number = form.cleaned_data['seat_number']
                
                # Create the trip passenger record
                TripPassenger.objects.create(
                    trip=trip,
                    passenger=passenger,
                    seat_number=seat_number
                )
                
                messages.success(request, f"Passenger {passenger.full_name} added to trip successfully.")
                
                # Check if we should add another passenger
                if 'add_another' in request.POST:
                    return redirect('add_passenger_to_trip', trip_id=trip.id)
                
                return redirect('trip_detail', pk=trip.id)
        else:
            form = AddPassengerToTripForm(trip=trip)
        
        context = {
            'form': form,
            'trip': trip,
        }
        
        return render(request, 'trips/add_passenger_to_trip.html', context)
    
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('home')

@login_required
def complete_trip(request, trip_id):
    # Check if the user has a company
    try:
        # Use the same attribute as in other views
        if hasattr(request.user, 'company'):
            company = request.user.company
        elif hasattr(request.user, 'company_profile'):
            company = request.user.company_profile
        else:
            messages.error(request, "You don't have a company profile. Please register your company first.")
            return redirect('home')
        
        trip = get_object_or_404(Trip, pk=trip_id, company=company)
        
        if request.method == 'POST':
            trip.is_completed = True
            trip.save()
            
            # Create payment record if it doesn't exist
            total_amount = trip.total_fee()
            
            if total_amount > 0:
                Payment.objects.get_or_create(
                    trip=trip,
                    defaults={
                        'amount': total_amount,
                        'payment_status': 'pending',
                        'payment_method': 'cash',
                        'reference': f"GTE-{uuid.uuid4().hex[:8].upper()}"
                    }
                )
            
            messages.success(request, f"Trip to {trip.destination} marked as completed.")
            return redirect('trip_detail', pk=trip.id)
        
        context = {
            'trip': trip,
        }
        
        return render(request, 'trips/complete_trip.html', context)
    
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('home')