from django.contrib.auth.models import User
from rest_framework import serializers
from core.models.user_profile import DriverProfile
from core.models.user_profile import DispatcherProfile


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    role = serializers.ChoiceField(choices=["driver", "dispatcher"])

    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "role")

    def create(self, validated_data):
        role = validated_data.pop("role")
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email"),
            password=validated_data["password"],
        )

        # Auto-create role profile
        if role == "driver":
            DriverProfile.objects.create(user=user)
        elif role == "dispatcher":
            DispatcherProfile.objects.create(user=user)

        return user
