from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


# Create your models here.
class CustomUser(AbstractUser):
    first_name = models.CharField(_("first name"), max_length=32)
    middle_name = models.CharField(_("middle name"), max_length=16, blank=True)
    last_name = models.CharField(_("last name"), max_length=16)
    name_suffix = models.CharField(_("name suffix"), max_length=8, blank=True)
    email = models.EmailField(_("email address"), unique=True)
    contact_number = models.CharField(_("contact number"), max_length=(16), unique=True)
    permanent_address = models.CharField(_("permanent address"), max_length=128)
    current_address = models.CharField(_("current address"), max_length=128)
    emergency_number = models.CharField(_("emergency contact number"), max_length=16)

    def __str__(self):
        return " ".join([self.first_name, self.middle_name, self.last_name])
