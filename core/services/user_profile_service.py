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
        for field, value in data.items():
            setattr(profile, field, value)
        profile.save()
        return profile

    @staticmethod
    def update_dispatcher_profile(profile: DispatcherProfile, data: dict) -> DispatcherProfile:
        for field, value in data.items():
            setattr(profile, field, value)
        profile.save()
        return profile
