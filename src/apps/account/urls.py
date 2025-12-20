from django.urls import path

from . import views

app_name = "apps.account"

urlpatterns = [
    path("login/", views.SimpleLoginView.as_view(), name="login"),
    path("signup/athlete/", views.AthleteSignupView.as_view(), name="signup_athlete"),
    path("signup/coach/", views.CoachSignupView.as_view(), name="signup_coach"),
]
