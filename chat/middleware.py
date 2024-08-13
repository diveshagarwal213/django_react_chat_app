from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken


@database_sync_to_async
def get_user(user_id):
    User = get_user_model()
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()


class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query_string = parse_qs(scope["query_string"].decode())
        token = query_string.get("token")
        if token:
            try:
                access_token = AccessToken(token[0])
                scope["user"] = await get_user(access_token["user_id"])
            except Exception as e:
                print(str(e))
                scope["user"] = AnonymousUser()
        else:
            print("token not found!")
            scope["user"] = AnonymousUser()

        return await super().__call__(scope, receive, send)
