from core.models import RouteSegment, Trip
import requests
from math import floor


OSRM_URL = "http://router.project-osrm.org/route/v1/driving"


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
    
    @staticmethod
    def get_route_data(start_coords, end_coords, waypoints=None):
        """
        start_coords / end_coords = (lat, lon)
        OSRM expects lon,lat
        """
        # Flip order to lon,lat
        start = f"{start_coords[0]},{start_coords[1]}"
        end = f"{end_coords[0]},{end_coords[1]}"

        coords = f"{start};{end}"

        if waypoints:
            waypoint_str = ";".join([f"{lon},{lat}" for lat, lon in waypoints])
            coords = f"{start};{waypoint_str};{end}"

        url = f"{OSRM_URL}/{coords}?overview=full&geometries=geojson&steps=true"
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()

        route = data["routes"][0]
        return {
            "distance_km": round(route["distance"] / 1000, 2),
            "duration_hr": round(route["duration"] / 3600, 2),
            "geometry": route["geometry"],
            "legs": route["legs"],
        }
    
    @staticmethod
    def calculate_fuel_stops(route_data, tank_range_km=600):
        """
        Estimate fuel stops based on tank range and return real map locations.
        """
        distance_km = route_data["distance_km"]
        coords = route_data["geometry"]["coordinates"]  # [lon, lat] pairs

        num_stops = floor(distance_km / tank_range_km)
        if num_stops == 0:
            return []

        stops = []
        km_per_segment = distance_km / len(coords)

        # iterate route geometry to find stop positions
        km_traveled = 0
        next_stop_at = tank_range_km

        from core.utils.reverse_geocode import reverse_geocode
        for idx, coord in enumerate(coords):
            km_traveled += km_per_segment
            if km_traveled >= next_stop_at:
                lat, lon = coord[1], coord[0]  # convert lon,lat → lat,lon
                name = reverse_geocode(lat, lon)
                stops.append({
                    "stop_number": len(stops) + 1,
                    "km_before_stop": round(next_stop_at, 2),
                    "location": {
                        "name": name,
                        "coords": [lat, lon]
                    }
                })
                next_stop_at += tank_range_km

        return stops
    
    @staticmethod
    def calculate_rest_stops(duration_hr, max_drive_hr=8):
        """
        Insert mandatory rests every `max_drive_hr` hours.
        """
        rests = []
        total_rests = int(duration_hr // max_drive_hr)
        for i in range(1, total_rests + 1):
            rests.append({
                "stop_number": i,
                "after_hours": i * max_drive_hr,
                "location": f"Rest stop after {i * max_drive_hr} hrs"
            })
        return rests
