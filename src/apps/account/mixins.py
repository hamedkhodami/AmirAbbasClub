from apps.core import text
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

from .enums import UserRoleEnum


class LogoutRequiredMixin:

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/")

        return super().dispatch(request, *args, **kwargs)


class RoleRequiredMixin(LoginRequiredMixin):
    allowed_roles = []

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and user.role in self.allowed_roles:
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied(text.permission_denied)


class CoachOrSuperUserRequiredMixin(LoginRequiredMixin):
    allowed_roles = [UserRoleEnum.COACH, UserRoleEnum.SUPER_USER]


class SuperUserRequiredMixin(LoginRequiredMixin):
    allowed_roles = [UserRoleEnum.SUPER_USER]
