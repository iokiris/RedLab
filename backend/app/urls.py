from django.urls import path
from . import views
urlpatterns = [
    path('web-response-time/', views.web_response_time, name='web_response_time'),
    path('throughput/', views.throughput, name='throughput'),
    path('apdex/', views.apdex, name='apdex'),
    path('error-rate/', views.error_rate, name='error_rate'),
    path('time-sector/', views.time_sector, name='time_sector'),
]