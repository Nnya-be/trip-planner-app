from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core.models import DriverProfile, DispatcherProfile
from core.serializers import DriverProfileSerializer, DispatcherProfileSerializer
from core.services.user_profile_service import UserProfileService


class DriverProfileViewSet(viewsets.ViewSet):
    from rest_framework.decorators import action

    @action(detail=False, methods=['get'], url_path='by-user/(?P<user_id>\\d+)')
    def by_user(self, request, user_id=None):
        try:
            profile = DriverProfile.objects.get(user__id=user_id)
        except DriverProfile.DoesNotExist:
            return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = DriverProfileSerializer(profile)
        return Response(serializer.data)
    permission_classes = [IsAuthenticated]


    def list(self, request):
        # Only return the requesting user's driver profile
        try:
            profile = DriverProfile.objects.get(user=request.user)
        except DriverProfile.DoesNotExist:
            return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = DriverProfileSerializer(profile)
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        # Only allow retrieving own profile
        try:
            profile = DriverProfile.objects.get(user=request.user, id=pk)
        except DriverProfile.DoesNotExist:
            return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = DriverProfileSerializer(profile)
        return Response(serializer.data)

    def create(self, request):
        serializer = DriverProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        profile = UserProfileService.create_driver_profile(request.user, serializer.validated_data)
        return Response(DriverProfileSerializer(profile).data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        profile = DriverProfile.objects.get(id=pk)
        serializer = DriverProfileSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        profile = UserProfileService.update_driver_profile(profile, serializer.validated_data)
        return Response(DriverProfileSerializer(profile).data)


class DispatcherProfileViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        profiles = DispatcherProfile.objects.all()
        serializer = DispatcherProfileSerializer(profiles, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        profile = DispatcherProfile.objects.get(id=pk)
        serializer = DispatcherProfileSerializer(profile)
        return Response(serializer.data)

    def create(self, request):
        serializer = DispatcherProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        profile = UserProfileService.create_dispatcher_profile(request.user, serializer.validated_data)
        return Response(DispatcherProfileSerializer(profile).data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        profile = DispatcherProfile.objects.get(id=pk)
        serializer = DispatcherProfileSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        profile = UserProfileService.update_dispatcher_profile(profile, serializer.validated_data)
        return Response(DispatcherProfileSerializer(profile).data)
