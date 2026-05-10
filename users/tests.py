from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()

# testing register role
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


class UserRoleEndpointTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="role-user",
            email="role-user@example.com",
            password="password123",
            role=User.ROLE_ANONYMOUS,
        )
        self.admin = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="password123",
        )

    def test_authenticated_anonymous_role_user_can_change_to_customer(self):
        self.client.force_authenticate(self.user)

        response = self.client.patch(
            "/api/users/me/role/",
            {"role": "customer"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()
        self.assertEqual(self.user.role, User.ROLE_CUSTOMER)
        self.assertEqual(
            self.user.owner_approval_status,
            User.OWNER_APPROVAL_NOT_REQUESTED,
        )

    def test_changing_to_owner_creates_pending_owner_request(self):
        self.client.force_authenticate(self.user)

        response = self.client.patch(
            "/api/users/me/role/",
            {"role": "owner"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()
        self.assertEqual(self.user.role, User.ROLE_OWNER)
        self.assertEqual(self.user.owner_approval_status, User.OWNER_APPROVAL_PENDING)

    def test_non_admin_cannot_list_all_users(self):
        self.client.force_authenticate(self.user)

        response = self.client.get("/api/users/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_list_all_users(self):
        self.client.force_authenticate(self.admin)

        response = self.client.get("/api/users/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data["results"]), 2)
