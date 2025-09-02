from core.models import DriverProfile, DispatcherProfile
from django.contrib.auth.models import User


class UserProfileService:
    @staticmethod
    def create_driver_profile(user: User, data: dict) -> DriverProfile:
        return DriverProfile.objects.create(
            user=user,
            license_number=data["license_number"],
            cycle_limit_hours=data.get("cycle_limit_hours", 70),
        )

    @staticmethod
    def create_dispatcher_profile(user: User, data: dict) -> DispatcherProfile:
        return DispatcherProfile.objects.create(
            user=user,
            company_name=data.get("company_name"),
        )

    @staticmethod
    def update_driver_profile(profile: DriverProfile, data: dict) -> DriverProfile:
        vehicle_info_data = data.pop('vehicle_info', None)
        # Update driver profile fields
        for field, value in data.items():
            setattr(profile, field, value)
        profile.save()
        # Update or create vehicle info
        if vehicle_info_data is not None:
            from core.models.user_profile import VehicleInfo
            vehicle_info, _ = VehicleInfo.objects.get_or_create(driver_profile=profile)
            for attr, value in vehicle_info_data.items():
                setattr(vehicle_info, attr, value)
            vehicle_info.save()
        return profile

