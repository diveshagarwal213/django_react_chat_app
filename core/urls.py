from django.urls import include, path
from rest_framework_nested import routers

from core import views

router = routers.DefaultRouter()


router.register("user", views.CustomUserViewSet, basename="custom-user")
urlpatterns = [
    path("", include(router.urls)),
]
