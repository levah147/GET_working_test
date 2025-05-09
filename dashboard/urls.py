# Update your existing dashboard/urls.py file

from django.urls import path
from . import views

urlpatterns = [
    path('company/', views.company_dashboard, name='company_dashboard'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/companies/', views.company_list, name='admin_company_list'),
    path('admin/companies/<int:pk>/', views.company_detail, name='admin_company_detail'),
    path('admin/statistics/', views.system_statistics, name='admin_system_statistics'),
    path('admin/emergencies/', views.emergency_monitoring, name='admin_emergency_monitoring'),
    path('admin/emergencies/<int:pk>/', views.emergency_detail_admin, name='emergency_detail_admin'),
    path('admin/emergencies/<int:pk>/update/', views.update_emergency_status, name='update_emergency_status'),
    
    path('admin/trips/', views.admin_trip_list, name='admin_trip_list'),
    
]