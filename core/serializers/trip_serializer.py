from rest_framework import serializers
from core.models import Trip
from .route_serializer import RouteSegmentSerializer


class TripSerializer(serializers.ModelSerializer):
    segments = RouteSegmentSerializer(many=True, read_only=True)

    class Meta:
        model = Trip
        fields = [
            "id",
            "driver",
            "current_location",
            "pickup_location",
            "dropoff_location",
            "cycle_hours_used",
            "created_at",
            "segments",
        ]
        read_only_fields = ["id", "created_at"]
