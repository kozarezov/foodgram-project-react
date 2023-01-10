from django.contrib import admin

from .models import (FavoriteRecipe, Follow, Ingredient, NumberIngredient,
                     ShoppingList, Recipe, Tag)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measure')
    search_fields = ('^name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('author', 'name', 'favorited')
    list_filter = ('author', 'name', 'tags')

    def favorited(self, obj):
        return FavoriteRecipe.objects.filter(recipe=obj).count()

    favorited.short_description = 'В избранном'


@admin.register(NumberIngredient)
class NumberIngredientAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'amount')


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('author', 'user')
