from django.contrib import admin
from .models import IngredientCategory, Ingredient, UserIngredient, RecipeCategory, Recipe, RecipeIngredient, Cart


admin.site.register(IngredientCategory)


# admin.site.register(Ingredient)
@admin.register(Ingredient)
class IngredintAdmin(admin.ModelAdmin):
    list_filter = ('category',)
    search_fields = ('title',)


admin.site.register(UserIngredient)
admin.site.register(RecipeCategory)
admin.site.register(Recipe)
admin.site.register(RecipeIngredient)
admin.site.register(Cart)
