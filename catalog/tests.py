from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Category, Product

User = get_user_model()


class CatalogPermissionTests(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Shoes")
        Product.objects.create(
            name="Classic Loafer",
            price=120,
            category=self.category,
            stock=5,
        )
        self.customer = User.objects.create_user(
            username="customer",
            password="password123",
            role="customer",
        )
        self.owner = User.objects.create_user(
            username="owner",
            password="password123",
            role="owner",
            owner_approval_status=User.OWNER_APPROVAL_APPROVED,
        )

    def test_anonymous_can_view_products(self):
        response = self.client.get("/api/products/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_customer_cannot_create_product(self):
        self.client.force_authenticate(self.customer)

        response = self.client.post(
            "/api/products/",
            {
                "name": "Oxford",
                "price": "150.00",
                "category": self.category.id,
                "stock": 2,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_owner_can_create_product(self):
        self.client.force_authenticate(self.owner)

        response = self.client.post(
            "/api/products/",
            {
                "name": "Oxford",
                "price": "150.00",
                "category": self.category.id,
                "stock": 2,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
