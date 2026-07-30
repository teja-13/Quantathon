"""
URL Configuration for Cancer Detection & Reporting System project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render

def custom_404_view(request, exception=None):
    return render(request, 'errors/404.html', status=404)

def custom_500_view(request):
    return render(request, 'errors/500.html', status=500)

handler404 = 'config.urls.custom_404_view'
handler500 = 'config.urls.custom_500_view'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls', namespace='dashboard')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('patients/', include('patients.urls', namespace='patients')),
    path('diagnosis/', include('diagnosis.urls', namespace='diagnosis')),
    path('reports/', include('reports.urls', namespace='reports')),
    path('history/', include('history.urls', namespace='history')),
    path('settings/', include('system_settings.urls', namespace='system_settings')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
