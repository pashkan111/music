from django.conf import settings
import datetime
import jwt
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from .services import get_avatar_path, validate_image_size
from django.core.validators import FileExtensionValidator


class MyManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    email = models.CharField(max_length=255, unique=True)
    username = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(max_length=2000, blank=True, null=True)
    display_name = models.CharField(max_length=255, blank=True, null=True)
    avatar = models.ImageField(
        upload_to=get_avatar_path,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=('jpg', 'png')), validate_image_size]
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = MyManager()

    @property
    def token(self):
        token = self._create_token(user_id=self.id)
        return token

    def _create_token(self, user_id: int) -> dict:
        access_token_expires = datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return {
            'user_id': user_id,
            'access_token': self._create_access_token(
                data={'user_id': user_id}, expires_delta=access_token_expires
            ),
            'token_type': 'TokenJWT'
        }


    def _create_access_token(self, data: dict, expires_delta: datetime.timedelta = None) -> str:
        to_encode = data.copy()
        if not expires_delta:
            expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
        expire = (datetime.datetime.utcnow() + expires_delta).isoformat()
        to_encode.update({
            'expire': expire,
            'sub': 'access'
        })
        encoded_jwt = jwt.encode(to_encode, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
    
