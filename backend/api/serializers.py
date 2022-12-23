from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import (FavoriteRecipe, Follow, Ingredient, NumberIngredient,
                     ShoppingList, Recipe, Tag)

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели User."""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'password'
        )
        read_only_fields = 'is_subscribed',

    def get_is_subscribed(self, obj):
        """Подписка пользователя."""

        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Follow.objects.filter(
            user=request.user,
            author=obj.id).exists()
