from django.db.models import fields
from rest_framework import serializers
from ..models import AuthUser, CocialLink


class AuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
        fields = (
        'email', 'country', 'city', 'display_name', 'avatar',
    )


class AuthorLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = CocialLink
        fields = (
            'link',
        )


class AuthorSerializer(serializers.ModelSerializer):
    cocial_link = AuthorLinkSerializer(many=True)
    class Meta:
        model = AuthUser
        fields = (
       'id', 'email', 'country', 'city', 'display_name', 'avatar',
    )
        read_only_fields = fields

