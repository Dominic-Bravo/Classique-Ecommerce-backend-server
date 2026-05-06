from rest_framework import generics

from users.permissions import IsCustomerRole, IsOrderOwnerOrOwnerRole, get_user_role
from .models import Order
from .serializers import OrderCreateSerializer, OrderSerializer


class OrderListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsCustomerRole]

    def get_queryset(self):
        queryset = Order.objects.prefetch_related("items__product__category")
        user = self.request.user
        if user.is_staff or user.is_superuser or get_user_role(user) == "owner":
            return queryset
        return queryset.filter(customer=user)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return OrderCreateSerializer
        return OrderSerializer


class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsCustomerRole, IsOrderOwnerOrOwnerRole]

    def get_queryset(self):
        return Order.objects.prefetch_related("items__product__category")
