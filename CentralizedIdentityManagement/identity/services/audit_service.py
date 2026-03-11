from identity.models import AuditLog


def log_event(action, resource, request=None, user=None):
    ip = None
    email = None

    if request:
        ip = request.META.get("REMOTE_ADDR")

    if user:
        email = getattr(user, "email", None)

    AuditLog.objects.create(
        user_email=email,
        action=action,
        resource=resource,
        ip_address=ip,
    )
