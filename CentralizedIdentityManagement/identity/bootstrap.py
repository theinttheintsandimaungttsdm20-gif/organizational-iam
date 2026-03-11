from django.contrib.auth import get_user_model
from .models import Role, Application, ApplicationPolicy, Scope, RoleScope
from .config_loader import load_initial_config

User = get_user_model()


def bootstrap_system():
    # Run only if no SUPER_ADMIN exists
    if User.objects.filter(role__name="SUPER_ADMIN").exists():
        return

    config = load_initial_config()

    # 1️⃣ Create roles
    role_map = {}
    for role_name in config["roles"]:
        role, _ = Role.objects.get_or_create(name=role_name)
        role_map[role_name] = role

    # 2️⃣ Create scopes
    scope_map = {}
    for scope_name in config["scopes"]:
        scope, _ = Scope.objects.get_or_create(name=scope_name)
        scope_map[scope_name] = scope

    # 3️⃣ Assign scopes to roles (RBAC hierarchy via inheritance)
    for role_name, scopes in config["role_scopes"].items():
        role = role_map[role_name]
        for scope_name in scopes:
            RoleScope.objects.get_or_create(
                role=role,
                scope=scope_map[scope_name]
            )

    # 4️⃣ Create application (Working Hour System)
    app_cfg = config["applications"][0]
    application, _ = Application.objects.get_or_create(
        client_id=app_cfg["client_id"],
        defaults={"name": app_cfg["name"]}
    )

    # 5️⃣ Create session policy (30 min default for MANAGER)
    ApplicationPolicy.objects.get_or_create(
        application=application,
        role=role_map["MANAGER"],
        defaults={
            "session_timeout_seconds": app_cfg["default_session_timeout"]
        }
    )

    # 6️⃣ Create default SUPER_ADMIN
    admin_cfg = config["admin"]
    User.objects.create_superuser(
        email=admin_cfg["email"],
        password=admin_cfg["password"],
        role=role_map[admin_cfg["role"]],
        force_password_change=True
    )
