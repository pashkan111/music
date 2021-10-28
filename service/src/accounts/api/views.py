from rest_framework import serializers, viewsets, parsers, permissions
from .serializers import AuthSerializer, AuthorSerializer, AuthorLinkSerializer
from ..models import AuthUser
from src.base.permissions import IsAuthor


class AuthView(viewsets.ModelViewSet):
    serializer_class = AuthSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = (parsers.MultiPartParser, )

    def get_queryset(self):
        return self.request.user

    def get_object(self):
        return self.get_queryset()


class AuthorView(viewsets.ReadOnlyModelViewSet):
    queryset = AuthUser.objects.all().prefetch_related('link_related')
    serializer_class = AuthorSerializer


class AuthorLinkView(viewsets.ModelViewSet):
    serializer_class = AuthorLinkSerializer
    permission_classes = (IsAuthor,)

    def get_queryset(self):
        return self.request.user.link_related.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)