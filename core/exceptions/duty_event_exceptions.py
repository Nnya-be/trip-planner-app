from .base import DomainException


class InvalidDutyEvent(DomainException):
    status_code = 400
    default_detail = "Invalid duty event."
    default_code = "invalid_event"
