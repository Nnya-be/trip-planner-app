from core.models import RouteSegment, Trip


class RouteSegmentService:
    @staticmethod
    def add_segment(trip: Trip, data: dict) -> RouteSegment:
        return RouteSegment.objects.create(
            trip=trip,
            start=data["start"],
            end=data["end"],
            distance_miles=data["distance_miles"],
            duration_hours=data["duration_hours"],
            requires_fuel_stop=data.get("requires_fuel_stop", False),
            requires_rest_break=data.get("requires_rest_break", False),
        )

    @staticmethod
    def update_segment(segment: RouteSegment, data: dict) -> RouteSegment:
        for field, value in data.items():
            setattr(segment, field, value)
        segment.save()
        return segment

    @staticmethod
    def delete_segment(segment: RouteSegment):
        segment.delete()
