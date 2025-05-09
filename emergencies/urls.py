from django.urls import path
from . import views

urlpatterns = [
    path('report/', views.report_emergency, name='report_emergency'),
    path('list/', views.emergency_list, name='emergency_list'),
    path('detail/<int:pk>/', views.emergency_detail, name='emergency_detail'),
]