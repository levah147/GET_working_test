from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_passenger, name='register_passenger'),
    path('list/', views.passenger_list, name='passenger_list'),
    path('detail/<int:pk>/', views.passenger_detail, name='passenger_detail'),
]