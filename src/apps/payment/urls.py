from django.urls import path

from . import views

app_name = "apps.payment"

urlpatterns = [
    path("create/<uuid:pk>/", views.PaymentCreateView.as_view(), name="payment_create"),
    path(
        "profile/<uuid:pk>/", views.PaymentProfileView.as_view(), name="payment_profile"
    ),
    path("income-summary/", views.IncomeSummaryView.as_view(), name="income_summary"),
    path(
        "income-summary/<str:month_label>/",
        views.MonthlyIncomeDetailView.as_view(),
        name="monthly_income_detail",
    ),
]
