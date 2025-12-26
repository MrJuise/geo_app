from rest_framework import serializers
from .models import Point, Message

class PointCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        fields = ('id', 'latitude', 'longitude', 'created_at')
        read_only_fields = ('id', 'created_at')

    def validate_latitude(self, value):
        if not (-90 <= value <= 90):
            raise serializers.ValidationError(
                "latitude must be between -90 and 90"
            )
        return value

    def validate_longitude(self, value):
        if not (-180 <= value <= 180):
            raise serializers.ValidationError(
                "longitude must be between -180 and 180"
            )
        return value

class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'point', 'content', 'created_at')
        read_only_fields = ('id', 'created_at')

    def validate_point(self, value: Point):
        if value is None:
            raise serializers.ValidationError("Point is required")
        return value

class PointSearchParamsSerializer(serializers.Serializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    radius = serializers.FloatField()

    def validate_latitude(self, value):
        if not (-90 <= value <= 90):
            raise serializers.ValidationError("latitude must be between -90 and 90")
        return value

    def validate_longitude(self, value):
        if not (-180 <= value <= 180):
            raise serializers.ValidationError("longitude must be between -180 and 180")
        return value

    def validate_radius(self, value):
        if value <= 0:
            raise serializers.ValidationError("radius must be > 0")
        return value

class MessageReadSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Message
        fields = ('id', 'point', 'content', 'created_at', 'author_username')



