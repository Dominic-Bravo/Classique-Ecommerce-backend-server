from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from catalog.models import Category, Product
from .models import Order

User = get_user_model()


class OrderApiTests(APITestCase):
    def setUp(self):
        category = Category.objects.create(name="Bags")
        self.product = Product.objects.create(
            name="Tote",
            price="75.00",
            category=category,
            stock=3,
        )
        self.customer = User.objects.create_user(
            username="customer",
            password="password123",
            role="customer",
        )

    def test_customer_can_order_product(self):
        self.client.force_authenticate(self.customer)

        response = self.client.post(
            "/api/orders/",
            {
                "items": [
                    {
                        "product": self.product.id,
                        "quantity": 2,
                    }
                ]
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)

        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 1)

    def test_anonymous_cannot_order_product(self):
        response = self.client.post(
            "/api/orders/",
            {
                "items": [
                    {
                        "product": self.product.id,
                        "quantity": 1,
                    }
                ]
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
