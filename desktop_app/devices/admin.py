from django.contrib import admin

# Register your models here.
from .models import Device, ScanResult

admin.site.register(Device)

admin.site.register(ScanResult)