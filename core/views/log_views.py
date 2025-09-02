from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core.models import DailyLog, Logbook
from core.serializers import DailyLogSerializer, LogbookSerializer
from core.services.log_service import LogService


class DailyLogViewSet(viewsets.ViewSet):
    def compliant_log(self, request):
        """
        Returns FMCSA-compliant log for a given trip and date.
        Expects query params: trip_id, date (YYYY-MM-DD)
        """
        trip_id = request.query_params.get('trip_id')
        log_date = request.query_params.get('date')
        if not trip_id or not log_date:
            return Response({"error": "trip_id and date are required."}, status=status.HTTP_400_BAD_REQUEST)
        from core.models import Trip
        from datetime import datetime
        try:
            trip = Trip.objects.get(id=trip_id)
            log_date_obj = datetime.strptime(log_date, "%Y-%m-%d").date()
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        log_data = LogService.generate_compliant_log(trip, log_date_obj)
        if not log_data:
            return Response({"error": "No log found for this trip and date."}, status=status.HTTP_404_NOT_FOUND)
        return Response(log_data)
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
