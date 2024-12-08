from django.db import models

class Device(models.Model):
    hostname = models.CharField(max_length=100)
    mac_address = models.CharField(max_length=17, unique=True)
    
    def __str__(self):
        return self.hostname

class ScanResult(models.Model):
    device = models.ForeignKey(Device, related_name='scan_results', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    os_name = models.CharField(max_length=100)
    os_version = models.CharField(max_length=100)
    available_disk = models.CharField(max_length=100)
    free_disk_space = models.CharField(max_length=100)
    total_disk_space = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.device.hostname} - {self.timestamp}"
