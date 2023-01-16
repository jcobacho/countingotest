from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models

# Create your models here.
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.utils.translation import ugettext_lazy as _


def has11digits(value):
    if value.isdigit() == False:
        raise ValidationError(_("Must provide only digits"))
    if len(value) != 11:
        raise ValidationError(_("Must provide 11 digits"))


class User(AbstractUser):
    SEX_CHOICES = (
        ('m', 'MALE'),
        ('F', 'FEMALE'),
    )

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[AbstractUser.username_validator],
        null=True,
        blank=True,
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    first_name = models.CharField(max_length=150)
    middle_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150)

    ci = models.CharField(max_length=11, unique=True, null=True, validators=[has11digits])
    address = models.TextField(null=True)
    age = models.PositiveSmallIntegerField(null=True, validators=[MinValueValidator(18)])
    sex = models.CharField(choices=SEX_CHOICES, max_length=6, null=True)

    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.username or self.get_full_name()

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s %s' % (self.first_name, self.middle_name, self.last_name)
        return full_name.strip()