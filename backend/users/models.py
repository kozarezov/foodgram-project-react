from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Кастомная модель User."""

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLES = (
        (USER, 'Пользователь'),
        (ADMIN, 'Администратор'),
    )
    username = models.CharField('Логин', max_length=150, unique=True)
    email = models.EmailField('Email', max_length=254, unique=True)
    first_name = models.CharField('Имя', max_length=150, blank=True)
    last_name = models.CharField('Фамилия', max_length=150, blank=True)
    role = models.CharField('Роль', max_length=15, choices=ROLES, default=USER)
    subscribe = models.ManyToManyField(
        verbose_name='Подписка',
        related_name='subscribers',
        to='self',
        symmetrical=False,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = (
            models.UniqueConstraint(
                fields=('username', 'email'),
                name='unique_username_email'
            ),
        )

    def __str__(self):
        return f'{self.username} - {self.email}'

    @property
    def is_admin(self):
        return self.is_staff or self.role == self.ADMIN
