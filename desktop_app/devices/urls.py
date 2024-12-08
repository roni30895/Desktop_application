from django.urls import path
from .views import RegisterDeviceView, SaveScanResultsView, ViewAllDevicesView

urlpatterns = [
    path('register_device/', RegisterDeviceView.as_view(), name='register_device'),
    path('save_scan_results/', SaveScanResultsView.as_view(), name='save_scan_results'),
    path('view_all_devices/', ViewAllDevicesView.as_view(), name='view_all_devices'),
]
