from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import FormView
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, RedirectView

from . import mixins
from .enums import UserRoleEnum
from .forms import AthleteSignupForm, CoachSignupForm, LoginForm
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
    paginate_by = 20

    def get_queryset(self):
        query = self.request.GET.get("q", "")
        base_qs = User.objects.all()
        if query:
            base_qs = base_qs.filter(
                Q(first_name__icontains=query) | Q(last_name__icontains=query)
            )

        return base_qs.order_by("first_name")


class ChangeUserRoleView(mixins.SuperUserRequiredMixin, View):
    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)

        if user.role == UserRoleEnum.SUPER_USER:
            raise PermissionDenied("نمی‌توان نقش ابرکاربر را تغییر داد.")

        if user.role == UserRoleEnum.ATHLETE:
            user.role = UserRoleEnum.COACH
            messages.success(request, f"نقش {user.full_name()} به مربی تغییر یافت.")
        else:
            user.role = UserRoleEnum.ATHLETE
            messages.success(request, f"نقش {user.full_name()} به ورزشکار تغییر یافت.")

        user.save()
        return redirect("apps.account:athlete_list_all")


class CoachSignupView(mixins.SuperUserRequiredMixin, FormView):
    template_name = "account/coach_athlete.html"
    form_class = CoachSignupForm
    success_url = reverse_lazy("apps.account:login")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


# ---------------------------------------------------------------


# ---SuperUser And Coach-----------------------------------------
class AthleteListView(mixins.CoachOrSuperUserRequiredMixin, ListView):
    template_name = "account/athlete_list.html"
    context_object_name = "athletes"
    paginate_by = 20

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


# ---------------------------------------------------------------
