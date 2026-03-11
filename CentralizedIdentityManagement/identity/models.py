from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager


class Role(models.Model):
    """
    Role acts as a logical grouping of privileges.
    Role hierarchy is implemented via scope inheritance.
    """
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    role = models.ForeignKey(Role, on_delete=models.PROTECT)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    force_password_change = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class Application(models.Model):
    """
    Represents a client application (e.g. Working Hour System).
    """
    name = models.CharField(max_length=100)
    client_id = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Scope(models.Model):
    """
    Fine-grained privilege following OAuth2 scope concept.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class ApplicationPolicy(models.Model):
    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE
    )
    session_timeout_seconds = models.IntegerField(default=1800)
        
class RoleScope(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    scope = models.ForeignKey(Scope, on_delete=models.CASCADE)
    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name="role_scopes"
    )

    class Meta:
        unique_together = ("role", "scope", "application")

class AuditLog(models.Model):
    """
    Records security-relevant events for auditing.
    """
    user_email = models.EmailField(null=True, blank=True)
    action = models.CharField(max_length=100)
    resource = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"{self.timestamp} - {self.action}"
