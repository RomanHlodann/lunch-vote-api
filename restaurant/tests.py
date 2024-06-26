from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls.base import reverse
from rest_framework.test import APIClient
from rest_framework import status

from restaurant.models import Restaurant, Menu


def get_restaurant_list_url():
    return reverse("restaurant:restaurant-list")


def sample_restaurant(number: int = 0):
    return {
        "name": f"restaurant{number}",
        "address": "some address",
        "phone_number": f"+38099999999{number}",
    }


def get_menu_list_url():
    return reverse("restaurant:menu-list")


class TestUnauthenticatedUserAccess(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_restaurant_access(self):
        result = self.client.get(get_restaurant_list_url())
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, result.status_code)

    def test_menu_access(self):
        result = self.client.get(get_menu_list_url())
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, result.status_code)


class TestRestaurant(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            "admin@myproject.com", "password"
        )
        self.client.force_authenticate(self.user)

    def test_unique_names(self):
        data = sample_restaurant()
        self.client.post(get_restaurant_list_url(), data=data)

        data["phone_number"] = "+393039030390"
        result = self.client.post(get_restaurant_list_url(), data=data)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, result.status_code)

    def test_unique_phone_numbers(self):
        data = sample_restaurant()
        self.client.post(get_restaurant_list_url(), data=data)

        data["name"] = "Other name"
        result = self.client.post(get_restaurant_list_url(), data=data)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, result.status_code)

    def test_restaurant_pagination(self):
        for i in range(12):
            Restaurant.objects.create(
                **sample_restaurant(i)
            )
        response = self.client.get(
            get_restaurant_list_url(), {"page": 1}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 10)

        response = self.client.get(
            get_restaurant_list_url(), {"page": 2}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)


class TestMenu(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            "admin@myproject.com", "password"
        )
        self.client.force_authenticate(self.user)

        self.restaurant1 = Restaurant.objects.create(**sample_restaurant(1))
        self.restaurant2 = Restaurant.objects.create(**sample_restaurant(2))

        self.menu1 = Menu.objects.create(
            description="Menu 1",
            date=datetime.today().date(),
            restaurant=self.restaurant1
        )
        self.menu2 = Menu.objects.create(
            description="Menu 2",
            date=datetime.today().date() - timedelta(days=1),
            restaurant=self.restaurant2
        )
        self.menu3 = Menu.objects.create(
            description="Menu 3",
            date=datetime.today().date(),
            restaurant=self.restaurant2
        )

        self.url = reverse("restaurant:menu-list")

    def test_filter_by_lunch_date(self):
        response = self.client.get(
            self.url,
            {"lunch_date": datetime.today().date().strftime("%Y-%m-%d")}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 2)

    def test_filter_all_parameter(self):
        response = self.client.get(
            self.url,
            {"all": "true"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 3)

    def test_filter_restaurants(self):
        response = self.client.get(
            self.url,
            {"restaurants": "1"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)

    def test_few_filters_simultaneously(self):
        response = self.client.get(
            self.url,
            {
                "all": "true",
                "restaurants": "2"
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 2)
