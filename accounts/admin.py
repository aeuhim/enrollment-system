from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser


# Register your models here.
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "email", "contact_number", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "middle_name",
                    "last_name",
                    "name_suffix",
                    "permanent_address",
                    "current_address",
                    "emergency_number",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            _("Login credentials"),
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "contact_number",
                    "password1",
                    "password2",
                ),
            },
        ),
        (
            _("Personal info"),
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "middle_name",
                    "last_name",
                    "name_suffix",
                    "permanent_address",
                    "current_address",
                    "emergency_number",
                ),
            },
        ),
        (
            _("Permissions"),
            {
                "classes": ("wide",),
                "fields": (
                    "is_active",
                    "is_staff",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
    list_display = (
        "username",
        "last_name",
        "first_name",
        "is_staff",
        "email",
        "contact_number",
        "permanent_address",
        "current_address",
        "emergency_number",
    )
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = (
        "username",
        "last_name",
        "first_name",
        "email",
        "contact_number",
        "permanent_address",
        "current_address",
        "emergency_number",
    )
    ordering = ("last_name", "first_name", "username")


admin.site.register(CustomUser, CustomUserAdmin)
