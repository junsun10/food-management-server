from rest_framework import serializers
from django.contrib.auth.models import User

from .models import IngredientCategory, Ingredient, UserIngredient, RecipeCategory, Recipe, RecipeIngredient, Cart


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class IngredientCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = IngredientCategory
        fields = ['id', 'title']


class IngredientSerializer(serializers.ModelSerializer):
    category = IngredientCategorySerializer(read_only=True)

    category_id = serializers.PrimaryKeyRelatedField(
        source='category', queryset=IngredientCategory.objects.all(), write_only=True)

    class Meta:
        model = Ingredient
        fields = ['id', 'title', 'category', 'category_id']


class UserIngredientSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    ingredient = IngredientSerializer(read_only=True)

    ingredient_id = serializers.PrimaryKeyRelatedField(
        source='ingredient', queryset=Ingredient.objects.all(), write_only=True)

    class Meta:
        model = UserIngredient
        fields = ['id', 'user', 'ingredient',
                  'ingredient_id', 'quantity', 'start', 'end', 'memo']


class RecipeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeCategory
        fields = ['id', 'title']


class RecipeSerializer(serializers.ModelSerializer):
    category = RecipeCategorySerializer(read_only=True)

    category_id = serializers.PrimaryKeyRelatedField(
        source='category', queryset=RecipeCategory.objects.all(), write_only=True)

    recipe_ingredients = serializers.SerializerMethodField(read_only=True)

    def get_recipe_ingredients(self, obj):
        recipe_ingredients = RecipeIngredient.objects.filter(recipe=obj)
        serializer = RecipeIngredientSerializer(recipe_ingredients, many=True)
        return serializer.data

    class Meta:
        model = Recipe
        fields = ['id', 'code', 'title', 'category',
                  'category_id', 'recipe_ingredients']


class RecipeIngredientSerializer(serializers.ModelSerializer):
    recipe = serializers.SerializerMethodField(read_only=True)
    ingredient = IngredientSerializer(read_only=True)

    recipe_id = serializers.PrimaryKeyRelatedField(
        source='recipe', queryset=Recipe.objects.all(), write_only=True)
    ingredient_id = serializers.PrimaryKeyRelatedField(
        source='ingredient', queryset=Ingredient.objects.all(), write_only=True)

    class Meta:
        model = RecipeIngredient
        fields = ['id', 'ingredient', 'recipe', 'recipe_id', 'ingredient_id']

    def get_recipe(self, obj):
        return {'id': obj.recipe.id, 'code': obj.recipe.code, 'title': obj.recipe.title, 'category': obj.recipe.category.title}


# class CartSerializer(serializers.ModelSerializer):
#     user = UserSerializer(read_only=True)
#     ingredient = IngredientSerializer(read_only=True)

#     user_id = serializers.PrimaryKeyRelatedField(
#         source='user', queryset=User.objects.all(), write_only=True)
#     ingredient_id = serializers.PrimaryKeyRelatedField(
#         source='ingredient', queryset=Ingredient.objects.all(), write_only=True)

#     class Meta:
#         model = Cart
#         fields = ['id', 'user', 'ingredient',
#                   'user_id', 'ingredient_id', 'buy']


class CartSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    ingredient = IngredientSerializer(read_only=True)

    ingredient_id = serializers.PrimaryKeyRelatedField(
        source='ingredient', queryset=Ingredient.objects.all(), write_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'ingredient', 'ingredient_id', 'buy']
