from rest_framework import status, mixins, serializers, viewsets, parsers, permissions, generics, views
from rest_framework.response import Response
from .serializers import AuthSerializer, AuthorSerializer, AuthorLinkSerializer, LoginSerializer, RegisterSerializer
from ..models import AuthUser
from src.base.permissions import IsAuthor
from ..services.base_auth import User


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


class Register(views.APIView):

    serializer_class = RegisterSerializer
    queryset = User.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)


class Login(views.APIView):

    serializer_class = LoginSerializer
    queryset = User.objects.all()
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = User.objects.get(email=request.data['email'])
            token = user.token
            return Response(token)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


# class Authenticator(generics.GenericAPIView, mixins.CreateModelMixin):

#     serializer_class = UserSerializer
#     queryset = User.objects.all()

#     def perform_create(self, serializer):
#         return super().perform_create(serializer)
    
