from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core.models import DailyLog, Logbook
from core.serializers import DailyLogSerializer, LogbookSerializer
from core.services.log_service import LogService


class DailyLogViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        logs = DailyLog.objects.all()
        serializer = DailyLogSerializer(logs, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        log = LogService.get_daily_log(pk)
        serializer = DailyLogSerializer(log)
        return Response(serializer.data)

    def create(self, request):
        serializer = DailyLogSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        log = LogService.create_daily_log(
            serializer.validated_data["trip"],
            serializer.validated_data["date"]
        )
        return Response(DailyLogSerializer(log).data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        log = LogService.get_daily_log(pk)
        LogService.delete_daily_log(log)
        return Response(status=status.HTTP_204_NO_CONTENT)


class LogbookViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, pk=None):
        logbook = LogService.get_or_create_logbook(pk)
        serializer = LogbookSerializer(logbook)
        return Response(serializer.data)
