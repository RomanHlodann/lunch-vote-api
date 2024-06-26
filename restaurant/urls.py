from django.urls import path, include
from rest_framework import routers

from restaurant.views import RestaurantViewSet, MenuViewSet


router = routers.DefaultRouter()

router.register("all", RestaurantViewSet)
router.register("menus", MenuViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "restaurant"
