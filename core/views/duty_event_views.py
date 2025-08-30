from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core.models import DutyEvent, DailyLog
from core.serializers import DutyEventSerializer
from core.services.duty_event_service import DutyEventService


class DutyEventViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        events = DutyEvent.objects.all()
        serializer = DutyEventSerializer(events, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        event = DutyEvent.objects.get(id=pk)
        serializer = DutyEventSerializer(event)
        return Response(serializer.data)

    def create(self, request):
        serializer = DutyEventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        log = serializer.validated_data["log"]
        event = DutyEventService.add_event(log, serializer.validated_data)
        return Response(DutyEventSerializer(event).data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        event = DutyEvent.objects.get(id=pk)
        serializer = DutyEventSerializer(event, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        event = DutyEventService.update_event(event, serializer.validated_data)
        return Response(DutyEventSerializer(event).data)

    def destroy(self, request, pk=None):
        event = DutyEvent.objects.get(id=pk)
        DutyEventService.delete_event(event)
        return Response(status=status.HTTP_204_NO_CONTENT)
