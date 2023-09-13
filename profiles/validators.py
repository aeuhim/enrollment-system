from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from accounts.models import CustomUser


def validate_professor(pk):
    user = CustomUser.objects.get(Q(pk=pk))
    if not user.is_staff:
        raise ValidationError(_("User is not a staff."))


def validate_student(pk):
    user = CustomUser.objects.get(Q(pk=pk))
    if user.is_staff:
        raise ValidationError(_("User is a staff."))
