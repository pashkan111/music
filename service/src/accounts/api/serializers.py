from django.db.models import fields
from rest_framework import serializers, exceptions
from ..models import AuthUser, CocialLink
from ..services.base_auth import User
from django.contrib.auth import authenticate


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email', 'password'
        )

    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')
        user = User.objects.create_user(email=email, password=password)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)
# class LoginSerializer(serializers.Serializer):
#     email = serializers.CharField(max_length=255)
#     password = serializers.CharField(max_length=255)

    def validate(self, data):
        email = data['email']
        password = data.get('password')
        user = authenticate(email=email, password=password)
        if not user:
            return exceptions.AuthenticationFailed('No user matching this token was found')
        return user


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

