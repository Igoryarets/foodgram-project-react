from django.contrib import admin

from .models import (FavoriteRecipe, Ingredient, Recipe, RecipeIngredient,
                     RecipeTag, ShoppingCart, Tag)


class RecipeTagAdmin(admin.StackedInline):
    model = RecipeTag
    autocomplete_fields = ('tag',)


class RecipeIngredientAdmin(admin.StackedInline):
    model = RecipeIngredient
    autocomplete_fields = ('ingredient',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'author', 'name', 'image', 'text',
        'cooking_time', 'get_favorite_count',
        'get_ingredients', 'get_tags'
    )
    search_fields = ('name', 'author__username', 'tags__name')
    list_filter = ('author', 'name', 'tags')
    inlines = (RecipeTagAdmin, RecipeIngredientAdmin,)
    empty_value_display = '-пусто-'

    def get_favorite_count(self, object):
        return object.favorite_recipe.count()

    def get_tags(self, object):
        tags_list = []
        for obj in object.tags.all():
            tags_list.append(obj.name)
        return tags_list

    def get_ingredients(self, object):
        ingredient_list = []
        for obj in object.recipe.all():
            ingredient_list.append(
                f'{obj.ingredient.name} - {obj.amount}'
                f'{obj.ingredient.measurement_unit}.'
            )
        return ingredient_list


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
