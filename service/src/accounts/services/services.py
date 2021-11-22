from django.core.exceptions import ValidationError
import os


def get_avatar_path(instance, file):
    return f"avatar/{instance.id}/{file}"


def get_album_path(instance, file):
    return f"album/{instance.user.id}/{file}"


def get_track_path(instance, file):
    return f"track/{instance.id}/{file}"


def get_playlist_path(instance, file):
    return f"playlist/{instance.id}/{file}"


def validate_image_size(image_obj):
    size_limit = 2
    if image_obj.size > size_limit * 1024 * 1024:
        raise ValidationError("Размер не может превышать 2 мб")


def delete_old_file(path_file):
    if os.path.exists(path_file):
        os.remove(path_file)
