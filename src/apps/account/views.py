from django.contrib.auth import login
from django.contrib.auth.views import FormView
from django.shortcuts import redirect
from django.urls import reverse_lazy

from . import mixins
from .forms import AthleteSignupForm, CoachSignupForm, LoginForm


class SimpleLoginView(
    FormView, mixins.LogoutRequiredMixin, mixins.CoachOrSuperUserRequiredMixin
):
    template_name = "account/login.html"
    form_class = LoginForm

    def form_valid(self, form):
        user = form.cleaned_data["user"]
        login(self.request, user)
        return redirect("home")


class AthleteSignupView(FormView, mixins.CoachOrSuperUserRequiredMixin):
    template_name = "account/signup_athlete.html"
    form_class = AthleteSignupForm
    success_url = reverse_lazy("apps.account:login")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class CoachSignupView(FormView, mixins.SuperUserRequiredMixin):
    template_name = "account/coach_athlete.html"
    form_class = CoachSignupForm
    success_url = reverse_lazy("apps.account:login")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
