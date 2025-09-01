from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User
from core.models.user_profile import DriverProfile, DispatcherProfile

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        # User info
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': getattr(user, 'role', None),
            'firstName': getattr(user, 'first_name', None),
            'lastName': getattr(user, 'last_name', None),
            'driverInfo': None,
            'vehicleInfo': None,
        }
        # Attach driverInfo or vehicleInfo if available
        try:
            user_data['driverInfo'] = {
                # Add driver profile fields here
            }
        except Exception:
            pass
        try:
            user_data['vehicleInfo'] = {
                # Add dispatcher profile fields here
            }
        except Exception:
            pass
        return {
            'user': user_data,
            'tokens': {
                'access': data['access'],
                'refresh': data['refresh']
            }
        }

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
