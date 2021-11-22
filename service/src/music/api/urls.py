from django.urls import path
from . import views


urlpatterns = [
    path('genres/', views.GenreListView.as_view()),

    path('licenses/', views.LicenseListView.as_view({
        'get': 'list', 'post': 'create'
        })),
    path('licenses/<int:id>', views.LicenseListView.as_view({
        'put': 'update', 'delete': 'destroy'
        })),

    path('albums-author/', views.UserAlbumView.as_view({
        'get': 'list', 'post': 'create'
        })),
    path('albums-author/<int:pk>', views.UserAlbumView.as_view({
        'put': 'update', 'delete': 'destroy', 'get': 'retrieve'
        })),
    path('albums/<int:id>', views.AlbumView.as_view()),

    path('tracks/', views.TrackView.as_view({
        'get': 'list', 'post': 'create'
        })),
    path('tracks/<int:pk>', views.TrackView.as_view({
        'put': 'update', 'delete': 'destroy', 'get': 'retrieve'
        })),
    path('tracks-list/', views.TrackListView.as_view()),
    path('author-tracks-list/<int:pk>', views.TrackAuthorListView.as_view()),
    path('stream-track/<int:pk>', views.StreamingFileView.as_view()),
    path('download-track/<int:pk>', views.DownloadTrackView.as_view()),

    path('playlists/', views.PlaylistView.as_view({
        'get': 'list', 'post': 'create'
        })),
    path('playlists/<int:pk>', views.PlaylistView.as_view({
        'put': 'update', 'delete': 'destroy', 'get': 'retrieve'
        })),
]

