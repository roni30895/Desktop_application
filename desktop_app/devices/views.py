from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Device, ScanResult
from .serializers import DeviceSerializer, ScanResultSerializer

# Register Device
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def register_device(request):
    if request.method == 'POST':
        hostname = request.data.get('hostname')
        mac_address = request.data.get('mac_address')

        if not hostname or not mac_address:
            return Response({'error': 'Hostname and MAC Address are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if device already exists
        device, created = Device.objects.get_or_create(mac_address=mac_address, defaults={'hostname': hostname})

        if created:
            return Response({'message': 'Device registered successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Device already exists'}, status=status.HTTP_200_OK)

# Save Scan Results
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def save_scan_results(request):
    if request.method == 'POST':
        mac_address = request.data.get('mac_address')
        scan_data = request.data.get('scan_data')

        if not mac_address or not scan_data:
            return Response({'error': 'MAC Address and Scan data are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            device = Device.objects.get(mac_address=mac_address)
        except Device.DoesNotExist:
            return Response({'error': 'Device not found'}, status=status.HTTP_404_NOT_FOUND)

        scan_result = ScanResult.objects.create(
            device=device,
            os_name=scan_data.get('os_name'),
            os_version=scan_data.get('os_version'),
            available_disk=scan_data.get('available_disk'),
            free_disk_space=scan_data.get('free_disk_space'),
            total_disk_space=scan_data.get('total_disk_space'),
        )

        return Response({'message': 'Scan results saved successfully'}, status=status.HTTP_201_CREATED)

# View All Devices
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def view_all_devices(request):
    if request.method == 'GET':
        devices = Device.objects.all()
        serializer = DeviceSerializer(devices, many=True)
        return Response(serializer.data)

# View Scan Results for a Device
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def view_scan_results(request, device_id):
    if request.method == 'GET':
        try:
            device = Device.objects.get(id=device_id)
            scan_results = ScanResult.objects.filter(device=device)
            serializer = ScanResultSerializer(scan_results, many=True)
            return Response(serializer.data)
        except Device.DoesNotExist:
            return Response({'error': 'Device not found'}, status=status.HTTP_404_NOT_FOUND)
