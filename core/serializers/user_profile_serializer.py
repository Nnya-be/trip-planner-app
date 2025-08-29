from rest_framework import serializers
from core.models import DriverProfile, DispatcherProfile
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]


class DriverProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = DriverProfile
        fields = ["id", "user", "license_number", "cycle_limit_hours", "created_at"]
        read_only_fields = ["id", "created_at"]


class DispatcherProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = DispatcherProfile
        fields = ["id", "user", "company_name", "created_at"]
        read_only_fields = ["id", "created_at"]
