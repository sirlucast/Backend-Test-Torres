import os
import uuid

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from accounts.models import Employee
from menus import helpers


def validate_menu_date(value):
    """ If a value (Date) is before today, raises an Error"""
    if value < timezone.localtime(timezone.now()).date():
        raise ValidationError(
            _("date '%(value)s' is not valid. choose a later date or equal to today "),
            params={"value": value},
        )


class Dish(models.Model):
    """ Model of dish """

    name = models.CharField(max_length=250, verbose_name=_("Dish's name"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Date"))

    class Meta:
        verbose_name = _("Dish")
        verbose_name_plural = _("Dishes")

    def __str__(self):
        return self.name


class Meal(models.Model):
    """Meal that a menu could have"""

    name = models.CharField(max_length=250, verbose_name=_("Meal's name"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Date"))
    dishes = models.ManyToManyField(Dish, related_name="meals", blank=True)

    class Meta:
        verbose_name = _("Meal option")
        verbose_name_plural = _("Meal options")

    def __str__(self):
        return self.name


class Menu(models.Model):
    """Menu's model"""

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Date"))
    menu_date = models.DateField(
        verbose_name=_("Menu's date"),
        validators=[validate_menu_date],
        unique=True,
    )
    uuid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
        verbose_name=_("UUID"),
    )
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="menus",
    )
    meals = models.ManyToManyField(Meal, related_name="menus", blank=True)

    class Meta:
        verbose_name = _("Menu")
        verbose_name_plural = _("Menus")
        ordering = ["-created_at"]

    def __str__(self):
        return self.menu_date.strftime("%d %b %Y")

    def send_today_menu_slack_each_user(self):
        """Send today's menu to each chilean employee using attachment
        slack message
        """
        employees = Employee.objects.filter(nationality=Employee.CHILEAN)
        url = os.getenv("DOMAIN_NAME")
        meal_option = ""
        for idx, meal in enumerate(self.meals.all()):
            dish_count = meal.dish.all().count()
            dishes = ""
            for jdx, dish in enumerate(meal.dish.all()):
                if dish_count == 1:
                    dishes += f"{dish.name}."
                elif jdx < dish_count - 2:
                    dishes += f"{dish.name}, "
                elif jdx < dish_count - 1:
                    dishes += f"{dish.name} "
                else:
                    dishes += f"y {dish.name}."
            meal_option += f"- Option {idx+1}: {dishes}\n"
        for employee in employees:
            # message = f"Hi!\nRemind you can choose a meal option for lunch"
            # +"from today's Nora's menu.\n here: {self.uuid}"
            attachment = [
                {
                    "color": "#36a64f",
                    "title": "Menú del día aqui!",
                    "title_link": f"{url}/menu/{self.uuid}",
                    "text": "Hola!\nDejo el menú de hoy: :smile:\n"
                    + f"\n{meal_option}\nTambien puedes ver el menú de hoy aqui:"
                    + f"\n{url}/menu/{self.uuid}\nTengan lindo día!",
                    "footer": "Nora's app",
                    "footer_icon": "https://platform.slack-edge.com/img/defau"
                    + "lt_application_icon.png",
                }
            ]
            helpers.post_to_user_slack(employee.slack_user, attachment=attachment)

    @staticmethod
    def check_todays_menu_is_created():
        menu_today, created = Menu.objects.get_or_create(
            menu_date=timezone.localtime(timezone.now()).date()
        )
        if created:
            menu_today.send_today_menu_slack_each_user()


class Order(models.Model):
    """Order's model"""

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Date"))
    customization = models.CharField(
        max_length=250, verbose_name=_("Specify customizations")
    )
    meal = models.ForeignKey(Meal, related_name="orders", on_delete=models.CASCADE)
    employee = models.ForeignKey(
        Employee, related_name="orders", on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
