from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls.base import reverse
from rest_framework.test import APIClient
from rest_framework import status

from restaurant.tests import sample_restaurant
from restaurant.models import Restaurant, Menu


def sample_vote(user_id: int, menu_id: int):
    return {
        "user": user_id,
        "menu": menu_id
    }


def vote_list_url():
    return reverse("vote:vote-list")


class TestVote(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            "admin@myproject.com", "password"
        )
        self.client.force_authenticate(self.user)
        self.restaurant = Restaurant.objects.create(**sample_restaurant())
        self.menu = Menu.objects.create(
            description="Test",
            date=datetime.today().date(),
            restaurant=self.restaurant
        )

    def test_create_few_votes_at_same_date(self):
        self.client.post(
            vote_list_url(),
            data=sample_vote(self.user.id, self.menu.id)
        )
        menu1 = Menu.objects.create(
            description="Test2",
            date=datetime.today().date(),
            restaurant=self.restaurant
        )

        self.client.post(
            vote_list_url(),
            sample_vote(self.user.id, menu1.id)
        )
        response = self.client.get(vote_list_url())
        self.assertEqual(
            status.HTTP_200_OK, response.status_code
        )
        self.assertEqual(response.data["count"], 2)
