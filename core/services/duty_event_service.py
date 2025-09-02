from core.models import DutyEvent, DailyLog
from core.validators.duty_event_validator import DutyEventValidator


class DutyEventService:
    @staticmethod
    def add_event(log: DailyLog, data: dict) -> DutyEvent:
        DutyEventValidator.validate_time_range(data["start_time"], data["end_time"])
        return DutyEvent.objects.create(
            log=log,
            status=data["status"],
            start_time=data["start_time"],
            end_time=data["end_time"],
            location=data.get("location", ""),
        )
