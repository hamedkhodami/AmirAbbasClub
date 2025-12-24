from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import FormView
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, RedirectView, TemplateView

from . import mixins
from .enums import UserRoleEnum
from .forms import AthleteSignupForm, CoachSignupForm, LoginForm, PromoteToCoachForm
from .models import User


# ---User------------------------------------------------------
class SimpleLoginView(mixins.LogoutRequiredMixin, FormView):
    template_name = "account/login.html"
    form_class = LoginForm

    def form_valid(self, form):
        user = form.cleaned_data["user"]
        login(self.request, user)
        return redirect("public:home")


class LogoutView(LoginRequiredMixin, RedirectView):

    url = reverse_lazy("account:login")

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "شما با موفقیت خارج شدین.")
        return super().get(request, *args, **kwargs)


# ---------------------------------------------------------------


# ---SuperUser---------------------------------------------------
class AthleteAllListView(mixins.SuperUserRequiredMixin, ListView):
    template_name = "account/all_user.html"
    context_object_name = "athletes"
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get("q", "")
        base_qs = User.objects.filter(
            role__in=[UserRoleEnum.ATHLETE, UserRoleEnum.COACH]
        )

        if query:
            base_qs = base_qs.filter(
                Q(first_name__icontains=query) | Q(last_name__icontains=query)
            )

        return base_qs.order_by("first_name")


class PromoteToCoachView(mixins.SuperUserRequiredMixin, FormView):
    template_name = "account/promote_to_coach.html"
    form_class = PromoteToCoachForm

    def dispatch(self, request, *args, **kwargs):
        self.user_obj = get_object_or_404(User, pk=kwargs["pk"])
        if self.user_obj.role != UserRoleEnum.ATHLETE:
            raise PermissionDenied("فقط ورزشکار را می‌توان به مربی ارتقا داد.")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        password = form.cleaned_data["password"]
        self.user_obj.role = UserRoleEnum.COACH
        self.user_obj.password = make_password(password)
        self.user_obj.is_active = True
        self.user_obj.save()
        messages.success(
            self.request, f"نقش {self.user_obj.full_name()} به مربی تغییر یافت."
        )
        return redirect("apps.account:athlete_list_all")


class ChangeUserRoleView(mixins.SuperUserRequiredMixin, View):
    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)

        if user.role == UserRoleEnum.SUPER_USER:
            raise PermissionDenied("نمی‌توان نقش ابرکاربر را تغییر داد.")

        if user.role == UserRoleEnum.ATHLETE:
            return redirect("apps.account:promote_to_coach", pk=user.pk)

        else:
            user.role = UserRoleEnum.ATHLETE
            user.set_unusable_password()
            user.is_active = False
            user.save()
            messages.success(request, f"نقش {user.full_name()} به ورزشکار تغییر یافت.")
            return redirect("apps.account:athlete_list_all")


class CoachSignupView(mixins.SuperUserRequiredMixin, FormView):
    template_name = "account/signup_coach.html"
    form_class = CoachSignupForm
    success_url = reverse_lazy("apps.account:login")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class AllPaymentDayListView(mixins.SuperUserRequiredMixin, TemplateView):
    template_name = "account/all_users_payment.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["days"] = list(range(1, 31))
        return context


class AllAthletesByPaymentDayView(mixins.SuperUserRequiredMixin, ListView):
    template_name = "account/all_user_list_by_day.html"
    context_object_name = "athletes"
    paginate_by = 5

    def get_queryset(self):
        day = self.kwargs.get("day")
        query = self.request.GET.get("q", "")
        qs = User.objects.filter(payment_day=day)
        if query:
            qs = qs.filter(
                Q(first_name__icontains=query) | Q(last_name__icontains=query)
            )
        return qs.order_by("first_name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["selected_day"] = self.kwargs.get("day")
        return context


# ---------------------------------------------------------------


# ---SuperUser And Coach-----------------------------------------
class AthleteListView(mixins.CoachOrSuperUserRequiredMixin, ListView):
    template_name = "account/athlete_list.html"
    context_object_name = "athletes"
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get("q", "")
        user = self.request.user

        base_qs = User.objects.filter(role=UserRoleEnum.ATHLETE, gender=user.gender)

        if query:
            base_qs = base_qs.filter(
                Q(first_name__icontains=query) | Q(last_name__icontains=query)
            )

        return base_qs.order_by("first_name")


class AthleteSignupView(mixins.CoachOrSuperUserRequiredMixin, FormView):
    template_name = "account/signup_athlete.html"
    form_class = AthleteSignupForm
    success_url = reverse_lazy("apps.account:login")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class PaymentDayListView(mixins.CoachOrSuperUserRequiredMixin, TemplateView):
    template_name = "account/payment_day_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["days"] = list(range(1, 31))
        return context


class AthletesByPaymentDayView(mixins.CoachOrSuperUserRequiredMixin, ListView):
    template_name = "account/athlete_list_by_day.html"
    context_object_name = "athletes"
    paginate_by = 5

    def get_queryset(self):
        day = self.kwargs.get("day")
        user = self.request.user
        query = self.request.GET.get("q", "")

        qs = User.objects.filter(
            role=UserRoleEnum.ATHLETE, gender=user.gender, payment_day=day
        )

        if query:
            qs = qs.filter(
                Q(first_name__icontains=query) | Q(last_name__icontains=query)
            )

        return qs.order_by("first_name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["selected_day"] = self.kwargs.get("day")
        return context


# ---------------------------------------------------------------
