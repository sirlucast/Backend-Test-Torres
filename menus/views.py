from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from menus.models import Dish, Meal, Menu, Order
from menus.serializers import (
    DishSerializer,
    MealSerializer,
    MenuSerializer,
    OrderSerializer,
)


class DishViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Dish.objects.all().order_by("-created_at")
    serializer_class = DishSerializer


class MealViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Meal.objects.all().order_by("-created_at")
    serializer_class = MealSerializer


class MenuViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Menu.objects.all().order_by("-created_at")
    serializer_class = MenuSerializer


class OrderViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all().order_by("-created_at")
    serializer_class = OrderSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all().order_by("-created_at")
        employee = self.request.user.get_employee_profile()
        if employee:
            return Order.objects.filter(employee=employee).order_by("-created_at")
        return super().get_queryset()
