from django.db import models
from django.core.validators import FileExtensionValidator
from .services.services import get_avatar_path, validate_avatar_size
from .services.base_auth import User


class AuthUser(models.Model):
    email = models.EmailField(max_length=100, unique=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(max_length=2000, blank=True, null=True)
    display_name = models.CharField(max_length=255, blank=True, null=True)
    avatar = models.ImageField(
        upload_to=get_avatar_path,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=('jpg', 'png')), validate_avatar_size]
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @property
    def is_authenticated(self):
        return True

    def __str__(self):
        return self.email


class Follower(models.Model):

    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name='owner')
    subscriber = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name='subscribers')

    def __str__(self):
        return f'{self.subscriber} is subscribed on {self.user}'


class CocialLink(models.Model):
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name='link_related')
    link = models.URLField(max_length=100)

    def __str__(self):
        return f'{self.user} link'