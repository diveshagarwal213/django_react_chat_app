from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from my_app.models import Interest
from my_app.permissions import HasInterestAccess
from my_app.serializers import EmptySerializer, InterestSerializer


# Create your views here.
class InterestViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    serializer_class = InterestSerializer

    def get_permissions(self):
        if self.action in ["retrieve", "destroy"]:
            return [IsAuthenticated(), HasInterestAccess(interest_id_kwarg="pk")]
        if self.action in ["accept_interest"]:
            return [
                IsAuthenticated(),
                HasInterestAccess(interest_id_kwarg="pk", sent_to=True),
            ]
        return [IsAuthenticated()]  # list, create

    def get_queryset(self):
        query_set = Interest.objects.filter(
            Q(sent_to=self.request.user) | Q(sent_by=self.request.user)
        )
        return query_set

    @action(detail=True, methods=["post"], serializer_class=EmptySerializer)
    def accept_interest(self, *args, **kwargs):
        interest = self.get_object()
        interest.is_accepted = True
        interest.save()
        return Response("Ok", status=status.HTTP_200_OK)
