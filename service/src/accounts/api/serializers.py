from django.db.models import fields
from rest_framework import serializers, exceptions
from ..models import SocialLink
from ..services.base_auth import User
from django.contrib.auth import authenticate


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "password")

    def create(self, validated_data):
        email = validated_data.get("email")
        password = validated_data.get("password")
        user = User.objects.create_user(email=email, password=password)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)

    def validate(self, data):
        email = data["email"]
        password = data.get("password")
        user = authenticate(email=email, password=password)
        if not user:
            raise exceptions.AuthenticationFailed("No user was found")
        return user


class AuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "email",
            "country",
            "city",
            "display_name",
            "avatar",
        )


class AuthorLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLink
        fields = ("link",)


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "country",
            "city",
            "display_name",
            "avatar",
        )
        read_only_fields = fields
