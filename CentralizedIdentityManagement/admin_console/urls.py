from django.urls import path
from .views import (
    AdminLoginView,
    EmployeeListCreateView,
    EmployeeDetailView,
    RoleScopeUpdateView,
    SessionPolicyUpdateView,
    ApplicationAccessMatrixView,
    ApplicationListCreateView,
    RoleListCreateView
)

urlpatterns = [
    path("auth/login/", AdminLoginView.as_view(), name="admin-login"),

    path("applications/", ApplicationListCreateView.as_view()),
    path("applications/role-scopes/", RoleScopeUpdateView.as_view()),
    path("applications/session-policy/", SessionPolicyUpdateView.as_view()),
    path("applications/<str:client_id>/access-matrix/", ApplicationAccessMatrixView.as_view()),
    
    path("roles/", RoleListCreateView.as_view()),
    path("scopes/", ApplicationListCreateView.as_view()),

    path("employees/", EmployeeListCreateView.as_view()),
    path("employees/<int:pk>/", EmployeeDetailView.as_view()),
    


    
]