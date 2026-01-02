from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Point, Message

User = get_user_model()


class PointCreateTests(APITestCase):
    def test_create_point(self):
        user = User.objects.create_user(
            username="testuser",
            password="password123"
        )

        self.client.force_authenticate(user=user)

        payload = {
            "latitude": 52.36,
            "longitude": 4.90,
        }

        response = self.client.post(
            "/api/points/",
            data=payload,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Point.objects.count(), 1)

        point = Point.objects.first()

        self.assertEqual(point.latitude, payload["latitude"])
        self.assertEqual(point.longitude, payload["longitude"])
        self.assertEqual(point.owner, user)


class PointSearchTests(APITestCase):
    def test_search_points_in_radius(self):
        user = User.objects.create_user(
            username="testuser2",
            password="password123"
        )
        self.client.force_authenticate(user=user)

        center_lat = 55.55
        center_lon = 5.00
        radius_km = 5.0

        near_point = Point.objects.create(
            owner=user,
            latitude=center_lat,
            longitude=center_lon,
        )

        far_point = Point.objects.create(
            owner=user,
            latitude=77.77,
            longitude=7.77,
        )

        url = f"/api/points/search/?latitude={center_lat}&longitude={center_lon}&radius={radius_km}"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        returned_ids = {item["id"] for item in response.data}

        self.assertIn(near_point.id, returned_ids)
        self.assertNotIn(far_point.id, returned_ids)


class MessageSearchTests(APITestCase):
    def test_search_messages_in_radius(self):
        user = User.objects.create_user(
            username="testuser3",
            password="password123"
        )
        self.client.force_authenticate(user=user)

        center_lat = 55.55
        center_lon = 5.55
        radius_km = 5.0

        near_point = Point.objects.create(
            owner=user,
            latitude=center_lat,
            longitude=center_lon,
        )

        far_point = Point.objects.create(
            owner=user,
            latitude=77.77,
            longitude=7.77,
        )

        near_message = Message.objects.create(
            point=near_point,
            author=user,
            content="Near message",
        )

        far_message = Message.objects.create(
            point=far_point,
            author=user,
            content="Far message",
        )

        url = f"/api/messages/search/?latitude={center_lat}&longitude={center_lon}&radius={radius_km}"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        returned_ids = {item["id"] for item in response.data}

        self.assertIn(near_message.id, returned_ids)
        self.assertNotIn(far_message.id, returned_ids)
