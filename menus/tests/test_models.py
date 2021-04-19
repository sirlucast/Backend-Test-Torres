import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from menus.models import Dish, Meal, Menu


@pytest.mark.django_db
class ModelTests(TestCase):
    def setUp(self):
        username = "tony"
        password = "testPass123"
        self.user = get_user_model().objects.create_user(
            username=username,
            password=password,
        )
        self.dish = Dish.objects.create(name="Manzana")
        self.meal = Meal.objects.create(name="Veggy")
        self.menu = Menu.objects.create(menu_date=timezone.now().date(), user=self.user)
        self.menu.meals.add(self.meal)
        self.meal.dishes.add(self.dish)

    def test_menu_string_representation(self):
        """Test Menu entry’s string representation is formatted to :
        %d %b %Y
        """
        self.assertEqual(str(self.menu), self.menu.menu_date.strftime("%d %b %Y"))

    def test_dish_string_representation(self):
        """Test Dish entry’s string representation is name """
        self.assertEqual(str(self.dish), self.dish.name)

    def test_meal_string_representation(self):
        """Test Meal entry’s string representation is name """
        self.assertEqual(str(self.meal), self.meal.name)

    def test_meal_dish_relationship_exixst(self):
        """Test if m2m relationship between meal and dish exist"""
        self.meal.dishes.create(name="Pera")
        dish = Dish.objects.get(name="Pera")
        self.assertTrue(dish.meals.exists())
        self.assertTrue(self.meal.dishes.exists())

    def test_create_before_today_menu_date(self):
        """Test create/edit a menu with menu_date before today raises a
        validation error
        """
        menu = Menu.objects.create(
            menu_date=(timezone.now().date() - timezone.timedelta(days=2)),
            user=self.user,
        )
        self.assertRaises(ValidationError, menu.full_clean)

    def tearDown(self):
        self.user.delete()
        self.dish.delete()
        self.meal.delete()
        self.menu.delete()
