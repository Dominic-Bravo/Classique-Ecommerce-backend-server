from django.db import transaction
from rest_framework import serializers

from catalog.models import Product
from catalog.serializers import ProductSerializer
from .models import Order, OrderItem


class OrderItemCreateSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    quantity = serializers.IntegerField(min_value=1)


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "product", "quantity", "unit_price", "line_total"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "customer",
            "status",
            "total_price",
            "items",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "customer",
            "status",
            "total_price",
            "created_at",
            "updated_at",
        ]


class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemCreateSerializer(many=True)

    class Meta:
        model = Order
        fields = ["id", "items"]
        read_only_fields = ["id"]

    def validate_items(self, items):
        if not items:
            raise serializers.ValidationError("At least one product is required.")

        product_quantities = {}
        for item in items:
            product = item["product"]
            product_quantities[product.id] = product_quantities.get(product.id, 0) + item["quantity"]

        products = Product.objects.filter(id__in=product_quantities.keys())
        for product in products:
            requested_quantity = product_quantities[product.id]
            if requested_quantity > product.stock:
                raise serializers.ValidationError(
                    f"Only {product.stock} units available for {product.name}."
                )

        return items

    @transaction.atomic
    def create(self, validated_data):
        items = validated_data.pop("items")
        customer = self.context["request"].user
        order = Order.objects.create(customer=customer)

        total_price = 0
        for item in items:
            product = item["product"]
            quantity = item["quantity"]
            line_total = product.price * quantity

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                unit_price=product.price,
                line_total=line_total,
            )
            product.stock -= quantity
            product.save(update_fields=["stock", "updated_at"])
            total_price += line_total

        order.total_price = total_price
        order.save(update_fields=["total_price", "updated_at"])
        return order
