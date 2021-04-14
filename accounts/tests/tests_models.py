from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.models import Employee


class ModelTests(TestCase):
    def setUp(self):
        self.nationality = 1
        self.username = "test_username"
        self.password = "testPass123"
        self.test_user = get_user_model().objects.create_user(
            username=self.username,
            password=self.password,
        )
        self.test_employee = Employee.objects.create(
            nationality=self.nationality, user=self.test_user
        )

    def test_create_employee_user_successful(self):
        """Test creating a new employee and getting
        his nationality as text
        """

        self.assertEqual(self.test_employee.user.username, self.username)
        self.assertTrue(
            self.test_employee.user.check_password(self.password), self.password
        )
        self.assertAlmostEqual(self.test_employee.nationality, self.nationality)
        self.assertEqual(
            self.test_employee.get_nationality(),
            self.test_employee.NATIONALITY[self.nationality],
        )

    def tearDown(self):
        self.test_user.delete()
        self.test_employee.delete()
