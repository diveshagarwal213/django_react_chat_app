from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from my_app.models import ChatMessage, Interest
from my_app.permissions import HasChatMessageAccess, HasInterestAccess
from my_app.serializers import (
    ChatMessageSerializer,
    EmptySerializer,
    InterestSerializer,
    MyInterestSerializer,
)


# Create your views here.
class InterestViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):

    filter_backends = [OrderingFilter, DjangoFilterBackend, SearchFilter]
    filterset_fields = ["is_accepted"]
    search_fields = ["sent_by__first_name", "sent_to__first_name"]
    ordering_fields = ["created_at", "id"]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return MyInterestSerializer
        return InterestSerializer

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
        ).prefetch_related("sent_to", "sent_by")
        return query_set

    @action(detail=True, methods=["post"], serializer_class=EmptySerializer)
    def accept_interest(self, *args, **kwargs):
        interest = self.get_object()
        interest.is_accepted = True
        interest.save()
        return Response("Ok", status=status.HTTP_200_OK)


class ChatMessageViewSet(
    ListModelMixin, RetrieveModelMixin, CreateModelMixin, GenericViewSet
):
    serializer_class = ChatMessageSerializer

    def get_permissions(self):
        if self.action in ["retrieve"]:
            return [IsAuthenticated(), HasChatMessageAccess(chat_message_id_kwarg="pk")]
        return [IsAuthenticated(), HasInterestAccess()]  # list, create

    def get_queryset(self):
        interest_id = self.kwargs.get("interest_pk")
        return ChatMessage.objects.filter(interest_id=interest_id)

    def get_serializer_context(self):
        default_context = super().get_serializer_context()
        default_context["interest_id"] = self.kwargs.get("interest_pk")
        return default_context
