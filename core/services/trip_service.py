from core.models import Trip
from core.validators.trip_validator import TripValidator
from core.exceptions.trip_exceptions import TripNotFound


class TripService:
    @staticmethod
    def create_trip(driver, data: dict) -> Trip:
        from core.models.log import Logbook, DailyLog
        from datetime import date
        TripValidator.validate_locations(data["pickup_location"], data["dropoff_location"])
        trip = Trip.objects.create(
            driver=driver,
            current_location=data.get("current_location"),
            pickup_location=data["pickup_location"],
            dropoff_location=data["dropoff_location"],
            cycle_hours_used=data.get("cycle_hours_used"),
        )
        # Create logbook and today's daily log for the trip
        Logbook.objects.create(trip=trip)
        DailyLog.objects.create(trip=trip, date=date.today())
        return trip

    @staticmethod
    def get_trip(trip_id: str) -> Trip:
        try:
            return Trip.objects.get(id=trip_id)
        except Trip.DoesNotExist:
            raise TripNotFound()
