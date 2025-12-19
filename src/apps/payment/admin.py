from django.contrib import admin

from .models import PaymentModel


@admin.register(PaymentModel)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "user_full_name",
        "user_phone",
        "formatted_amount",
        "month_label",
        "paid_at_shamsi",
        "status_display",
    )
    list_filter = ("month_label", "status", "paid_at")
    search_fields = ("user__first_name", "user__last_name", "user__phone_number")
    ordering = ("-paid_at",)

    @admin.display(description="نام ورزشکار")
    def user_full_name(self, obj):
        return obj.user.full_name()

    @admin.display(description="شماره تماس")
    def user_phone(self, obj):
        return obj.user.phone_number

    @admin.display(description="مبلغ")
    def formatted_amount(self, obj):
        return f"{obj.amount:,} تومان"

    @admin.display(description="تاریخ پرداخت (شمسی)")
    def paid_at_shamsi(self, obj):
        return obj.paid_at_shamsi()

    @admin.display(description="وضعیت")
    def status_display(self, obj):
        return obj.get_status_display()
