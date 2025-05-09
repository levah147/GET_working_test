from django.urls import path
from . import views

urlpatterns = [
    path('vehicles/', views.vehicle_list, name='vehicle_list'),
    path('vehicles/add/', views.add_vehicle, name='add_vehicle'),
    path('create/', views.create_trip, name='create_trip'),
    path('list/', views.trip_list, name='trip_list'),
    path('detail/<int:pk>/', views.trip_detail, name='trip_detail'),
    path('add-passenger/<int:trip_id>/', views.add_passenger_to_trip, name='add_passenger_to_trip'),
    path('complete/<int:trip_id>/', views.complete_trip, name='complete_trip'),
    
    
    # Vehicle management URLs
    path('vehicles/<int:pk>/edit/', views.edit_vehicle, name='edit_vehicle'),
    path('vehicles/<int:pk>/delete/', views.delete_vehicle, name='delete_vehicle'),
    
    
    path('trips/', views.trip_list, name='trip_list'),
    
]