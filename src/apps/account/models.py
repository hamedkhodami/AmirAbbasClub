from apps.core.models import BaseModel
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import (
    MaxLengthValidator,
    MaxValueValidator,
    MinLengthValidator,
    MinValueValidator,
)
from django.db import models

from .enums import UserGenderEnum, UserRoleEnum
from .manager import CustomObjectsManager


class User(BaseModel, AbstractBaseUser, PermissionsMixin):

    Role = UserRoleEnum
    Gender = UserGenderEnum

    phone_number = models.CharField("شماره تماس", max_length=15, unique=True)
    first_name = models.CharField(
        "نام",
        max_length=128,
        null=True,
        blank=True,
        default="بدون اسم",
    )
    last_name = models.CharField(
        "نام خانوادگی",
        max_length=128,
        null=True,
        blank=True,
        default="بدون اسم",
    )
    role = models.CharField(
        "نقش", max_length=20, choices=Role.choices, default=Role.ATHLETE
    )
    gender = models.CharField(
        "جنسیت", max_length=10, choices=Gender.choices, null=True, blank=True
    )
    payment_day = models.PositiveSmallIntegerField(
        "روز پرداخت شهریه",
        validators=[MinValueValidator(1), MaxValueValidator(30)],
    )
    national_id = models.CharField(
        "کد ملی",
        max_length=11,
        unique=True,
        validators=[MinLengthValidator(9), MaxLengthValidator(11)],
    )
    image = models.ImageField(
        "تصویر", upload_to="images/profiles/", null=True, blank=True
    )

    is_active = models.BooleanField("فعال", default=True)
    is_superuser = models.BooleanField("ابرکاربر", default=False)
    is_staff = models.BooleanField("کارمند", default=False)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    objects = CustomObjectsManager()

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.phone_number}"

    def full_name(self):
        return f"{self.first_name or ''} {self.last_name or ''}".strip() or "بدون اسم"

    def has_role(self, role_enum):
        return self.role == role_enum

    def get_full_name(self):
        return self.full_name()

    def get_short_name(self):
        return self.first_name or "بدون نام"
