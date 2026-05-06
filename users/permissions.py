from rest_framework.permissions import SAFE_METHODS, BasePermission


def get_user_role(user):
    if not user or not user.is_authenticated:
        return "anonymous"

    if getattr(user, "role", "customer") == "owner":
        if getattr(user, "is_approved_owner", False):
            return "owner"
        return "customer"

    return getattr(user, "role", "customer")


class GlobalRolePermission(BasePermission):
    """
    Baseline API permission:
    - anonymous users may read safe endpoints
    - authenticated users may use non-safe endpoints
    - staff/superusers bypass role checks
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        if not request.user or not request.user.is_authenticated:
            return False

        return get_user_role(request.user) != "anonymous"


class IsOwnerRoleOrReadOnly(BasePermission):
    """Catalog writes are reserved for owner role users."""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        user = request.user
        if not user or not user.is_authenticated:
            return False

        return bool(
            user.is_staff
            or user.is_superuser
            or get_user_role(user) == "owner"
        )


class IsCustomerRole(BasePermission):
    """Customers can place orders; owners/staff can manage order data."""

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        if user.is_staff or user.is_superuser:
            return True

        return get_user_role(user) in {"customer", "owner"}


class IsOrderOwnerOrOwnerRole(BasePermission):
    """Customers can access their own orders; owners/staff can access all."""

    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        if user.is_staff or user.is_superuser or get_user_role(user) == "owner":
            return True

        return obj.customer_id == user.id
