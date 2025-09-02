from django.db import models
from .base import BaseModel
from .trip import Trip


class DailyLog(BaseModel):
    """A 24-hour log sheet with duty events."""
    trip = models.ForeignKey(
        Trip, on_delete=models.CASCADE, related_name="logs"
    )
    date = models.DateField()

    class Meta:
        unique_together = ("trip", "date")

    def __str__(self):
        return f"Log for {self.trip} on {self.date}"


class Logbook(BaseModel):
    """A collection of daily logs across a multi-day trip."""
    trip = models.OneToOneField(
        Trip, on_delete=models.CASCADE, related_name="logbook"
    )

    def __str__(self):
        return f"Logbook for {self.trip}"
