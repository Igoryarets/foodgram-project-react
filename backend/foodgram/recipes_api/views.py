from io import StringIO
from wsgiref.util import FileWrapper

from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .filter import RecipeFilter
from .models import FavoriteRecipe, Ingredient, Recipe, ShoppingCart, Tag
from .permissions import AuthorOrReadOnly
from .serializers import (FavoriteRecipeSerializer, IngredientSerializer,
                          RecipeSerializer, ShopRecipeSerializer,
                          TagSerializer)


class RecipeListDetailUpdate(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (AuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter,
                       filters.SearchFilter)
    filter_class = RecipeFilter
    filterset_fields = ('tags', 'author')
    ordering_fields = ('name',)
    search_fields = ('ingredients',)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)


class AddDeleteShoppingCart(generics.CreateAPIView, generics.DestroyAPIView):
    queryset = ShoppingCart.objects.all()
    serializer_class = ShopRecipeSerializer

    def create(self, request, *args, **kwargs):
        recipe_id = kwargs['recipe_id']
        recipe = get_object_or_404(Recipe, id=recipe_id)
        if ShoppingCart.objects.filter(
                user=self.request.user, recipe=recipe).exists():
            return Response(
                {'errors': 'Такой рецепт уже есть в корзине'},
                status=status.HTTP_400_BAD_REQUEST
            )
        add_shop_cart = ShoppingCart.objects.create(
            user=self.request.user, recipe=recipe)
        serializer = self.get_serializer(add_shop_cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        recipe_id = kwargs['recipe_id']
        recipe = get_object_or_404(Recipe, id=recipe_id)
        ShoppingCart.objects.filter(
            user=self.request.user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddDeleteFavoriteRecipe(generics.CreateAPIView, generics.DestroyAPIView):
    queryset = FavoriteRecipe.objects.all()
    serializer_class = FavoriteRecipeSerializer

    def create(self, request, *args, **kwargs):
        recipe_id = kwargs['recipe_id']
        recipe = get_object_or_404(Recipe, id=recipe_id)
        if FavoriteRecipe.objects.filter(
                user=self.request.user, recipe=recipe).exists():
            return Response(
                {'errors': 'Такой рецепт уже есть в списке избранных'},
                status=status.HTTP_400_BAD_REQUEST
            )
        add_favorit = FavoriteRecipe.objects.create(
            user=self.request.user, recipe=recipe)
        serializer = self.get_serializer(add_favorit)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        recipe_id = kwargs['recipe_id']
        recipe = get_object_or_404(Recipe, id=recipe_id)
        FavoriteRecipe.objects.filter(
            user=self.request.user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagListDetail(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    filter_backends = DjangoFilterBackend, filters.OrderingFilter
    filterset_fields = ('slug',)
    ordering_fields = ('name',)
    pagination_class = None


class IngridientListDetail(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None


@api_view(['GET'])
def download_shopping_cart(request):
    user = request.user
    ingredients = Ingredient.objects.filter(
        recipe__shopping_cart__user=user
    ).values(
        'name', 'measurement_unit'
    ).annotate(amount=Sum('ingredient__amount'))

    ingredient_list = []

    for ingredient in ingredients:
        ingredient_list.append(
            f"{ingredient.get('name')} "
            f"({ingredient.get('measurement_unit')}) - "
            f"{ingredient.get('amount')}"
        )

    data = '\n'.join(ingredient_list)
    file_name = f'{user.username}_shopping_cart.txt'
    file = StringIO(data)
    response = HttpResponse(FileWrapper(file), content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename={file_name}'

    return response
