import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from accounts.models import Employee


@pytest.mark.django_db
def test_create_employee_user_successful():
    """Test creating a new employee and getting
    his nationality, username and password as text
    """
    test_username = "test_user"
    test_password = "test_password"
    test_nationality_chilean = 0
    test_nationality_other = 1
    test_user = get_user_model().objects.create(
        username=test_username, password=make_password(test_password)
    )
    test_employee = Employee.objects.create(
        nationality=test_nationality_chilean, user=test_user
    )
    assert test_employee.nationality == Employee.CHILEAN
    assert test_nationality_other == Employee.OTHER
    assert test_employee.user.username == test_username
    assert test_employee.user.check_password(test_password)
    assert test_user.get_employee_profile() == test_employee
