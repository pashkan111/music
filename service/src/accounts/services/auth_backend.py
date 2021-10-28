from rest_framework import authentication, exceptions
import jwt
from django.conf import settings
from ..models import AuthUser
from typing import Optional

class AuthBackend(authentication.BaseAuthentication):

    authentication_header = 'TokenJWT'

    def authenticate(self, request, token=None, **kwargs) -> Optional[tuple]:
        auth_header = authentication.get_authorization_header(request).split()
        if not auth_header or auth_header[0].lower() != 'token':
            return None
        if len(auth_header) < 2:
            raise exceptions.AuthenticationFailed('Invalid token header')
        elif len(auth_header) > 2:
            raise exceptions.AuthenticationFailed('Invalid token header. Token should not have spaces')
        
        try:
            token = auth_header[1].decode('utf-8')
        except UnicodeError:
            raise exceptions.AuthenticationFailed('Invalid token')
        return self.authenticate_credential(token)


    def authenticate_credential(self, token) -> tuple:
        try:
            payload = jwt.decode(token, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        except jwt.PyJWTError:
            raise exceptions.AuthenticationFailed('Could not to decode a token')
        user_id = payload.get('user_id', None)
        try:
            user = AuthUser.objects.get(id=user_id)
        except AuthUser.DoesNotExist:
            raise exceptions.AuthenticationFailed('No user matching this token was found')
        return user, None

