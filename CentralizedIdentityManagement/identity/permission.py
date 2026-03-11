from rest_framework.permissions import BasePermission


class HasScope(BasePermission):
    """
    Checks if the request has required scopes.
    """

    def has_permission(self, request, view):
        required_scopes = getattr(view, "required_scopes", [])
        user_scopes = getattr(request, "scopes", [])
        if request.user.role == "ADMIN":
                return True
        return all(scope in user_scopes for scope in required_scopes)