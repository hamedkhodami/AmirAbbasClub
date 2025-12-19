from django.db.models import TextChoices


class PaymentStatus(TextChoices):
    PAID = "paid", "پرداخت شده"
    DUE = "due", "بدهکار"


class PaymentMonth(TextChoices):
    FARVARDIN = "farvardin", "فروردین"
    ORDIBEHESHT = "ordibehesht", "اردیبهشت"
    KHORDAD = "khordad", "خرداد"
    TIR = "tir", "تیر"
    MORDAD = "mordad", "مرداد"
    SHAHRIVAR = "shahrivar", "شهریور"
    MEHR = "mehr", "مهر"
    ABAN = "aban", "آبان"
    AZAR = "azar", "آذر"
    DEY = "dey", "دی"
    BAHMAN = "bahman", "بهمن"
    ESFAND = "esfand", "اسفند"
