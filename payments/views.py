from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Payment

@login_required
def process_payment(request, payment_id):
    # Ensure the user is a company
    if not request.user.is_company():
        messages.error(request, "You don't have permission to access this page.")
        return redirect('home')
    
    company = request.user.company_profile
    payment = get_object_or_404(Payment, id=payment_id, trip__company=company)
    
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        
        if payment_method:
            payment.payment_method = payment_method
            payment.payment_status = 'completed'
            payment.save()
            
            messages.success(request, f"Payment of ₦{payment.amount} processed successfully.")
            return redirect('trip_detail', pk=payment.trip.id)
    
    context = {
        'payment': payment,
    }
    
    return render(request, 'payments/process_payment.html', context)

@login_required
def payment_history(request):
    # Ensure the user is a company
    if not request.user.is_company():
        messages.error(request, "You don't have permission to access this page.")
        return redirect('home')
    
    company = request.user.company_profile
    
    # Filter options
    status = request.GET.get('status', 'all')
    
    # Base queryset
    payments = Payment.objects.filter(trip__company=company).order_by('-payment_date')
    
    # Apply filters
    if status == 'completed':
        payments = payments.filter(payment_status='completed')
    elif status == 'pending':
        payments = payments.filter(payment_status='pending')
    elif status == 'failed':
        payments = payments.filter(payment_status='failed')
    
    context = {
        'payments': payments,
        'status': status,
    }
    
    return render(request, 'payments/payment_history.html', context)