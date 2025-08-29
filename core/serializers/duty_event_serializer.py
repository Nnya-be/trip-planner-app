from rest_framework import serializers
from core.models import DutyEvent


class DutyEventSerializer(serializers.ModelSerializer):
    duration_hours = serializers.FloatField(read_only=True)

    class Meta:
        model = DutyEvent
        fields = [
            "id",
            "log",
            "status",
            "start_time",
            "end_time",
            "location",
            "duration_hours",
            "created_at",
        ]
        read_only_fields = ["id", "duration_hours", "created_at"]
