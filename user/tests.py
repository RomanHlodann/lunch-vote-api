from django.test import TestCase
from django.urls.base import reverse
from rest_framework.test import APIClient
from rest_framework import status


class TestUserUnauthenticated(TestCase):
    def test_user_creation(self):
        client = APIClient()
        result = client.post(
            reverse("user:create"),
            data={
                "email": "admin@admin.com",
                "password": "12345"
            }
        )
        self.assertEqual(result.status_code, status.HTTP_401_UNAUTHORIZED)
