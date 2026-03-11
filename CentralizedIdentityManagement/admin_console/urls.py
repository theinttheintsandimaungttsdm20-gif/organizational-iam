from django.urls import path
from .views import (
    AdminLoginView,
    EmployeeListCreateView,
    EmployeeRoleUpdateView,
    RoleScopeUpdateView,
    SessionPolicyUpdateView,
    ApplicationAccessMatrixView
)

urlpatterns = [
    path("auth/login/", AdminLoginView.as_view(), name="admin-login"),
    path("employees/", EmployeeListCreateView.as_view()),
    path("applications/<str:client_id>/access-matrix/", ApplicationAccessMatrixView.as_view()),
    path("employees/<int:user_id>/role/", EmployeeRoleUpdateView.as_view()),
    path("applications/role-scopes/", RoleScopeUpdateView.as_view()),
    path("applications/session-policy/", SessionPolicyUpdateView.as_view()),
]