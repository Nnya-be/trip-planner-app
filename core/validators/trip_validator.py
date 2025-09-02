from core.exceptions.trip_exceptions import InvalidTripData


class TripValidator:
    @staticmethod
    def validate_locations(pickup, dropoff):
        if pickup == dropoff:
            raise InvalidTripData("Pickup and dropoff cannot be the same.")
