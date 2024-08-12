# from django.conf import settings
from django.contrib.auth import get_user_model
from djoser.conf import settings as djoser_settings
from djoser.views import UserViewSet

User = get_user_model()
# Create your views here.


class CustomUserViewSet(UserViewSet):
    def get_queryset(self):
        user = self.request.user
        queryset = User.objects.select_related("customer", "seller").all()
        if djoser_settings.HIDE_USERS and self.action == "list" and not user.is_staff:
            queryset = queryset.filter(pk=user.pk)
        return queryset
