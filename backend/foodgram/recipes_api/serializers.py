from drf_base64.fields import Base64ImageField
from rest_framework import serializers

from users_api.models import Subscription, User

from .models import (FavoriteRecipe, Ingredient, Recipe, RecipeIngredient,
                     ShoppingCart, Tag)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeUserSerializer(serializers.ModelSerializer):

    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        return Subscription.objects.filter(
            user=user.id, author=obj
        ).exists()


class RecipeSerializer(serializers.ModelSerializer):

    tags = TagSerializer(many=True, read_only=True,)
    author = RecipeUserSerializer(
        read_only=True,
    )
    ingredients = RecipeIngredientSerializer(
        many=True, required=True, source='recipe'
    )
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time'
        )

    def get_is_favorited(self, object):
        user = self.context.get('request').user
        return FavoriteRecipe.objects.filter(
            user=user.id,
            recipe=object.id
        ).exists()

    def get_is_in_shopping_cart(self, object):
        user = self.context.get('request').user
        return ShoppingCart.objects.filter(
            user=user.id, recipe=object.id
        ).exists()

    def create(self, validated_data):
        validated_data.pop('recipe')
        tags = self.initial_data.pop('tags')
        ingredients = self.initial_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        for ingredient in ingredients:
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient_id=ingredient.get('id'),
                amount=ingredient.get('amount'),
            )
        return recipe

    def update(self, instance, validated_data):
        validated_data.pop('recipe')
        tags = self.initial_data.pop('tags')
        ingredients = self.initial_data.pop('ingredients')
        if tags:
            instance.tags.set(tags)

        if ingredients:
            instance.ingredients.clear()
            for ingredient in ingredients:
                RecipeIngredient.objects.create(
                    recipe=instance,
                    ingredient_id=ingredient.get('id'),
                    amount=ingredient.get('amount'),
                )
        instance.save()
        return instance


class ShopRecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='recipe.id')
    name = serializers.CharField(source='recipe.name')
    image = Base64ImageField(source='recipe.image')
    cooking_time = serializers.IntegerField(source='recipe.cooking_time')

    class Meta:
        model = ShoppingCart
        fields = ('id', 'name', 'image', 'cooking_time',)


class FavoriteRecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='recipe.id')
    name = serializers.CharField(source='recipe.name')
    image = Base64ImageField(source='recipe.image')
    cooking_time = serializers.IntegerField(source='recipe.cooking_time')

    class Meta:
        model = FavoriteRecipe
        fields = ('id', 'name', 'image', 'cooking_time',)
