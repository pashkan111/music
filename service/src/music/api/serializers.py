from rest_framework import serializers
from src.music import models
from src.accounts.services.services import delete_old_file
from src.accounts.services.base_auth import User
from src.accounts.api.serializers import AuthorSerializer


class UserSerializer(serializers.StringRelatedField):
    def to_representation(self, value):
        return super().to_representation(value)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Genre
        fields = "__all__"


class LicenseSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = models.License
        fields = ("user", "text")


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Album
        fields = ("id", "name", "description", "private", "image", "created")

    def update(self, instance, validated_data):
        image = instance.image
        if image:
            delete_old_file(instance.image.path)
        return super().update(instance, validated_data)


class CreateAuthorTrackSerializer(serializers.ModelSerializer):
    plays_count = serializers.IntegerField(read_only=True)
    download = serializers.IntegerField(read_only=True)
    likes_count = serializers.IntegerField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = models.Track
        fields = (
            "id",
            "name",
            "license",
            "album",
            "genre",
            "file",
            "created",
            "plays_count",
            "download",
            "likes_count",
            "private",
            "image",
            "user",
        )

    def update(self, instance, validated_data):
        if instance.image:
            delete_old_file(instance.file.path)
        return super().update(instance, validated_data)


class AuthorTrackSerializer(CreateAuthorTrackSerializer):
    license = LicenseSerializer()
    genre = GenreSerializer(many=True)
    album = AlbumSerializer()
    user = AuthorSerializer()


class CreateAuthorPlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Playlist
        fields = ("id", "name", "tracks", "image", "user")

    def update(self, instance, validated_data):
        if instance.image:
            delete_old_file(instance.file.path)
        return super().update(instance, validated_data)


class AuthorPlaylistSerializer(CreateAuthorPlaylistSerializer):
    tracks = AuthorTrackSerializer(many=True, read_only=True)
