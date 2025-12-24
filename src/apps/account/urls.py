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
        "user/<uuid:pk>/promote-to-coach/",
        views.PromoteToCoachView.as_view(),
        name="promote_to_coach",
    ),
    path(
        "change-role/<uuid:pk>/",
        views.ChangeUserRoleView.as_view(),
        name="change_user_role",
    ),
    path("signup/coach/", views.CoachSignupView.as_view(), name="signup_coach"),
    path(
        "payment-days-all/",
        views.AllPaymentDayListView.as_view(),
        name="payment_day_list_all",
    ),
    path(
        "payment-day-all/<int:day>/athletes/",
        views.AllAthletesByPaymentDayView.as_view(),
        name="payment_day_all_users",
    ),
    # SuperUser And Coach
    path("signup/athlete/", views.AthleteSignupView.as_view(), name="signup_athlete"),
    path("athletes/", views.AthleteListView.as_view(), name="athlete_list"),
    path("payment-days/", views.PaymentDayListView.as_view(), name="payment_day_list"),
    path(
        "payment-day/<int:day>/athletes/",
        views.AthletesByPaymentDayView.as_view(),
        name="payment_day_users",
    ),
]
