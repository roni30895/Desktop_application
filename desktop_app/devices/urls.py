from django.urls import path
from . import views

urlpatterns = [
    path('register_device/', views.register_device, name='register_device'),
    path('save_scan_results/', views.save_scan_results, name='save_scan_results'),
    path('view_all_devices/', views.view_all_devices, name='view_all_devices'),
    path('view_scan_results/<str:hostname>/', views.view_scan_results, name='view_scan_results'),
]
