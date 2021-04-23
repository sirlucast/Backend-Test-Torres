from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from accounts.serializers import EmployeeSerializer, UserSerializer
from menus.models import Dish, Meal, Menu, Order, validate_menu_date

LIMIT_HOUR = 11  # Deadline to choose meal on daily order.


class DishSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S", read_only=True)

    class Meta:
        model = Dish
        fields = (
            "id",
            "name",
            "created_at",
        )


class MealSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S", read_only=True)

    class Meta:
        model = Meal
        fields = (
            "id",
            "name",
            "dishes",
            "created_at",
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["dishes"] = DishSerializer(instance.dishes, many=True).data
        return representation


class MenuSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S", read_only=True)
    menu_date = serializers.DateField(
        format="%d-%m-%Y", validators=[validate_menu_date]
    )
    user = UserSerializer(default=serializers.CurrentUserDefault())

    class Meta:
        model = Menu
        fields = (
            "id",
            "menu_date",
            "meals",
            "uuid",
            "user",
            "created_at",
        )
        extra_kwarks = {"uuid": {"read_only": True}}
        validators = [
            serializers.UniqueForDateValidator(
                queryset=Menu.objects.all(), field="menu_date", date_field="menu_date"
            ),
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["meals"] = MealSerializer(instance.meals, many=True).data
        return representation


class OrderSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S", read_only=True)
    employee = EmployeeSerializer(read_only=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "customization",
            "meal",
            "employee",
            "created_at",
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["meal"] = MealSerializer(instance.meal).data
        # representation["employee"] = EmployeeSerializer(instance.employee).data
        return representation

    def validate_meal(self, value):
        if timezone.localtime(timezone.now()).hour > LIMIT_HOUR:
            raise serializers.ValidationError(
                _("Exceeded meal selection time. Limit hour:") + f" {LIMIT_HOUR}"
            )
        if value not in Meal.objects.filter(
            menus__menu_date=timezone.localtime(timezone.now()).date()
        ):
            raise serializers.ValidationError(_("Invalid meal for todays's menu"))
        return value

    def create(self, validated_data):
        employee = self.context.get("request").user.employee
        return Order.objects.create(employee=employee, **validated_data)
