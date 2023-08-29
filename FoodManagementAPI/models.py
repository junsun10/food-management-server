from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

from unidecode import unidecode


class IngredientCategory(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(unidecode(self.title), allow_unicode=True)
        super().save(*args, **kwargs)


class Ingredient(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    category = models.ForeignKey(IngredientCategory, on_delete=models.PROTECT)

    def __str__(self):
        return self.title


class UserIngredient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=5, decimal_places=1)

    class Meta:
        unique_together = ('user', 'ingredient')

    def __str__(self):
        return self.user.username + "_" + self.ingredient.title + "_" + str(self.quantity)


class RecipeCategory(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(unidecode(self.title), allow_unicode=True)
        super().save(*args, **kwargs)


class Recipe(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    code = models.IntegerField(unique=True)
    category = models.ForeignKey(RecipeCategory, on_delete=models.PROTECT)

    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    def __str__(self):
        return self.recipe.title + "_" + self.ingredient.title


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    buy = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'ingredient')

    def __str__(self):
        return self.user.username + "_" + self.ingredient.title
