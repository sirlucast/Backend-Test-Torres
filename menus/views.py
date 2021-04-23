from django.utils import timezone
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

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

    @action(detail=False, methods=["get"])
    def send_today_reminder(self, request, pk=None):
        """Triggers asynchronous sending of messages
        with menu of the day reminder to all Slack User ID
        of chilean employees
        """
        try:
            today_menu = Menu.objects.get(
                menu_date=timezone.localtime(timezone.now()).date()
            )
            today_menu.send_today_menu_slack_each_user()
        except Menu.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(
            {"detail": "Reminder sent successfully."}, status=status.HTTP_200_OK
        )


class MenuPublicViewSet(
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [IsAuthenticated]
    queryset = Menu.objects.filter(menu_date=timezone.localtime(timezone.now()).date())
    serializer_class = MenuSerializer
    lookup_field = "uuid"


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
