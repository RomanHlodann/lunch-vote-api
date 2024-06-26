from rest_framework import serializers

from restaurant.models import Restaurant, Menu


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ("id", "name", "address", "phone_number",)


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ("id", "image", "description", "date", "restaurant")


class MenuListSerializer(serializers.ModelSerializer):
    restaurant_name = serializers.CharField(
        source="restaurant.name"
    )

    class Meta:
        model = Menu
        fields = ("id", "image", "description", "date", "restaurant_name")


class MenuDetailSerializer(MenuSerializer):
    restaurant = RestaurantSerializer()


class MenuListInRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ("id", "image", "description", "date")


class RestaurantDetailSerializer(serializers.ModelSerializer):
    menus = MenuListInRestaurantSerializer(many=True)

    class Meta:
        model = Restaurant
        fields = ("id", "name", "address", "phone_number", "menus",)
