from django.contrib import admin

from .models import FavoriteRecipe, Ingredient, Recipe, ShoppingCart, Tag


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'author', 'name', 'image', 'text',
        'cooking_time', 'get_favorite_count',
    )
    search_fields = ('name', )
    list_filter = ('author', 'name', 'tags')
    empty_value_display = '-пусто-'

    def get_favorite_count(self, object):
        return object.favorite_recipe.count()


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'name', 'color', 'slug',
    )
    search_fields = ('name', )
    list_filter = ('name', )
    empty_value_display = '-пусто-'


@admin.register(Ingredient)
class IngridientAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'name', 'measurement_unit',
    )
    search_fields = ('name', )
    list_filter = ('name', )
    empty_value_display = '-пусто-'


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):

    list_display = ('pk', 'user', 'get_recipe', )
    empty_value_display = '-пусто-'

    def get_recipe(self, object):
        return object.recipe


@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(admin.ModelAdmin):

    list_display = ('pk', 'user', 'get_recipe', )
    empty_value_display = '-пусто-'

    def get_recipe(self, object):
        return object.recipe
