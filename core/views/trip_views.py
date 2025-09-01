from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core.models import Trip
from core.serializers import TripSerializer
from core.services.trip_service import TripService


class TripViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        trips = Trip.objects.filter(driver=request.user)
        serializer = TripSerializer(trips, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        trip = TripService.get_trip(pk)
        serializer = TripSerializer(trip)
        return Response(serializer.data)

    def create(self, request):
        from core.utils.geocode import geocode_location
        serializer = TripSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        trip = TripService.create_trip(request.user, serializer.validated_data)
        # Geocode locations
        current_coords = geocode_location(trip.current_location)
        pickup_coords = geocode_location(trip.pickup_location)
        dropoff_coords = geocode_location(trip.dropoff_location)
        trip_data = {
            'currentLocation': trip.current_location,
            'pickupLocation': trip.pickup_location,
            'dropoffLocation': trip.dropoff_location,
            'currentCycleHours': trip.cycle_hours_used,
            'coordinates': {
                'current': list(current_coords),
                'pickup': list(pickup_coords),
                'dropoff': list(dropoff_coords),
            },
            'routeData': None,  # Add route data if available
        }
        return Response(trip_data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        trip = TripService.get_trip(pk)
        serializer = TripSerializer(trip, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        trip = TripService.update_trip(trip, serializer.validated_data)
        return Response(TripSerializer(trip).data)

    def destroy(self, request, pk=None):
        trip = TripService.get_trip(pk)
        TripService.delete_trip(trip)
        return Response(status=status.HTTP_204_NO_CONTENT)
