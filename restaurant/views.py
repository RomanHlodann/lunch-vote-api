import datetime

from django.db.models import Prefetch
from rest_framework import viewsets

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

    def get_queryset(self):
        queryset = Restaurant.objects.all()
        if self.action == "retrieve":
            today = datetime.date.today()
            queryset = (queryset.prefetch_related(
                Prefetch("menus", queryset=Menu.objects.filter(date=today))
            ))
        return queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return RestaurantDetailSerializer
        return RestaurantSerializer


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.select_related("restaurant")
    serializer_class = MenuSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return MenuListSerializer
        elif self.action == "retrieve":
            return MenuDetailSerializer
        return self.serializer_class
