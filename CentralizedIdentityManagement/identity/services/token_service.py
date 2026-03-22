from datetime import datetime, timedelta, timezone
import jwt
from django.conf import settings
from identity.models import RoleScope, Application, ApplicationPolicy


def _now_utc():
    return datetime.now(timezone.utc)


def get_scopes_for_role(role) -> list[str]:
    return list(
        RoleScope.objects.filter(role=role)
        .select_related("scope")
        .values_list("scope__name", flat=True)
    )


def get_timeout_seconds(application_client_id: str, role) -> int:
    # if policy not found, use default fallback
    default_timeout = settings.JWT_SETTINGS["DEFAULT_TIMEOUT_SECONDS"]

    try:
        app = Application.objects.get(client_id=application_client_id)
    except Application.DoesNotExist:
        return default_timeout

    policy = ApplicationPolicy.objects.filter(application=app).first()
    return policy.session_timeout_seconds if policy else default_timeout

def issue_admin_access_token(user):
    """
    Issue a global admin access token.
    This token is NOT tied to any specific application.
    """

    now = _now_utc()

    payload = {
        "iss": settings.JWT_SETTINGS["ISSUER"],
        "aud": settings.JWT_SETTINGS["AUDIENCE"],
        "sub": str(user.id),
        "email": user.email,
        "role": "ADMIN",
        "scope": (
            "settings.read settings.write "
            "application.manage role.manage"
        ),
        "iat": now,
        "exp": now + timedelta(seconds=settings.JWT_SETTINGS["DEFAULT_TIMEOUT_SECONDS"])
    }

    return jwt.encode(
        payload,
        settings.JWT_SETTINGS["SIGNING_KEY"],
        algorithm=settings.JWT_SETTINGS["ALGORITHM"],
    )


def issue_access_token(user, application_client_id: str) -> str:
    scopes = get_scopes_for_role(user.role)
    timeout_seconds = get_timeout_seconds(application_client_id, user.role)

    now = _now_utc()
    exp = now + timedelta(seconds=timeout_seconds)

    payload = {
        "iss": settings.JWT_SETTINGS["ISSUER"],
        "aud": settings.JWT_SETTINGS["AUDIENCE"],
        "iat": int(now.timestamp()),
        "exp": int(exp.timestamp()),
        "sub": str(user.id),
        "email": user.email,
        "name": user.name,
        "role": user.role.name,
        "scope": " ".join(scopes),
        "client_id": application_client_id,
    }

    token = jwt.encode(
        payload,
        settings.JWT_SETTINGS["SIGNING_KEY"],
        algorithm=settings.JWT_SETTINGS["ALGORITHM"],
    )

    return token
