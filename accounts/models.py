from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

""" Validators """


class User(
    AbstractUser,
):
    """Custom user model that supports using some extra field (in future)"""

    pass


class Employee(models.Model):
    CHILEAN = 0
    OTHER = 1
    NATIONALITY = {
        CHILEAN: _("Chilean"),
        OTHER: _("Other than Chilean"),
    }

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="employee",
    )
    nationality = models.SmallIntegerField(
        default=CHILEAN,
        choices=NATIONALITY.items(),
        verbose_name=_("Employee nationality"),
    )
    slack_user = models.CharField(max_length=250, blank=True)

    class Meta:
        verbose_name = _("Employee")
        verbose_name_plural = _("Employees")

    def get_nationality(self):
        return self.NATIONALITY[self.nationality]
