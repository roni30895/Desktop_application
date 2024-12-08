# devices/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Device
from .serializers import DeviceSerializer, ScanResultSerializer
from .services import register_device, save_scan_result, get_device_scan_results
from django.http import JsonResponse
from .models import Device, ScanResult



class RegisterDeviceView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        hostname = data.get('hostname')
        mac_address = data.get('mac_address')

        if not hostname or not mac_address:
            return Response({"error": "Hostname and MAC address are required."}, status=status.HTTP_400_BAD_REQUEST)

        device = register_device(hostname, mac_address)
        return Response(DeviceSerializer(device).data, status=status.HTTP_201_CREATED)

class SaveScanResultsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        mac_address = data.get('mac_address')
        hostname = data.get('hostname')
        os_name = data.get('os_name')
        os_version = data.get('os_version')
        available_disk = data.get('available_disk')
        free_disk_space = data.get('free_disk_space')
        total_disk_space = data.get('total_disk_space')

        if not all([mac_address, hostname, os_name, os_version]):
            return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

        scan_result = save_scan_result(mac_address, hostname, os_name, os_version, available_disk, free_disk_space, total_disk_space)
        return Response(ScanResultSerializer(scan_result).data, status=status.HTTP_201_CREATED)

class ViewAllDevicesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        device_data = []
        try:
            devices = Device.objects.all()
            for device in devices:
                # Fetch scan results for the device
                scan_results = get_device_scan_results(device.mac_address)
                
                # Check if scan results are found
                if scan_results is not None:
                    device_data.append({
                        'device': DeviceSerializer(device).data,
                        'scan_results': ScanResultSerializer(scan_results, many=True).data
                    })
                else:
                    device_data.append({
                        'device': DeviceSerializer(device).data,
                        'scan_results': []  # Empty scan results if there's an issue
                    })
            
            return Response(device_data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def get_device_scan_results(mac_address):
    try:
        # Assuming ScanResult is related to Device via mac_address
        return ScanResult.objects.filter(device__mac_address=mac_address)
    except Exception as e:
        return None
