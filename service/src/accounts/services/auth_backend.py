from datetime import datetime
from rest_framework import authentication, exceptions
import jwt
from django.conf import settings
from typing import Optional
from django.contrib.auth.backends import ModelBackend
from .base_auth import User


class AuthBackend(authentication.BaseAuthentication):
    authentication_header = "TokenJWT"

    def authenticate(self, request, token=None, **kwargs) -> Optional[tuple]:
        auth_header = authentication.get_authorization_header(request).split()
        if not auth_header or auth_header[0].lower() != b"token":
            return None
        if len(auth_header) < 2:
            raise exceptions.AuthenticationFailed("Invalid token header")
        elif len(auth_header) > 2:
            raise exceptions.AuthenticationFailed(
                "Invalid token header. Token should not have spaces"
            )
        try:
            token = auth_header[1].decode("utf-8")
        except UnicodeError:
            raise exceptions.AuthenticationFailed("Invalid token")
        return self.authenticate_credential(token)

    def authenticate_credential(self, token) -> tuple:
        try:
            payload = jwt.decode(token, key=settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.PyJWTError:
            raise exceptions.AuthenticationFailed("Could not to decode a token")
        if datetime.fromisoformat(payload["expire"]) < datetime.utcnow():
            raise exceptions.AuthenticationFailed("token is expired")
        user_id = payload.get("user_id", None)
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed(
                "No user matching this token was found"
            )
        return user, None


class SettingsBackend(ModelBackend):
    def _log_to_admin(self, username, password):
        """
        Custom authentication. While attempting log in admin,
        username comes instead of email.
        """
        if username:
            user = User.objects.filter(email=username).first()
        else:
            return None
        if user.check_password(password):
            return user

    def authenticate(self, request=None, email=None, password=None, **kwargs):
        username = kwargs.get("username", None)
        if username:
            user = self._log_to_admin(username, password)
            return user
        user = User.objects.filter(email=email).first()
        if not user:
            return None
        if user.check_password(password):
            return user
        return None
