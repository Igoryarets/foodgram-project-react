from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action, api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Subscription, User
from .serializers import (GetTokenSerializer, RegisterSerializer,
                          SubscriptionSerializer, UserNewPasswordSerializer,
                          UserSerializer)


class RegisterGetUserAPI(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    filter_backends = DjangoFilterBackend, filters.OrderingFilter
    ordering_fields = ('username', 'first_name', 'last_name')
    ordering = ('first_name',)

    def perform_create(self, serializer):
        password = make_password(self.request.data['password'])
        serializer.save(password=password)

    def get_serializer_class(self):
        if self.action == 'list' or 'retrieve':
            return UserSerializer
        return RegisterSerializer

    @action(
        url_path='me',
        detail=False,
    )
    def about_me(self, request):
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(serializer.data)


@api_view(['POST'])
def logout(request):
    token = get_object_or_404(Token, user=request.user)
    token.delete()
    return Response()


@api_view(['POST'])
def set_password(request):
    serializer = UserNewPasswordSerializer(
        data=request.data, context={'request': request}
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(
        'Пароль успешно изменен', status=status.HTTP_204_NO_CONTENT
    )


class SubscriptionList(viewsets.ReadOnlyModelViewSet):
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        subscription = Subscription.objects.filter(user=self.request.user)
        return subscription


class SubscriptionApi(generics.CreateAPIView, generics.DestroyAPIView):

    serializer_class = SubscriptionSerializer

    def create(self, request, *args, **kwargs):
        author_id = kwargs['user_id']
        author = get_object_or_404(User, id=author_id)
        data = {
            'user_id': request.user.id,
            'author_id': author_id,
            'user': self.request.user,
            'author': author
        }
        self.get_serializer().validate(data)
        subscription = Subscription.objects.create(
            user=self.request.user, author=author
        )
        serializer = self.get_serializer(subscription)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        author_id = kwargs['user_id']
        author = get_object_or_404(User, id=author_id)
        Subscription.objects.filter(
            user=self.request.user, author=author
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GetTokenAPI(generics.CreateAPIView):
    serializer_class = GetTokenSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            "auth_token": str(token)},
            status=status.HTTP_201_CREATED,
        )
