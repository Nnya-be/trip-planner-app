from core.models import DailyLog, Trip, Logbook
from datetime import date


class LogService:
    @staticmethod
    def create_daily_log(trip: Trip, log_date: date) -> DailyLog:
        return DailyLog.objects.create(trip=trip, date=log_date)

    @staticmethod
    def get_daily_log(log_id: str) -> DailyLog:
        return DailyLog.objects.get(id=log_id)

    @staticmethod
    def delete_daily_log(log: DailyLog):
        log.delete()

    @staticmethod
    def get_or_create_logbook(trip: Trip) -> Logbook:
        logbook, _ = Logbook.objects.get_or_create(trip=trip)
        return logbook
