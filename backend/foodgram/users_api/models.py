from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Переопределяем поля в соответствии с ТЗ."""

    email = models.EmailField(
        'Адрес электронной почты',
        max_length=254,
        unique=True
    )

    username = models.CharField(
        'Ваш логин',
        max_length=150,
        unique=True
    )

    first_name = models.CharField(
        'Ваше имя',
        max_length=150
    )

    last_name = models.CharField(
        'Ваша фамилия',
        max_length=150
    )

    password = models.CharField(
        'Пароль',
        max_length=150,
        unique=True
    )


class Subscription(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="follower"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following"
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='unique_subscription',
            )
        ]

    def __str__(self):
        return f'подписчик {self.user}, автор рецепта {self.author}'
