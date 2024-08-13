from django.urls import include, path
from rest_framework_nested import routers

from my_app import views

# NOTE: levels represent the nesting between routes

# router config
router = routers.DefaultRouter()

# Level One
router.register("interests", views.InterestViewSet, basename="interests")

# Level Two
interest_router = routers.NestedDefaultRouter(router, "interests", lookup="interest")

interest_router.register(
    "chat_messages", views.ChatMessageViewSet, basename="interest-chat_messages"
)
urlpatterns = [path("", include(router.urls + interest_router.urls))]
