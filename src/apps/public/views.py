from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

User = get_user_model()


class Home(LoginRequiredMixin, TemplateView):
    template_name = "public/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_superuser:
            role = "superuser"
        elif hasattr(user, "role"):
            role = user.role
        else:
            role = "unknown"

        context["role"] = role
        return context
