from django.http.response import FileResponse, Http404
from .serializers import (
    GenreSerializer,
    LicenseSerializer,
    AlbumSerializer,
    AuthorTrackSerializer,
    CreateAuthorTrackSerializer,
    AuthorPlaylistSerializer,
    CreateAuthorPlaylistSerializer,
)
from rest_framework import generics, views, viewsets, parsers
from src.music import models
from src.base import permissions, mixins
from src.accounts.services.services import delete_old_file
from src.accounts.services.base_auth import User
import os


class GenreListView(generics.ListCreateAPIView):
    """
    List of genres
    """

    serializer_class = GenreSerializer
    queryset = models.Genre.objects.all()


class LicenseListView(viewsets.ModelViewSet):
    """
    List of licenses
    """

    serializer_class = LicenseSerializer
    permission_classes = (permissions.IsAuthor,)

    def get_queryset(self):
        return models.License.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserAlbumView(viewsets.ModelViewSet):
    """
    Albums of certain user
    """

    serializer_class = AlbumSerializer
    permission_classes = (permissions.IsAuthor,)
    parser_classes = (
        parsers.JSONParser,
        parsers.MultiPartParser,
    )

    def get_queryset(self):
        return models.Album.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        if instance.image:
            delete_old_file(instance.image.path)
        instance.delete()


class AlbumView(generics.ListAPIView):
    """
    List of albums
    """

    serializer_class = AlbumSerializer

    def get_queryset(self):
        user_id = self.kwargs.get("id", None)
        if user_id is not None:
            return models.Album.objects.filter(user__id=user_id, private=False)


class TrackView(mixins.SerializerMixin, viewsets.ModelViewSet):
    """
    CRUD of tracks
    """

    serializer_class = CreateAuthorTrackSerializer
    permission_classes = (permissions.IsAuthor,)
    # parser_classes = (parsers.JSONParser,)
    parser_classes = (parsers.MultiPartParser,)
    serializer_classes_by_action = {"list": AuthorTrackSerializer}

    def create(self, request, *args, **kwargs):
        print(request.data)
        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        return models.Track.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        if instance.file:
            delete_old_file(instance.image.path)
            delete_old_file(instance.file.path)
        return super().perform_destroy(instance)


class PlaylistView(mixins.SerializerMixin, viewsets.ModelViewSet):
    """
    CRUD of playlists
    """

    serializer_class = CreateAuthorPlaylistSerializer
    permission_classes = (permissions.IsAuthor,)
    parser_classes = (parsers.MultiPartParser,)
    serializer_classes_by_action = {"list": AuthorPlaylistSerializer}

    def get_queryset(self):
        return models.Playlist.objects.filter(user=self.request.user)

    def perform_destroy(self, instance):
        if instance.file:
            delete_old_file(instance.image.path)
        return super().perform_destroy(instance)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TrackListView(generics.ListAPIView):
    """
    List of all tracks
    """

    serializer_class = AuthorTrackSerializer
    queryset = models.Track.objects.all()
    pagination_class = mixins.Pagination


class TrackAuthorListView(generics.ListAPIView):
    """
    List of certain author's tracks
    """

    serializer_class = AuthorTrackSerializer
    pagination_class = mixins.Pagination

    def get_queryset(self):
        return models.Track.objects.filter(
            user__id=self.kwargs.get("pk"), private=False, album__private=False
        )


class StreamingFileView(views.APIView):
    """
    stream track
    """

    def change_count_stream(self, track):
        track.plays_count += 1
        track.save()

    def get(self, request, *args, **kwargs):
        track_id = kwargs.get("pk")
        track = generics.get_object_or_404(models.Track, id=track_id)
        if os.path.exists(track.file.path):
            self.change_count_stream(track)
            return FileResponse(open(track.file.path, "rb"), filename=track.file.name)
        return Http404


class DownloadTrackView(views.APIView):
    """
    download track
    """

    def change_download_count(self):
        self.track.download += 1
        self.track.save()

    def get(self, request, *args, **kwargs):
        track_id = kwargs.get("pk")
        track = generics.get_object_or_404(models.Track, id=track_id)
        if os.path.exists(track.file.path):
            self.change_download_count(track)
            return FileResponse(
                open(track.file.path, "rb"),
                filename=track.file.name,
                as_attachment=True,
            )
        return Http404
