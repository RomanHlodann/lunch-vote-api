from rest_framework import serializers

from vote.models import Vote
from restaurant.serializers import MenuListSerializer


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ("id", "menu", "created_at",)


class VoteListSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source="user.email")
    menu_description = serializers.CharField(source="menu.description")
    restaurant_name = serializers.CharField(source="menu.restaurant.name")

    class Meta:
        model = Vote
        fields = ("id", "menu_description", "restaurant_name", "created_at", "email",)


class VoteDetailSerializer(VoteListSerializer):
    menu = MenuListSerializer()

    class Meta:
        model = Vote
        fields = ("id", "menu", "created_at", "email",)
