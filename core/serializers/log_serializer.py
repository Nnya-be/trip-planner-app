from rest_framework import serializers
from core.models import DailyLog, Logbook
from .duty_event_serializer import DutyEventSerializer


class DailyLogSerializer(serializers.ModelSerializer):
    events = DutyEventSerializer(many=True, read_only=True)

    class Meta:
        model = DailyLog
        fields = ["id", "trip", "date", "created_at", "events"]
        read_only_fields = ["id", "created_at"]


class LogbookSerializer(serializers.ModelSerializer):
    logs = DailyLogSerializer(source="trip.logs", many=True, read_only=True)

    class Meta:
        model = Logbook
        fields = ["id", "trip", "created_at", "logs"]
        read_only_fields = ["id", "created_at"]
