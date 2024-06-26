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

    def get_serializer_class(self):
        if self.action == "list":
            return MenuListSerializer
        elif self.action == "retrieve":
            return MenuDetailSerializer
        return self.serializer_class
