from django.urls import path, include
from rest_framework import routers

from vote.views import VoteViewSet


router = routers.DefaultRouter()

router.register("", VoteViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "vote"
