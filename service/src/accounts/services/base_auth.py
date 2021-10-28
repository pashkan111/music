from django.conf import settings
import datetime
import jwt
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.CharField(max_length=255, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @property
    def token(self):
        token = self._create_token(user_id=self.id)
        return token


    def _create_token(self, user_id: int) -> dict:
        access_token_expires = datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return {
            'user_id': user_id,
            'access_token': self._create_access_token(
                data={'user_id': user_id}, expires_data=access_token_expires
            ),
            'token_type': 'TokenJWT'
        }


    def _create_access_token(self, data: dict, expires_delta: datetime.timedelta = None) -> str:
        to_encode = data.copy()
        if not expires_delta:
            expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
        expire = datetime.datetime.utcnow() + expires_delta
        to_encode.update({
            'expire': expire,
            'sub': 'access'
        })
        encoded_jwt = jwt.encode(to_encode, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
    