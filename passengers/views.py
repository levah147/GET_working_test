from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .models import Passenger
from .forms import PassengerForm

@login_required
def register_passenger(request):
    # Ensure the user is a company
    if not request.user.is_company():
        messages.error(request, "You don't have permission to access this page.")
        return redirect('home')
    
    if request.method == 'POST':
        form = PassengerForm(request.POST)
        if form.is_valid():
            passenger = form.save()
            messages.success(request, f"Passenger {passenger.full_name} registered successfully.")
            
            # Check if we need to add this passenger to a trip
            next_url = request.POST.get('next')
            if next_url and 'add_passenger_to_trip' in next_url:
                return redirect(next_url)
            
            return redirect('passenger_list')
    else:
        form = PassengerForm()
    
    context = {
        'form': form,
        'next': request.GET.get('next', ''),
    }
    
    return render(request, 'passengers/register_passenger.html', context)

@login_required
def passenger_list(request):
    # Ensure the user is a company
    if not request.user.is_company():
        messages.error(request, "You don't have permission to access this page.")
        return redirect('home')
    
    # Get search query
    query = request.GET.get('q', '')
    
    if query:
        passengers = Passenger.objects.filter(
            Q(full_name__icontains=query) | 
            Q(phone_number__icontains=query)
        )
    else:
        passengers = Passenger.objects.all()
    
    context = {
        'passengers': passengers,
        'query': query,
    }
    
    return render(request, 'passengers/passenger_list.html', context)

@login_required
def passenger_detail(request, pk):
    # Ensure the user is a company
    if not request.user.is_company():
        messages.error(request, "You don't have permission to access this page.")
        return redirect('home')
    
    passenger = get_object_or_404(Passenger, pk=pk)
    
    # Get passenger's trip history
    trips = passenger.trips.all().order_by('-trip__departure_time')
    
    context = {
        'passenger': passenger,
        'trips': trips,
    }
    
    return render(request, 'passengers/passenger_detail.html', context)