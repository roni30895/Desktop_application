from .models import Device, ScanResult
from django.core.exceptions import ObjectDoesNotExist

def register_device(hostname, mac_address):
    device, created = Device.objects.get_or_create(mac_address=mac_address, hostname=hostname)
    return device

def save_scan_result(mac_address, hostname, os_name, os_version, available_disk, free_disk_space, total_disk_space):
    scan_result = ScanResult(
        mac_address=mac_address,
        hostname=hostname,
        os_name=os_name,
        os_version=os_version,
        available_disk=available_disk,
        free_disk_space=free_disk_space,
        total_disk_space=total_disk_space,
    )
    scan_result.save()
    return scan_result

def get_device_scan_results(mac_address):
    try:
        device = Device.objects.get(mac_address=mac_address)
        return ScanResult.objects.filter(device=device)
    except ObjectDoesNotExist:
        return None
