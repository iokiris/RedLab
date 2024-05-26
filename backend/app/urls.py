from django.urls import path
from . import views
urlpatterns = [
    path('web-response-time/', views.web_response_time, name='web_response_time'),
    path('throughput/', views.throughput, name='throughput'),
    path('apdex/', views.apdex, name='apdex'),
    path('error-rate/', views.error_rate, name='error_rate'),
    path('time-sector/', views.time_sector, name='time_sector'),
    path('anomaly-stats/', views.anomaly_stats, name='anomaly_stats'),
    path('all-metrics', views.get_all_metrics, name='all_metrics'),
    path('fdwa/', views.full_data_with_anomalys, name='fdwa'),
    path('enchanced_wr/', views.enchanced_wr, name='enchanced_wr'),
    path('enchanced_thq/', views.enchanced_thq, name='enchanced_thq'),
    path('enchanced_apdex/', views.enchanced_apdex, name='enchanced_apdex'),
    path('enchanced_all/', views.enchanced_all, name='enchanced_all'),
    path('enchanced_fwda/', views.enchanced_fwda, name='enchanced_fwda')
]