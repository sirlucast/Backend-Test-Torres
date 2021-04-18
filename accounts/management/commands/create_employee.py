from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from accounts.models import Employee
from accounts.serializers import EmployeeSerializer
from backend_test import settings


class Command(BaseCommand):

    help = """Create a new user and their employee profile.
        It is necessary to indicate the slack user ID """
    requires_migrations_checks = True

    def add_arguments(self, parser):
        parser.add_argument(
            "slack_user",
            type=str,
            help="Indicates the slack user ID of user to be created",
        )

    def handle(self, *args, **kwargs):
        slack_user = kwargs["slack_user"]
        if get_user_model().objects.last() is None:
            last_id = 0
        else:
            last_id = get_user_model().objects.last().id
        username = f"{settings.EMPLOYEE_USERNAME}_{last_id+1}"
        password = f"{settings.EMPLOYEE_PASSWORD}_{last_id+1}"
        user = get_user_model().objects.create_user(
            username=username, email="", password=password
        )
        emp = Employee.objects.create(user=user, slack_user=slack_user)
        print(EmployeeSerializer(emp).data)
