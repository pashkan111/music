from rest_framework import serializers


class CredentialsSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
