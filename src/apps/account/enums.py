from django.db.models import TextChoices


class UserRoleEnum(TextChoices):
    SUPER_USER = "super_user", "ابرکاربر"
    COACH = "coach", "مربی"
    ATHLETE = "athlete", "ورزشکار"


class UserGenderEnum(TextChoices):

    MALE = "m", "مرد"
    FEMALE = "f", "زن"
