from apps.account.models import User
from apps.core.models import BaseModel
from apps.core.utils import to_shamsi_date
from django.db import models

from .enums import PaymentMonth, PaymentStatus


class PaymentModel(BaseModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name="ورزشکار",
        limit_choices_to={"role": "athlete"},
    )
    amount = models.PositiveIntegerField("مبلغ (تومان)")
    month_label = models.CharField(
        "ماه مربوطه",
        max_length=12,
        choices=PaymentMonth.choices,
    )
    status = models.CharField(
        "وضعیت",
        max_length=10,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PAID,
    )
    description = models.TextField("توضیحات", blank=True, null=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payments_created",
        verbose_name="ثبت‌کننده",
    )

    class Meta:
        verbose_name = "پرداخت"
        verbose_name_plural = "پرداخت‌ها"

    def __str__(self):
        return f"{self.user.full_name()} - {self.amount} تومان"

    def month_label_display(self):
        return self.get_month_label_display()

    def status_display(self):
        return self.get_status_display()

    def is_paid(self):
        return self.status == PaymentStatus.PAID

    def formatted_amount(self):
        return f"{self.amount:,} تومان"

    def created_at_shamsi(self):
        return to_shamsi_date(self.created_at)
