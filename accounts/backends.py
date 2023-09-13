from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from accounts.models import CustomUser


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(CustomUser.USERNAME_FIELD)
        if username is None or password is None:
            return
        try:
            user = CustomUser.objects.get(Q(email__iexact=username))
        except CustomUser.DoesNotExist:
            CustomUser().set_password(password)
            return
        if user.check_password(password) and self.user_can_authenticate(user):
            return user


class ContactNumberBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(CustomUser.USERNAME_FIELD)
        if username is None or password is None:
            return
        try:
            user = CustomUser.objects.get(Q(contact_number__iexact=username))
        except CustomUser.DoesNotExist:
            CustomUser().set_password(password)
            return
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
