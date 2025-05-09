from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    # path('companies/', include('companies.urls')),
    path('passengers/', include('passengers.urls')),
    path('trips/', include('trips.urls')),
    path('payments/', include('payments.urls')),
    path('emergencies/', include('emergencies.urls')),
    path('dashboard/', include('dashboard.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

