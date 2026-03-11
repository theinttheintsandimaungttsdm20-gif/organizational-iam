from django.urls import path
from .views import login_view, submit_view, report_view, logout_view

urlpatterns = [
    path("login/", login_view, name="login"),
    path("submit/", submit_view, name="submit"),
    path("reports/", report_view, name="reports"),
    path("logout/", logout_view, name="logout"),
]
