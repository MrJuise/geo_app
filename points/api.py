from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Point, Message
from .serializers import PointCreateSerializer, MessageCreateSerializer, PointSearchParamsSerializer, MessageReadSerializer
import math

class PointCreateAPIView(generics.CreateAPIView):
    queryset = Point.objects.all()
    serializer_class = PointCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class MessageCreateAPIView(generics.CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lam = math.radians(lon2 - lon1)

    a = math.sin(d_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lam / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

class PointSearchAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PointSearchParamsSerializer
    queryset = Point.objects.all()

    def get(self, request, *args, **kwargs):
        params = self.get_serializer(data=request.query_params)
        params.is_valid(raise_exception=True)

        lat = params.validated_data["latitude"]
        lon = params.validated_data["longitude"]
        radius_km = params.validated_data["radius"]

        lat_delta = radius_km / 111.0  # 1 градус широты ~ 111 км

        cos_lat = max(0.000001, abs(math.cos(math.radians(lat))))
        lon_delta = radius_km / (111.0 * cos_lat)

        qs = Point.objects.filter(
            latitude__gte=lat - lat_delta,
            latitude__lte=lat + lat_delta,
            longitude__gte=lon - lon_delta,
            longitude__lte=lon + lon_delta,
        )

        result = []
        for p in qs:
            if haversine_km(lat, lon, p.latitude, p.longitude) <= radius_km:
                result.append(p)

        data = PointCreateSerializer(result, many=True).data
        return Response(data)

class MessageSearchAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PointSearchParamsSerializer
    queryset = Message.objects.all()

    def get(self, request, *args, **kwargs):
        params = self.get_serializer(data=request.query_params)
        params.is_valid(raise_exception=True)

        lat = params.validated_data["latitude"]
        lon = params.validated_data["longitude"]
        radius_km = params.validated_data["radius"]


        lat_delta = radius_km / 111.0
        cos_lat = max(0.000001, abs(math.cos(math.radians(lat))))
        lon_delta = radius_km / (111.0 * cos_lat)

        candidate_points = Point.objects.filter(
            latitude__gte=lat - lat_delta,
            latitude__lte=lat + lat_delta,
            longitude__gte=lon - lon_delta,
            longitude__lte=lon + lon_delta,
        )


        point_ids_in_radius = []
        for p in candidate_points:
            if haversine_km(lat, lon, p.latitude, p.longitude) <= radius_km:
                point_ids_in_radius.append(p.id)


        if not point_ids_in_radius:
            return Response([])


        qs = (
            Message.objects
            .filter(point_id__in=point_ids_in_radius)
            .select_related("author", "point")
            .order_by("-created_at")
        )

        data = MessageReadSerializer(qs, many=True).data
        return Response(data)
