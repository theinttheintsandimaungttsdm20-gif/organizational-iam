from django.urls import path
from .views import (
    AdminLoginView,
    EmployeeListCreateView,
    EmployeeDetailView,
    EmployeeDeleteView,
    RoleScopeListView,
    RoleScopeUpdateView,
    RoleScopeDeleteView,
    SessionPolicyListCreateView,
    SessionPolicyUpdateView,
    ApplicationAccessMatrixView,
    ApplicationListCreateView,
    ApplicationDeleteView,
    RoleListCreateView,
    RoleDeleteView,
    ScopeListCreateView,
    ScopeDeleteView
)

urlpatterns = [
    path("auth/login/", AdminLoginView.as_view(), name="admin-login"),

    path("applications/", ApplicationListCreateView.as_view()),
    path("applications/<int:app_id>/", ApplicationDeleteView.as_view()),
    path("roles/<int:role_id>/", RoleDeleteView.as_view()),
    path("applications/<str:app_id>/role-scopes/", RoleScopeListView.as_view()),
    path("applications/role-scopes/", RoleScopeUpdateView.as_view()),
    path("applications/role-scopes/<int:rs_id>/", RoleScopeDeleteView.as_view()),
    path("applications/session-policy/", SessionPolicyUpdateView.as_view()),
    path("session-policies/", SessionPolicyListCreateView.as_view()),
    path("applications/<str:client_id>/access-matrix/", ApplicationAccessMatrixView.as_view()),
    
    path("roles/", RoleListCreateView.as_view()),
    path("scopes/", ScopeListCreateView.as_view()),
    path("scopes/<int:scope_id>/", ScopeDeleteView.as_view()),

    path("employees/", EmployeeListCreateView.as_view()),
    path("employees/<int:pk>/", EmployeeDetailView.as_view()),
    path("employees/delete/<int:pk>/", EmployeeDeleteView.as_view()),


    
]