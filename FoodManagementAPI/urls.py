from django.urls import path, include
from . import views

urlpatterns = [
    path('ingredient-category', views.IngredientCategoryView.as_view()),
    path('ingredient-category/<int:pk>',
         views.SingleIngredientCategoryView.as_view()),
    path('ingredient', views.IngredientView.as_view()),
    path('ingredient/<int:pk>', views.SingleIngredientView.as_view()),
    path('user-ingredient', views.UserIngredientView.as_view()),
    path('user-ingredient/<int:pk>', views.SingleUserIngredientView.as_view()),
    path('user-cart', views.CartView.as_view()),
    path('user-cart/<int:pk>', views.SingleCartView.as_view()),
]
