from rest_framework import serializers
from .models import Device, ScanResult

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['hostname', 'mac_address']

class ScanResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScanResult
        fields = ['timestamp', 'mac_address', 'hostname', 'os_name', 'os_version', 'available_disk', 'free_disk_space', 'total_disk_space']
