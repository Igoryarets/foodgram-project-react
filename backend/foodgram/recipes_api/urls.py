from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .utils import download_shopping_cart
from .views import (AddDeleteFavoriteRecipe, AddDeleteShoppingCart,
                    IngridientListDetail, RecipeListDetailUpdate,
                    TagListDetail)

router = SimpleRouter()

router.register('recipes', RecipeListDetailUpdate, basename='recipes')
router.register('tags', TagListDetail, basename='tags')
router.register('ingredients', IngridientListDetail, basename='ingredients')

urlpatterns = [
    path('recipes/download_shopping_cart/', download_shopping_cart,
         name='download_shopping_cart'),
    path('', include(router.urls)),
    path('recipes/<int:recipe_id>/favorite/',
         AddDeleteFavoriteRecipe.as_view(),
         name='favorite_recipe'),
    path('recipes/<int:recipe_id>/shopping_cart/',
         AddDeleteShoppingCart.as_view(),
         name='shopping_cart'),

]
