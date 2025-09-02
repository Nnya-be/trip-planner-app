from rest_framework import serializers
from core.models import DriverProfile, DispatcherProfile
from core.models.user_profile import VehicleInfo
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]




class VehicleInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleInfo
        fields = [
            "truck_number",
            "trailer_number",
            "eld_device_id",
            "vin_number",
            "plate_number",
        ]

class DriverProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    vehicle_info = VehicleInfoSerializer(required=False)

    class Meta:
        model = DriverProfile
        fields = [
            "id", "user", "name", "co_driver_name", "carrier_name", "license_number", "phone_number", "cycle_limit_hours", "vehicle_info", "created_at"
        ]
        read_only_fields = ["id", "created_at"]

    def update(self, instance, validated_data):
        vehicle_info_data = validated_data.pop('vehicle_info', None)
        # Update driver profile fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        # Update or create vehicle info
        if vehicle_info_data is not None:
            vehicle_info_model = self.fields['vehicle_info'].Meta.model
            vehicle_info, _ = vehicle_info_model.objects.get_or_create(driver_profile=instance)
            for attr, value in vehicle_info_data.items():
                setattr(vehicle_info, attr, value)
            vehicle_info.save()
        return instance


class DispatcherProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = DispatcherProfile
        fields = ["id", "user", "company_name", "created_at"]
        read_only_fields = ["id", "created_at"]
