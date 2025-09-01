from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from core.serializers.auth_serializers import RegisterSerializer


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        from rest_framework_simplejwt.tokens import RefreshToken
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Prepare user data (same as in CustomTokenObtainPairSerializer)
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
            try:
                driver_profile = getattr(user, 'driver_profile', None)
                if driver_profile:
                    user_data['driverInfo'] = {
                        'license_number': driver_profile.license_number,
                        'cycle_limit_hours': driver_profile.cycle_limit_hours,
                    }
            except Exception:
                pass
            try:
                dispatcher_profile = getattr(user, 'dispatcher_profile', None)
                if dispatcher_profile:
                    user_data['vehicleInfo'] = {
                        'company_name': dispatcher_profile.company_name,
                    }
            except Exception:
                pass
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            tokens = {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }
            return Response({'user': user_data, 'tokens': tokens}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
