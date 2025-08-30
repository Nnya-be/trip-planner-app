from core.models import Trip
from core.validators.trip_validator import TripValidator
from core.exceptions.trip_exceptions import TripNotFound


class TripService:
    @staticmethod
    def create_trip(driver, data: dict) -> Trip:
        TripValidator.validate_locations(data["pickup_location"], data["dropoff_location"])
        return Trip.objects.create(
            driver=driver,
            current_location=data.get("current_location"),
            pickup_location=data["pickup_location"],
            dropoff_location=data["dropoff_location"],
            cycle_hours_used=data.get("cycle_hours_used", 0),
        )

    @staticmethod
    def get_trip(trip_id: str) -> Trip:
        try:
            return Trip.objects.get(id=trip_id)
        except Trip.DoesNotExist:
            raise TripNotFound()
