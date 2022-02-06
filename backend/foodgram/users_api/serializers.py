import django.contrib.auth.password_validation as ValidatePassword
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from recipes_api.models import Recipe
from rest_framework import serializers

from .models import Subscription, User


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email',
                  'first_name', 'last_name', 'is_subscribed',)

    def get_is_subscribed(self, object):
        user = self.context.get('request').user
        return Subscription.objects.filter(
            user=user.id, author=object
        ).exists()


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'password', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}

    def validate_password(self, value):
        ValidatePassword.validate_password(value)
        return value


class UserNewPasswordSerializer(serializers.Serializer):

    new_password = serializers.CharField()
    current_password = serializers.CharField()

    def validate_new_password(self, value):
        ValidatePassword.validate_password(value)
        return value

    def validate_current_password(self, current_password):
        user = self.context['request'].user
        if not authenticate(username=user, password=current_password):
            raise serializers.ValidationError(
                {'password': 'Введен неверный пароль.'}
            )

    def create(self, validated_data):
        user = self.context['request'].user
        new_password = make_password(validated_data.get('new_password'))
        User.objects.filter(username=user).update(password=new_password)
        return validated_data


class GetTokenSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()

    def validate(self, data):
        email_request = data.get('email')
        user = User.objects.filter(email=email_request)

        if not user.exists():
            raise serializers.ValidationError({
                'email': 'Неверно указан адрес электронной почты'
            })

        if not get_object_or_404(
                User, email=email_request
        ).check_password(data.get('password')):
            raise serializers.ValidationError({
                'password': 'Введен неверный пароль.'
            })
        return user.get()


class SubscribeRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time',)


class SubscriptionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='author.id')
    email = serializers.EmailField(source='author.email')
    username = serializers.CharField(source='author.username')
    first_name = serializers.CharField(source='author.first_name')
    last_name = serializers.CharField(source='author.last_name')
    recipes = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count',
        )

    def validate(self, data):
        if data['user_id'] == data['author_id']:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя'
            )
        if Subscription.objects.filter(
            user=data['user'], author=data['author']
        ).exists():
            raise serializers.ValidationError(
                'Такая подписка существует'
            )
        return data

    def get_is_subscribed(self, object):
        return Subscription.objects.filter(
            user=object.user, author=object.author
        ).exists()

    def get_recipes(self, object):
        recipes = Recipe.objects.filter(author=object.author)
        return SubscribeRecipeSerializer(recipes, many=True).data

    def get_recipes_count(self, object):
        return Recipe.objects.filter(author=object.author).count()
