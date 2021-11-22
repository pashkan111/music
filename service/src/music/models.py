from django.db import models
from src.accounts.services.base_auth import User
from src.accounts.services.services import get_album_path, get_track_path, validate_image_size, get_playlist_path
from django.core.validators import FileExtensionValidator


class License(models.Model):
    """
    Класс лицензии
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='licenses'
        )
    text = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return f'license № {self.pk}'


class Genre(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self) -> str:
        return self.name


class Album(models.Model):
    name = models.CharField(max_length=30)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='albums'
        )
    description = models.TextField(null=True, blank=True)
    private = models.BooleanField(default=False)
    image = models.ImageField(
        upload_to=get_album_path,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=('png', 'jpg')), validate_image_size]
    )
    created = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return f'album - {self.name}'


class Track(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='tracks'
        )
    license = models.ForeignKey(
        License, on_delete=models.PROTECT, related_name='tracks'
    )
    album = models.ForeignKey(
        Album, 
        on_delete=models.SET_NULL, 
        related_name='tracks', 
        blank=True,
        null=True
    )
    genre = models.ManyToManyField(Genre, related_name='tracks')
    file = models.FileField(
        upload_to=get_track_path,
        validators=[FileExtensionValidator(allowed_extensions=('mp3', 'png'))],
    )
    created = models.DateField(auto_now_add=True)
    plays_count = models.PositiveIntegerField(default=0)
    download = models.PositiveIntegerField(default=0)
    likes_count = models.PositiveIntegerField(default=0)
    users_of_likes = models.ManyToManyField(
        User, related_name='likes', blank=True
        )

    def __str__(self) -> str:
        return self.name


class Comment(models.Model):
    track = models.ForeignKey(
        Track, on_delete=models.CASCADE, related_name='comments'
        )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
        )
    created = models.DateTimeField(auto_now_add=True)
    text = models.TextField()


class Playlist(models.Model):
    name = models.CharField(
        max_length=100, 
        default='New Playlist', 
        unique=True,
        null=True,
        blank=True
        )
    tracks = models.ManyToManyField(Track, related_name='playlists')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='playlists'
        )
    image = models.ImageField(
        upload_to=get_playlist_path,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=('png', 'jpg')), validate_image_size]
    )
    
