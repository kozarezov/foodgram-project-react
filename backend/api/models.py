from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    """Модель ингредиентов."""

    name = models.CharField(
        max_length=200,
        verbose_name='Название',
        help_text='Введите название ингредиента',
    )
    measure = models.CharField(
        max_length=200,
        verbose_name='Единица измерения',
        help_text='Введите единицу измерения',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}, {self.measure}'


class Tag(models.Model):
    """Модель тэгов."""

    name = models.CharField(
        verbose_name='Название',
        max_length=100,
        unique=True,
        db_index=True,
        help_text='Введите название тэга',
    )
    color = models.CharField(
        max_length=7,
        verbose_name='Цветовой HEX-код',
        validators=[RegexValidator(regex=r'^#([A-Fa-f0-9]{6})$')],
        unique=True,
    )
    slug = models.SlugField(
        max_length=20,
        unique=True,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return f'{self.name} (цвет: {self.color})'


class NumberIngredient(models.Model):
    """Модель для количества ингредиентов в блюде."""

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
        related_name='ingredients_amount',
    )
    amount = models.PositiveIntegerField(
        verbose_name='Количество ингредиента',
        default=0,
        validators=(
            MinValueValidator(
                1, 'Слишком малое количество ингредиента.'
            ),
        ),
    )

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'

    def __str__(self):
        return f'{self.amount} {self.ingredient}'


class Recipe(models.Model):
    """Модель рецептов."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта',
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
        help_text='Введите название рецепта',
    )
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='recipes/',
    )
    text = models.TextField(
        verbose_name='Описание',
        help_text='Введите описание рецепта',
    )
    ingredients = models.ManyToManyField(
        'NumberIngredient',
        related_name='recipes',
        verbose_name='Ингредиенты',
        help_text='Выберите ингредиенты для рецепта',
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Теги',
        help_text='Выберите подходящие теги для рецепта',
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления',
        validators=[MinValueValidator(
            1,
            'Слишком маленькое время приготовления'
        )],
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )
    favorite = models.BooleanField('Избранное', default=False)
    cart = models.BooleanField('В списке покупок', default=False)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name

    @property
    def is_favorited(self):
        return self.favorite

    @property
    def is_in_shopping_cart(self):
        return self.cart


class FavoriteRecipe(models.Model):
    """Модель для избранных рецептов."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_author',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite_recipe',
    )
    date_added = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='favorite_user_recept_unique'
            )
        ]

    def __str__(self):
        return f'Рецепт {self.recipe} в избранном у {self.user}'


class Follow(models.Model):
    """Модель для подписок."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
    )
    subscription_date = models.DateField(
        auto_now_add=True,
        verbose_name='Дата подписки',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'], name='follow_unique'
            )
        ]

    def __str__(self):
        return f'{self.user} подписан на {self.author}'


class ShoppingList(models.Model):
    """Модель для покупок."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_lists',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_lists',
    )
    date_added = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления',
    )

    class Meta:
        ordering = ('-date_added',)
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='shopping_user_recipe_unique'
            )
        ]

    def __str__(self):
        return f'Рецепт {self.recipe} в списке покупок {self.user}'
