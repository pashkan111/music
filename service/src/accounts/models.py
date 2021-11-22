from django.db import models
from .services.base_auth import User


class Follower(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscribers')

    def __str__(self):
        return f'{self.subscriber} is subscribed on {self.user}'


class SocialLink(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='link_related')
    link = models.URLField(max_length=100)

    def __str__(self):
        return f'{self.user} link'