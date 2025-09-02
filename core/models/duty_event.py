from django.db import models
from .base import BaseModel
from .log import DailyLog


class DutyEvent(BaseModel):
    """Represents a duty status block in the log grid."""
    DUTY_STATUSES = [
        ("OFF", "Off Duty"),
        ("SLEEPER", "Sleeper Berth"),
        ("DRIVING", "Driving"),
        ("ON_DUTY", "On Duty (Not Driving)"),
    ]

    log = models.ForeignKey(
        DailyLog, on_delete=models.CASCADE, related_name="events"
    )
    status = models.CharField(max_length=20, choices=DUTY_STATUSES)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=255, null=False, blank=False)

    @property
    def duration_hours(self):
        return (self.end_time - self.start_time).total_seconds() / 3600

    def __str__(self):
        return f"{self.status} ({self.start_time} - {self.end_time})"
