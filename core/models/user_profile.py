from django.db import models
from django.conf import settings
from .base import BaseModel


class DriverProfile(BaseModel):
    """Extended profile for a driver."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="driver_profile"
    )
    license_number = models.CharField(max_length=50, unique=True)
    cycle_limit_hours = models.IntegerField(default=70)  # 70hrs/8days by default

    def __str__(self):
        return f"Driver Profile: {self.user.username}"


class DispatcherProfile(BaseModel):
    """Extended profile for a dispatcher/admin."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="dispatcher_profile"
    )
    company_name = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return f"Dispatcher Profile: {self.user.username}"
