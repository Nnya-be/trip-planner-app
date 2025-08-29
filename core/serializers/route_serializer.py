from rest_framework import serializers
from core.models import RouteSegment


class RouteSegmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteSegment
        fields = [
            "id",
            "trip",
            "start",
            "end",
            "distance_miles",
            "duration_hours",
            "requires_fuel_stop",
            "requires_rest_break",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]
