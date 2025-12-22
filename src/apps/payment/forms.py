from django import forms

from .enums import PaymentMonth, PaymentStatus
from .models import PaymentModel


class PaymentForm(forms.ModelForm):
    class Meta:
        model = PaymentModel
        fields = ["amount", "month_label", "status", "description"]
        widgets = {
            "month_label": forms.Select(choices=PaymentMonth.choices),
            "status": forms.Select(choices=PaymentStatus.choices),
            "description": forms.Textarea(attrs={"rows": 3}),
        }
        labels = {
            "amount": "مبلغ (تومان)",
            "month_label": "ماه مربوطه",
            "status": "وضعیت پرداخت",
            "description": "توضیحات",
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    def clean_month_label(self):
        month = self.cleaned_data["month_label"]
        if self.user and self.user.payments.filter(month_label=month).exists():
            raise forms.ValidationError(f"پرداخت برای ماه {month} قبلاً ثبت شده است.")
        return month
