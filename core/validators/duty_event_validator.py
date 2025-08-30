from core.exceptions.duty_event_exceptions import InvalidDutyEvent


class DutyEventValidator:
    @staticmethod
    def validate_time_range(start, end):
        if start >= end:
            raise InvalidDutyEvent("End time must be after start time.")
