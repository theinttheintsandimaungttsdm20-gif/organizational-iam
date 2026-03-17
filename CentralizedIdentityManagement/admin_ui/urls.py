from django.urls import path
from .views import *

urlpatterns = [
    path("", admin_login),
    path("dashboard/", dashboard, name="dashboard"),

    path("applications/", applications_view, name="applications"),
    path("applications/delete/<int:app_id>/", delete_app, name="delete_app"),

    path("employees/", employees_view, name="employees"),
    path("employees/<int:emp_id>/", edit_employee, name="edit_employee"),
    path("employees/<int:emp_id>/", delete_employee, name="delete_employee"),

    path("settings/", settings_view, name="settings"),
    path("roles/create/", create_role_view),
    path("roles/delete/<int:role_id>/", delete_role_view),
    path("scopes/create/", create_scope_view),
    path("scopes/delete/<int:scope_id>/", delete_scope_view),
    path("role-scopes/create/", create_role_scope_view),
    path("role-scopes/delete/<int:rs_id>/", delete_role_scope_view),

    path("session/", session_view),
]