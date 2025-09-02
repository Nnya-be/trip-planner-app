from django.db import models
from django.conf import settings
from .base import BaseModel


class Trip(BaseModel):
    """Represents a trip planned by a driver."""
    driver = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="trips"
    )
    current_location = models.CharField(max_length=255)
    pickup_location = models.CharField(max_length=255)
    dropoff_location = models.CharField(max_length=255)
    cycle_hours_used = models.FloatField(default=0)  # Hours already used in 70/8 cycle

    def __str__(self):
        return f"Trip {self.id} by {self.driver}"
