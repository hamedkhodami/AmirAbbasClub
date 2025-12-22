import jdatetime
from apps.account import mixins
from apps.account.enums import UserRoleEnum
from apps.account.models import User
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, TemplateView

from .enums import PaymentMonth, PaymentStatus
from .forms import PaymentForm
from .models import PaymentModel


class PaymentCreateView(mixins.CoachOrSuperUserRequiredMixin, CreateView):
    model = PaymentModel
    form_class = PaymentForm
    template_name = "payment/payment_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.athlete = get_object_or_404(
            User, pk=kwargs["pk"], role=UserRoleEnum.ATHLETE
        )
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.athlete
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["athlete"] = self.athlete
        paid_months = self.athlete.payments.values_list("month_label", flat=True)
        context["paid_months"] = list(paid_months)
        return context

    def get_success_url(self):
        return reverse_lazy(
            "apps.payment:payment_profile", kwargs={"pk": self.athlete.pk}
        )


class PaymentProfileView(mixins.CoachOrSuperUserRequiredMixin, DetailView):
    model = User
    template_name = "payment/payment_profile.html"
    context_object_name = "athlete"
    pk_url_kwarg = "pk"

    def get_queryset(self):
        return User.objects.filter(role=UserRoleEnum.ATHLETE)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        athlete = self.object

        selected_year = self.request.GET.get("year")
        if selected_year is None:
            selected_year = str(jdatetime.date.today().year)
        context["selected_year"] = selected_year

        payments_by_month = {month[0]: None for month in PaymentMonth.choices}

        paid_payments = athlete.payments.filter(status=PaymentStatus.PAID)

        for payment in paid_payments:
            shamsi_year = jdatetime.date.fromgregorian(
                date=payment.created_at.date()
            ).year
            if (
                str(shamsi_year) == selected_year
                and not payments_by_month[payment.month_label]
            ):
                payments_by_month[payment.month_label] = payment

        context["payments_by_month"] = payments_by_month
        context["month_choices"] = PaymentMonth.choices

        context["year_choices"] = [str(y) for y in range(1404, 1430)]

        return context


class IncomeSummaryView(mixins.SuperUserRequiredMixin, TemplateView):
    template_name = "payment/income_summary.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        selected_year = self.request.GET.get("year")
        if selected_year is None:
            selected_year = str(jdatetime.date.today().year)

        context["selected_year"] = selected_year
        context["year_choices"] = [str(y) for y in range(1404, 1430)]
        context["month_choices"] = PaymentMonth.choices

        return context


class MonthlyIncomeDetailView(mixins.SuperUserRequiredMixin, TemplateView):
    template_name = "payment/monthly_income_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        month_label = self.kwargs["month_label"]
        year = self.request.GET.get("year")
        if year is None:
            year = str(jdatetime.date.today().year)

        all_payments = PaymentModel.objects.filter(
            month_label=month_label,
            status=PaymentStatus.PAID,
        )

        filtered_payments = []
        for p in all_payments:
            shamsi_year = jdatetime.date.fromgregorian(date=p.created_at.date()).year
            if str(shamsi_year) == year:
                filtered_payments.append(p)

        paginator = Paginator(filtered_payments, 20)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        total_income = sum(p.amount for p in filtered_payments)

        context.update(
            {
                "payments": page_obj,
                "month_label": dict(PaymentMonth.choices).get(month_label, month_label),
                "month_code": month_label,
                "selected_year": year,
                "total_income": total_income,
                "year_choices": [str(y) for y in range(1404, 1430)],
            }
        )
        return context
