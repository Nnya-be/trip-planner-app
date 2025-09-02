from .base import DomainException


class InvalidTripData(DomainException):
    status_code = 400
    default_detail = "Invalid trip data provided."
    default_code = "invalid_trip"


class TripNotFound(DomainException):
    status_code = 404
    default_detail = "Trip not found."
    default_code = "trip_not_found"
