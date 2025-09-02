from django.db import models
from django.conf import settings
from .base import BaseModel



class DriverProfile(BaseModel):
    """Extended profile for a driver."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="driver_profile"
    )
    name = models.CharField(max_length=255, null=False, blank=False,default="Unknown")
    co_driver_name = models.CharField(max_length=255, blank=True)
    carrier_name = models.CharField(max_length=255, null=True)
    license_number = models.CharField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=20, null=False, blank=False,default="000-000-0000")
    cycle_limit_hours = models.IntegerField(default=70)  # 70hrs/8days by default

    def __str__(self):
        return f"Driver Profile: {self.user.username}"


class VehicleInfo(BaseModel):
    driver_profile = models.OneToOneField(DriverProfile, on_delete=models.CASCADE, related_name="vehicle_info")
    truck_number = models.CharField(max_length=50, null=True, blank=True)
    trailer_number = models.CharField(max_length=50, null=True, blank=True)
    eld_device_id = models.CharField(max_length=100, null=True, blank=True)
    vin_number = models.CharField(max_length=100, null=True, blank=True)
    plate_number = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"Vehicle Info for {self.driver_profile.user.username}"


class DispatcherProfile(BaseModel):
    """Extended profile for a dispatcher/admin."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="dispatcher_profile"
    )
    company_name = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return f"Dispatcher Profile: {self.user.username}"
