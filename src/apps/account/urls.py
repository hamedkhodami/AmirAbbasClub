from django.urls import path

from . import views

app_name = "apps.account"

urlpatterns = [
    # User
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("login/", views.SimpleLoginView.as_view(), name="login"),
    # SuperUser
    path("all/athletes/", views.AthleteAllListView.as_view(), name="athlete_list_all"),
    path(
        "change-role/<uuid:pk>/",
        views.ChangeUserRoleView.as_view(),
        name="change_user_role",
    ),
    path("signup/coach/", views.CoachSignupView.as_view(), name="signup_coach"),
    # SuperUser And Coach
    path("signup/athlete/", views.AthleteSignupView.as_view(), name="signup_athlete"),
    path("athletes/", views.AthleteListView.as_view(), name="athlete_list"),
]
