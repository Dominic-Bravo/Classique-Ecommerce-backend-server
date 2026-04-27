from rest_framework import serializers
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model with all fields."""
    
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for Product model with nested category information."""
    
    category = CategorySerializer(read_only=True)
    
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    """Dedicated serializer for creating and updating products, with category as ID."""
    
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'stock']
        extra_kwargs = {
            'price': {'min_value': 0},
            'stock': {'min_value': 0},
        }
    
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value
    
    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock cannot be negative.")
        return value