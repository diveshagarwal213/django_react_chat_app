# from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Prefetch
from djoser.views import UserViewSet
from rest_framework.response import Response

from core.serializers import UserListSerializer
from my_app.models import Interest

User = get_user_model()


class CustomUserViewSet(UserViewSet):

    def list(self, request, *args, **kwargs):
        # get already requested or current friends ids
        queryset = (
            User.objects.prefetch_related(
                Prefetch(
                    "sent_to",
                    queryset=Interest.objects.filter(sent_by=self.request.user),
                ),
                Prefetch(
                    "sent_by",
                    queryset=Interest.objects.filter(sent_to=self.request.user),
                ),
            )
            .all()
            .exclude(id=self.request.user.id)
        )
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action in ["list"]:
            return UserListSerializer
        return super().get_serializer_class()
