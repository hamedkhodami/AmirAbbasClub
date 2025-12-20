from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from . import models
from .forms import CustomUserChangeForm, CustomUserCreationForm


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    model = models.User

    list_display = ("phone_number", "is_active", "last_login", "role")
    list_filter = ("is_active", "role", "first_name", "last_name")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "phone_number",
                    "password",
                    "role",
                    "gender",
                    "national_id",
                    "image",
                    "first_name",
                    "last_name",
                )
            },
        ),
        (
            "Permissions",
            {"fields": ("is_active",)},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "phone_number",
                    "password1",
                    "password2",
                    "is_active",
                    "first_name",
                    "last_name",
                    "national_id",
                    "role",
                    "gender",
                    "image",
                ),
            },
        ),
    )
    search_fields = ("phone_number",)
    ordering = ("phone_number",)
    filter_horizontal = ()


admin.site.register(models.User, CustomUserAdmin)
