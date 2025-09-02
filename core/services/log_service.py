from core.models import DailyLog, Trip, Logbook
from datetime import date


class LogService:
    @staticmethod
    def plan_trip_logs(trip, route_data, start_date=None, cycle_hours_used=0):
        """
        Split trip into daily logs and generate compliant duty events for each day, including stops and rests.
        - trip: Trip object
        - route_data: dict with 'distance_km', 'duration_hr', 'legs', etc.
        - start_date: date to start logs (default today)
        - cycle_hours_used: hours already used in 70/8 cycle
        """
        from core.models.log import DailyLog
        from core.models.duty_event import DutyEvent
        from datetime import date, timedelta, datetime
        from core.services.route_service import RouteSegmentService
        if not start_date:
            start_date = date.today()
        # FMCSA rules
        MAX_DRIVE_HRS_PER_DAY = 11
        MAX_ON_DUTY_HRS_PER_DAY = 14
        MAX_CYCLE_HRS = 70
        REST_BREAK_HRS = 10
        # Get total trip duration and distance
        total_drive_hours = route_data["duration_hr"]
        total_distance_km = route_data["distance_km"]
        # Calculate number of days needed
        remaining_cycle = MAX_CYCLE_HRS - cycle_hours_used
        max_days = min(int((total_drive_hours // MAX_DRIVE_HRS_PER_DAY) + 1), int(remaining_cycle // MAX_DRIVE_HRS_PER_DAY) + 1)
        # Calculate fuel stops and rest stops
        fuel_stops = RouteSegmentService.calculate_fuel_stops(route_data, tank_range_km=1609)  # 1000 miles in km
        rest_stops = RouteSegmentService.calculate_rest_stops(total_drive_hours, max_drive_hr=MAX_DRIVE_HRS_PER_DAY)
        # Split trip into daily logs
        drive_hours_left = total_drive_hours
        distance_left = total_distance_km
        current_cycle = cycle_hours_used
        logs = []
        for day in range(max_days):
            log_date = start_date + timedelta(days=day)
            daily_log = DailyLog.objects.create(trip=trip, date=log_date)
            logs.append(daily_log)
            # Calculate hours for this day
            drive_today = min(MAX_DRIVE_HRS_PER_DAY, drive_hours_left, remaining_cycle)
            on_duty_today = min(MAX_ON_DUTY_HRS_PER_DAY, drive_today + 2)  # 1hr pickup, 1hr dropoff
            # Duty events: Off Duty (rest), On Duty (pickup), Driving, Fuel/Rest stops, On Duty (dropoff), Off Duty (end)
            events = []
            # 1. Off Duty (rest before shift)
            events.append({
                "status": "OFF",
                "start": "00:00",
                "end": "06:00",
                "location": trip.current_location if day == 0 else "Rest stop"
            })
            # 2. On Duty (pickup)
            events.append({
                "status": "ON_DUTY",
                "start": "06:00",
                "end": "07:00",
                "location": trip.pickup_location
            })
            # 3. Driving (with fuel/rest stops)
            drive_start = datetime.combine(log_date, datetime.strptime("07:00", "%H:%M").time())
            drive_end = drive_start + timedelta(hours=drive_today)
            # Insert fuel stops and rest breaks
            current_time = drive_start
            hours_driven = 0
            for stop in fuel_stops:
                if hours_driven + 2 > drive_today:
                    break
                stop_time = current_time + timedelta(hours=2)
                events.append({
                    "status": "ON_DUTY",
                    "start": current_time.strftime("%H:%M"),
                    "end": stop_time.strftime("%H:%M"),
                    "location": stop["location"]["name"]
                })
                current_time = stop_time
                hours_driven += 2
            # Driving remainder
            if hours_driven < drive_today:
                drive_remain_end = current_time + timedelta(hours=drive_today - hours_driven)
                events.append({
                    "status": "DRIVING",
                    "start": current_time.strftime("%H:%M"),
                    "end": drive_remain_end.strftime("%H:%M"),
                    "location": "En route"
                })
                current_time = drive_remain_end
            # 4. On Duty (dropoff)
            events.append({
                "status": "ON_DUTY",
                "start": current_time.strftime("%H:%M"),
                "end": (current_time + timedelta(hours=1)).strftime("%H:%M"),
                "location": trip.dropoff_location
            })
            current_time += timedelta(hours=1)
            # 5. Off Duty (rest after shift)
            events.append({
                "status": "OFF",
                "start": current_time.strftime("%H:%M"),
                "end": "23:59",
                "location": "Rest stop"
            })
            # Save events
            for event in events:
                start_dt = datetime.combine(log_date, datetime.strptime(event["start"], "%H:%M").time())
                end_dt = datetime.combine(log_date, datetime.strptime(event["end"], "%H:%M").time()) if event["end"] != "23:59" else datetime.combine(log_date, datetime.strptime("23:59", "%H:%M").time())
                if end_dt <= start_dt:
                    end_dt += timedelta(days=1)
                DutyEvent.objects.create(
                    log=daily_log,
                    status=event["status"],
                    start_time=start_dt,
                    end_time=end_dt,
                    location=event["location"]
                )
            drive_hours_left -= drive_today
            distance_left -= (total_distance_km / max_days)
            current_cycle += drive_today
            remaining_cycle = MAX_CYCLE_HRS - current_cycle
        return logs
    @staticmethod
    def generate_compliant_log(trip, log_date):
        # Get the daily log for this trip and date
        from core.models.log import DailyLog
        from core.models.duty_event import DutyEvent
        try:
            daily_log = DailyLog.objects.get(trip=trip, date=log_date)
        except DailyLog.DoesNotExist:
            return None

        # Get all duty events for this log
        events = DutyEvent.objects.filter(log=daily_log).order_by('start_time')
        duty_statuses = []
        from collections import defaultdict
        total_hours = defaultdict(float)
        for event in events:
            duty_statuses.append({
                "start_time": event.start_time.strftime("%H:%M"),
                "end_time": event.end_time.strftime("%H:%M"),
                "status": event.get_status_display(),
                "location": event.location,
                "remarks": getattr(event, 'remarks', None)
            })
            total_hours[event.get_status_display()] += event.duration_hours

        # Example: get trip/driver/vehicle info (customize as needed)
        log = {
            "date": log_date.isoformat(),
            "total_miles_driving_today": getattr(trip, 'miles_driven', 0),
            "truck_number": getattr(trip, 'truck_number', ""),
            "trailer_number": getattr(trip, 'trailer_number', ""),
            "driver_name": getattr(trip.driver, 'get_full_name', lambda: trip.driver.username)(),
            "carrier_name": getattr(trip.driver, 'carrier_name', ""),
            "main_office_address": getattr(trip.driver, 'main_office_address', ""),
            "co_driver_name": getattr(trip.driver, 'co_driver_name', ""),
            "duty_statuses": duty_statuses,
            "total_hours": dict(total_hours),
            "shipping_document": getattr(trip, 'shipping_document', ""),
            "signature": getattr(trip.driver, 'get_full_name', lambda: trip.driver.username)(),
        }
        return log
    @staticmethod
    def generate_logs(start_date=None, days=3):
        from datetime import date, timedelta
        if not start_date:
            start_date = date.today()

        logs = []
        for i in range(days):
            day_date = start_date + timedelta(days=i)
            logs.append({
                "date": day_date.isoformat(),
                "driveTime": 8.5 if i == 0 else (9.2 if i == 1 else 0),
                "onDutyTime": 12 if i < 2 else 0,
                "offDutyTime": 10 if i < 2 else 0,
                "sleeper": 2 if i == 0 else 0,
                "status": "Complete" if i == 0 else ("Current" if i == 1 else "Planned"),
                "violations": 0,
            })
        return logs
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
