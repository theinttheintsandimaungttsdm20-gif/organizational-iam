from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
import jwt

class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(
            token,
            settings.JWT_SETTINGS["SIGNING_KEY"],
            algorithms=[settings.JWT_SETTINGS["ALGORITHM"]],
            audience=settings.JWT_SETTINGS["AUDIENCE"],
            issuer=settings.JWT_SETTINGS["ISSUER"],
        )
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token expired")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token")
        
        scope_str = payload.get("scope", "")
        request.scopes = scope_str.split() if scope_str else []

        user_id = payload.get("sub")
        if not user_id:
            raise AuthenticationFailed("Invalid token payload")

        from identity.models import User
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise AuthenticationFailed("User not found")

        return (user, None)
