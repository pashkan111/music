from django.core.exceptions import ValidationError


def get_avatar_path(instance, file):
    return f'avatar/{instance.id}/{file}'


def validate_avatar_size(avatar_obj):
    size_limit = 2
    if avatar_obj.size > size_limit * 1024 * 1024:
        raise ValidationError('Размер не может превышать 2 мб')
