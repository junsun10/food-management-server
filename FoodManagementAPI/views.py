from django.shortcuts import render

from rest_framework import generics, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import IngredientCategory, Ingredient, UserIngredient, RecipeCategory, Recipe, RecipeIngredient, Cart
from .serializers import IngredientCategorySerializer, IngredientSerializer, UserIngredientSerializer, RecipeCategorySerializer, RecipeSerializer, RecipeIngredientSerializer, CartSerializer


# 설명: 식재료 카테고리 목록 조회, 식재료 카테고리 생성
# 메소드: GET, POST
# URL: /api/ingredient-category
# 식재료 카테고리 생성은 staff 권한 필요
class IngredientCategoryView(generics.ListCreateAPIView):
    queryset = IngredientCategory.objects.all()
    serializer_class = IngredientCategorySerializer

    # 필터링 설정
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    # URL: /api/ingredient?search=<str:search>
    search_fields = ['title']
    # URL: /api/ingredient?ordering=<str:ordering>
    ordering_fields = ['id', 'title']
    # default ordering
    ordering = ['title']

    def get_permissions(self):
        permission_classes = [IsAuthenticated]

        if self.request.method == 'POST':
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]


# 설명: 단일 식재료 카테고리 조회, 수정, 삭제
# 메소드: GET, PUT, DELETE
# URL: /api/ingredient-category/<int:pk>
class SingleIngredientCategoryView(generics.RetrieveUpdateDestroyAPIView):
    # staff 권한 필요
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = IngredientCategory.objects.all()
    serializer_class = IngredientCategorySerializer


# 설명: 식재료 목록 조회, 식재료 생성
# 메소드: GET, POST
# URL: /api/ingredient
class IngredientView(generics.ListCreateAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

    # 필터링 설정
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['title', 'category__title']
    ordering_fields = ['id', 'title']
    ordering = ['title']

    # 식재료 생성은 staff 권한 필요
    def get_permissions(self):
        permission_classes = [IsAuthenticated]

        if self.request.method == 'POST':
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]


# 설명: 단일 식재료 조회, 수정, 삭제
# 메소드: GET, PUT, DELETE
# URL: /api/ingredient/<int:pk>
# staff 권한 필요
class SingleIngredientView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


# 설명: 사용자 식재료 목록 조회, 사용자 식재료 생성
# 메소드: GET, POST
# URL: /api/user-ingredient
class UserIngredientView(generics.ListCreateAPIView):
    serializer_class = UserIngredientSerializer

    # 필터링 설정
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['ingredient__title']
    ordering_fields = ['id', 'ingredient__title']
    ordering = ['ingredient__title']

    def get_permissions(self):
        permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        return UserIngredient.objects.filter(user=user)


# 설명: 단일 사용자 식재료 조회, 수정, 삭제
# 메소드: GET, PUT, DELETE
# URL: /api/user-ingredient/<int:pk>
class SingleUserIngredientView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = UserIngredient.objects.all()
    serializer_class = UserIngredientSerializer


# 설명: 장바구니 목록 조회, 장바구니 생성
# 메소드: GET, POST
# URL: /api/user-cart
class CartView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    # 필터링 설정
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['ingredient__title']
    ordering_fields = ['id', 'ingredient__title']
    ordering = ['ingredient__title']

    def get_queryset(self):
        user = self.request.user
        return Cart.objects.filter(user=user)


# 설명: 단일 장바구니 조회, 수정, 삭제
# 메소드: GET, PUT, DELETE
# URL: /api/user-cart/<int:pk>
class SingleCartView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    def get_queryset(self):
        user = self.request.user
        return Cart.objects.filter(user=user)
