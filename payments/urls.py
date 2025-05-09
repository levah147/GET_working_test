from django.urls import path
from . import views

urlpatterns = [
    path('process/<int:payment_id>/', views.process_payment, name='process_payment'),
    path('history/', views.payment_history, name='payment_history'),
]