from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core.views.trip_views import TripViewSet
from core.views.route_views import RouteSegmentViewSet
from core.views.log_views import DailyLogViewSet, LogbookViewSet
from core.views.duty_event_views import DutyEventViewSet
from core.views.user_profile_views import DriverProfileViewSet, DispatcherProfileViewSet


# Create a DRF router instance
router = DefaultRouter()

# Register your viewsets
router.register(r"trips", TripViewSet, basename="trip")
router.register(r"routes", RouteSegmentViewSet, basename="route")
router.register(r"logs", DailyLogViewSet, basename="dailylog")
router.register(r"logbooks", LogbookViewSet, basename="logbook")
router.register(r"events", DutyEventViewSet, basename="dutyevent")
router.register(r"drivers", DriverProfileViewSet, basename="driverprofile")
router.register(r"dispatchers", DispatcherProfileViewSet, basename="dispatcherprofile")


urlpatterns = [
    path("logs/compliant_log/", DailyLogViewSet.as_view({"get": "compliant_log"}), name="compliant-log"),
    path("", include(router.urls)),
]