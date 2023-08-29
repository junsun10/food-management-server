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
        fields = ['id', 'title', 'slug']


class IngredientSerializer(serializers.ModelSerializer):
    category = IngredientCategorySerializer(read_only=True)

    class Meta:
        model = Ingredient
        fields = ['id', 'title', 'category']


class UserIngredientSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    ingredient = IngredientSerializer(read_only=True)

    user_id = serializers.PrimaryKeyRelatedField(
        source='user', queryset=User.objects.all(), write_only=True)
    ingredient_id = serializers.PrimaryKeyRelatedField(
        source='ingredient', queryset=Ingredient.objects.all(), write_only=True)

    class Meta:
        model = UserIngredient
        fields = ['id', 'user', 'ingredient',
                  'user_id', 'ingredient_id', 'quantity']


class RecipeCategorySerializer(serializers.ModelSerializer):
    pass


class RecipeSerializer(serializers.ModelSerializer):
    pass


class RecipeIngredientSerializer(serializers.ModelSerializer):
    pass


class CartSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    ingredient = IngredientSerializer(read_only=True)

    user_id = serializers.PrimaryKeyRelatedField(
        source='user', queryset=User.objects.all(), write_only=True)
    ingredient_id = serializers.PrimaryKeyRelatedField(
        source='ingredient', queryset=Ingredient.objects.all(), write_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'ingredient',
                  'user_id', 'ingredient_id', 'buy']
