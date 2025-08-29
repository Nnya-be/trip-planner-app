from django.db import models
from .base import BaseModel
from .trip import Trip


class RouteSegment(BaseModel):
    """Represents one leg of a route between two stops."""
    trip = models.ForeignKey(
        Trip, on_delete=models.CASCADE, related_name="segments"
    )
    start = models.CharField(max_length=255)
    end = models.CharField(max_length=255)
    distance_miles = models.FloatField()
    duration_hours = models.FloatField()
    requires_fuel_stop = models.BooleanField(default=False)
    requires_rest_break = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.start} → {self.end} ({self.distance_miles} mi)"
