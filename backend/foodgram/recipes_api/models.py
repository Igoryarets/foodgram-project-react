from colorfield.fields import ColorField
from django.core.validators import MinValueValidator
from django.db import models

from users_api.models import User


class Ingredient(models.Model):

    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Tag(models.Model):

    name = models.CharField(max_length=200, unique=True)
    color = ColorField(format='hex')
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return f'Название тега {self.name}, слаг тега {self.slug}'


class Recipe(models.Model):

    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='recipe',
    )

    name = models.CharField('Название рецепта', max_length=200)

    image = models.ImageField('Изображение блюда',
                              upload_to='media/recipes/images/')

    text = models.TextField('Текстовое описание рецепта',)

    ingredients = models.ManyToManyField(Ingredient,
                                         through='RecipeIngredient')

    tags = models.ManyToManyField(Tag, through='RecipeTag')

    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления в минутах',
        validators=(
            MinValueValidator(
                1,
                message='Минимальное время приготовления = 1 минута'
            ),
        )
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return f'Рецепт {self.name}'


class RecipeIngredient(models.Model):

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='recipe')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,
                                   related_name='ingredient')
    amount = models.PositiveSmallIntegerField(
        validators=(
            MinValueValidator(1, 'Минимальное количество ингредиентов = 1'),
        )
    )

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique ingredient')
        ]


class RecipeTag(models.Model):

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)


class FavoriteRecipe(models.Model):

    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='favorite_recipe',
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='favorite_recipe',
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'


class ShoppingCart(models.Model):

    user = models.ForeignKey(
        User,
        related_name='shopping_cart',
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='shopping_cart',
        on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_shopping_list')
        ]
        verbose_name = 'Корзина с рецептом'
        verbose_name_plural = 'Корзина с рецептами'
