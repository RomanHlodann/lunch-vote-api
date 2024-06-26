from datetime import datetime
from django.db.models import Count, F
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from vote.models import Vote
from vote.serializers import VoteSerializer, VoteDetailSerializer, VoteListSerializer


class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer

    @action(detail=False, methods=["get"], url_path="results")
    def get_results(self, request):
        queryset = self.get_queryset()

        votes_count = (queryset.select_related("menu", "menu__restaurant")
                       .values(menu_identifier=F("menu__id"),
                               description=F("menu__description"),
                               restaurant_name=F("menu__restaurant__name"),
                               date=F("menu__date"))
                       .annotate(vote_count=Count("id")).order_by("-vote_count"))

        return Response(votes_count, status=status.HTTP_200_OK)

    def get_queryset(self):
        queryset = self.queryset
        today = datetime.today()

        query_param_date = self.request.query_params.get("date")
        if query_param_date:
            today = datetime.strptime(query_param_date, "%Y-%m-%d").date()

        if self.action in ("list", "retrieve"):
            queryset = queryset.select_related("menu", "menu__restaurant")

        return queryset.filter(created_at=today)

    def get_serializer_class(self):
        if self.action == "list":
            return VoteListSerializer
        elif self.action == "retrieve":
            return VoteDetailSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
