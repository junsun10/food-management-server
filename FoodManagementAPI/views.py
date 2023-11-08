from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage

from rest_framework import generics, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.pagination import PageNumberPagination

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
            permission_classes.append(IsAdminUser)

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
            permission_classes.append(IsAdminUser)

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


# 설명: 레시피 카테고리 목록 조회, 레시피 카테고리 생성
# 메소드: GET, POST
# URL: /api/recipe-category
class RecipeCategoryView(generics.ListCreateAPIView):
    queryset = RecipeCategory.objects.all()
    serializer_class = RecipeCategorySerializer

    # 필터링 설정
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['title']
    ordering_fields = ['id', 'title']
    ordering = ['title']

    # 레시피 카테고리 생성은 staff 권한 필요
    def get_permissions(self):
        permission_classes = [IsAuthenticated]

        if self.request.method == 'POST':
            permission_classes.append(IsAdminUser)

        return [permission() for permission in permission_classes]


# 설명: 단일 레시피 카테고리 조회, 수정, 삭제
# 메소드: GET, PUT, DELETE
# URL: /api/recipe-category/<int:pk>
class SingleRecipeCategoryView(generics.RetrieveUpdateDestroyAPIView):
    # staff 권한 필요
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = RecipeCategory.objects.all()
    serializer_class = RecipeCategorySerializer


# 설명: 레시피 목록 조회, 레시피 생성
# 메소드: GET, POST
# URL: /api/recipe
class RecipeView(generics.ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    # 필터링 설정
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['title', 'category__title']
    ordering_fields = ['id', 'title']
    ordering = ['title']

    # 페이지 설정
    class RecipePagination(PageNumberPagination):
        page_size = 10
        page_size_query_param = 'page_size'
        max_page_size = 20

    pagination_class = RecipePagination

    # 레시피 생성은 staff 권한 필요
    def get_permissions(self):
        permission_classes = [IsAuthenticated]

        if self.request.method == 'POST':
            permission_classes.append(IsAdminUser)

        return [permission() for permission in permission_classes]


# 설명: 단일 레시피 조회, 수정, 삭제
# 메소드: GET, PUT, DELETE
# URL: /api/recipe/<int:pk>
class SingleRecipeView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def get_permissions(self):
        permission_classes = [IsAuthenticated]

        if self.request.method != 'GET':
            permission_classes.append(IsAdminUser)

        return [permission() for permission in permission_classes]


# 설명: 레시피 식재료 목록 조회, 레시피 식재료 생성
# 메소드: GET, POST
# URL: /api/recipe-ingredient
class RecipeIngredientView(generics.ListCreateAPIView):
    queryset = RecipeIngredient.objects.all()
    serializer_class = RecipeIngredientSerializer

    # 필터링 설정
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['recipe__title']
    ordering_fields = ['id', 'recipe__title', 'ingredient__title']
    ordering = ['recipe__title', 'ingredient__title']

    # 레시피 식재료 생성은 staff 권한 필요
    def get_permissions(self):
        permission_classes = [IsAuthenticated]

        if self.request.method == 'POST':
            permission_classes.append(IsAdminUser)

        return [permission() for permission in permission_classes]


# 설명: 해당 식재료가 포함된 레시피 목록 조회
# 메소드: GET
# URL: /api/ingredient-recipe
class IngredientRecipeView(generics.ListAPIView):
    queryset = RecipeIngredient.objects.all()
    serializer_class = RecipeIngredientSerializer

    # 필터링 설정
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['ingredient__title']
    ordering_fields = ['id', 'recipe__title', 'ingredient__title']
    ordering = ['recipe__title', 'ingredient__title']

    # 페이지 설정
    class IngredientPagination(PageNumberPagination):
        page_size = 10
        page_size_query_param = 'page_size'
        max_page_size = 20

    pagination_class = IngredientPagination

    def get_permissions(self):
        permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]


# 설명: 단일 레시피 식재료 조회, 수정, 삭제
# 메소드: GET, PUT, DELETE
# URL: /api/recipe-ingredient/<int:pk>
class SingleRecipeIngredientView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RecipeIngredient.objects.all()
    serializer_class = RecipeIngredientSerializer

    def get_permissions(self):
        permission_classes = [IsAuthenticated]

        if self.request.method != 'GET':
            permission_classes.append(IsAdminUser)

        return [permission() for permission in permission_classes]
