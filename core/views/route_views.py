from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core.models import RouteSegment
from core.serializers import RouteSegmentSerializer
from core.services.route_service import RouteSegmentService


class RouteSegmentViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        segments = RouteSegment.objects.all()
        serializer = RouteSegmentSerializer(segments, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        segment = RouteSegment.objects.get(id=pk)
        serializer = RouteSegmentSerializer(segment)
        return Response(serializer.data)

    def create(self, request):
        serializer = RouteSegmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        segment = RouteSegmentService.add_segment(
            serializer.validated_data["trip"],
            serializer.validated_data
        )
        return Response(RouteSegmentSerializer(segment).data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        segment = RouteSegment.objects.get(id=pk)
        serializer = RouteSegmentSerializer(segment, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        segment = RouteSegmentService.update_segment(segment, serializer.validated_data)
        return Response(RouteSegmentSerializer(segment).data)

    def destroy(self, request, pk=None):
        segment = RouteSegment.objects.get(id=pk)
        RouteSegmentService.delete_segment(segment)
        return Response(status=status.HTTP_204_NO_CONTENT)
