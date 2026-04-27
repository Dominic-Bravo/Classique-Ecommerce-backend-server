from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Category, Product
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    ProductCreateUpdateSerializer
)
from .services import CategoryService, ProductService


class CategoryListCreateView(generics.ListCreateAPIView):
    """List all categories or create a new category."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        CategoryService.create_category(serializer.validated_data)


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a category."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        category = self.get_object()
        CategoryService.update_category(category, serializer.validated_data)

    def perform_destroy(self, instance):
        CategoryService.delete_category(instance)


class ProductListCreateView(generics.ListCreateAPIView):
    """List all products or create a new product."""
    queryset = Product.objects.select_related('category').all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductCreateUpdateSerializer
        return ProductSerializer

    def perform_create(self, serializer):
        ProductService.create_product(serializer.validated_data)


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a product."""
    queryset = Product.objects.select_related('category').all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ProductCreateUpdateSerializer
        return ProductSerializer

    def perform_update(self, serializer):
        product = self.get_object()
        ProductService.update_product(product, serializer.validated_data)

    def perform_destroy(self, instance):
        ProductService.delete_product(instance)
