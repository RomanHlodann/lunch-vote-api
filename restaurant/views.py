from datetime import datetime

from django.db.models import Prefetch
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from restaurant.models import Restaurant, Menu
from restaurant.serializers import (
    RestaurantSerializer,
    RestaurantDetailSerializer,
    MenuSerializer,
    MenuListSerializer,
    MenuDetailSerializer
)


class DefaultPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = DefaultPagination


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.select_related("restaurant")
    serializer_class = MenuSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = DefaultPagination

    @staticmethod
    def _params_to_ints(qs):
        """Converts a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        queryset = self.queryset
        lunch_date = self.request.query_params.get("lunch_date")
        all_dates = self.request.query_params.get("all")
        restaurants = self.request.query_params.get("restaurants")

        today = datetime.today()
        if not all_dates or not all_dates.lower() in ("yes", "true", "t", "1"):
            if lunch_date:
                today = datetime.strptime(lunch_date, "%Y-%m-%d").date()

            queryset = queryset.filter(date=today)

        if restaurants:
            restaurant_ids = self._params_to_ints(restaurants)
            queryset = queryset.filter(restaurant_id__in=restaurant_ids)

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return MenuListSerializer
        elif self.action == "retrieve":
            return MenuDetailSerializer
        return self.serializer_class
