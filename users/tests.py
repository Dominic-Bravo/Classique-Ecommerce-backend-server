from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class RegisterRoleTests(APITestCase):
    def test_custom_registration_defaults_to_anonymous_without_role(self):
        response = self.client.post(
            "/api/register/",
            {
                "username": "default-anonymous",
                "email": "default@example.com",
                "password": "password123",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(username="default-anonymous")
        self.assertEqual(user.role, User.ROLE_ANONYMOUS)
        self.assertEqual(
            user.owner_approval_status,
            User.OWNER_APPROVAL_NOT_REQUESTED,
        )

    def test_customer_can_choose_customer_role(self):
        response = self.client.post(
            "/api/register/",
            {
                "username": "customer",
                "email": "customer@example.com",
                "password": "password123",
                "role": "customer",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(username="customer")
        self.assertEqual(user.role, User.ROLE_CUSTOMER)
        self.assertEqual(
            user.owner_approval_status,
            User.OWNER_APPROVAL_NOT_REQUESTED,
        )

    def test_owner_registration_waits_for_superadmin_approval(self):
        response = self.client.post(
            "/api/register/",
            {
                "username": "owner",
                "email": "owner@example.com",
                "password": "password123",
                "role": "owner",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(username="owner")
        self.assertEqual(user.role, User.ROLE_OWNER)
        self.assertEqual(user.owner_approval_status, User.OWNER_APPROVAL_PENDING)

    def test_anonymous_role_can_be_selected_on_registration(self):
        response = self.client.post(
            "/api/register/",
            {
                "username": "anonymous-user",
                "email": "anon@example.com",
                "password": "password123",
                "role": "anonymous",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(username="anonymous-user")
        self.assertEqual(user.role, User.ROLE_ANONYMOUS)

    def test_dj_rest_auth_registration_accepts_role(self):
        response = self.client.post(
            "/api/auth/registration/",
            {
                "username": "dj-owner",
                "email": "dj-owner@example.com",
                "password1": "S9#ownerPassphrase2026",
                "password2": "S9#ownerPassphrase2026",
                "role": "owner",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(username="dj-owner")
        self.assertEqual(user.role, User.ROLE_OWNER)
        self.assertEqual(user.owner_approval_status, User.OWNER_APPROVAL_PENDING)

    def test_dj_rest_auth_registration_defaults_to_anonymous_without_role(self):
        response = self.client.post(
            "/api/auth/registration/",
            {
                "username": "dj-anonymous",
                "email": "dj-anonymous@example.com",
                "password1": "S9#anonymousPassphrase2026",
                "password2": "S9#anonymousPassphrase2026",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(username="dj-anonymous")
        self.assertEqual(user.role, User.ROLE_ANONYMOUS)
