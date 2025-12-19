import secrets

from apps.core import text
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.db.models import Count, Q, Value
from django.db.models.functions import Concat

from .enums import UserRoleEnum


class CustomQuerySet(models.QuerySet):

    def search(self, value):
        if not value:
            return self
        qs = self.annotate(full_name=Concat("first_name", Value(" "), "last_name"))
        lookup = Q(phone_number=value) | Q(full_name__icontains=value)
        return qs.filter(lookup)

    def random(self):
        count = self.aggregate(count=Count("id"))["count"]
        if count == 0:
            return None
        return self.order_by("?").first()


class CustomObjectsManager(BaseUserManager):
    _queryset_class = CustomQuerySet

    def create_user(
        self,
        phone_number,
        password,
        role=UserRoleEnum.ATHLETE,
        **extra_fields,
    ):
        if not phone_number:
            raise ValueError(text.required_phone_number)
        user = self.model(phone_number=phone_number, role=role, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)

        if "national_id" not in extra_fields:
            extra_fields["national_id"] = secrets.token_hex(5)

        return self.create_user(
            phone_number=phone_number,
            password=password,
            role=UserRoleEnum.SUPER_USER,
            **extra_fields,
        )
