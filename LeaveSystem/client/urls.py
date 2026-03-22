from django.urls import path
from .views import (
    login_view,
    logout_view,
    apply_leave_view,
    leave_list_view,
    approve_leave_view
)

urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("leave/apply/", apply_leave_view, name="apply_leave"),
    path("leave/list/", leave_list_view, name="leave_list"),
    path("leave/approve/", approve_leave_view, name="approve_leave"),
]