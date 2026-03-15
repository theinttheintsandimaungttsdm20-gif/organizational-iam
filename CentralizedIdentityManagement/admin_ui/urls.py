from django.urls import path
from .views import *

urlpatterns = [
    path("", admin_login),
    path("dashboard/", dashboard, name="dashboard"),
    path("applications/", applications_view, name="applications"),
    path("applications/delete/<int:app_id>/", delete_app, name="delete_app"),
    path("users/", users_view),
    path("rolescope/", rolescope_view),
    path("session/", session_view),
]