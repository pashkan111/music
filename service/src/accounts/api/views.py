from django.http import response
from rest_framework import (
    status,
    mixins,
    viewsets,
    parsers,
    permissions,
    generics,
    views,
)
from rest_framework.response import Response
from .serializers import (
    AuthSerializer,
    AuthorSerializer,
    AuthorLinkSerializer,
    LoginSerializer,
    RegisterSerializer,
)
from src.base.permissions import IsAuthor
from ..services.base_auth import User


class AuthView(viewsets.ModelViewSet):
    serializer_class = AuthSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = (parsers.MultiPartParser,)

    def get_queryset(self):
        user = self.request.user
        if not user.is_anonymous:
            return user
        return None

    def get_object(self):
        return self.get_queryset()


class AuthorView(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all().prefetch_related("link_related")
    serializer_class = AuthorSerializer


class AuthorLinkView(viewsets.ModelViewSet):
    serializer_class = AuthorLinkSerializer
    permission_classes = (IsAuthor,)

    def get_queryset(self):
        return self.request.user.link_related.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class Register(generics.GenericAPIView, mixins.CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def post(self, *args, **kwargs):
        return self.create(*args, **kwargs)


class Login(views.APIView):
    serializer_class = LoginSerializer
    queryset = User.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                user = User.objects.get(email=request.data["email"])
            except User.DoesNotExist:
                return Response(
                    data="Invalid credentials", status=status.HTTP_400_BAD_REQUEST
                )
            token = user.token
            return Response(token)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
