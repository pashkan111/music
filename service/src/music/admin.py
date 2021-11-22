from django.contrib import admin
from .models import *


@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    list_display_links = ('user',)
    list_filter = ('user',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('name',)


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'created')
    list_display_links = ('user',)
    list_filter = ('user',)


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'created', 'album')
    list_display_links = ('user', 'album')
    list_filter = ('user', 'album')
