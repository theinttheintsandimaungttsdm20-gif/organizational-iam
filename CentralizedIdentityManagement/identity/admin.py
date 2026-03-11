from django.contrib import admin
from .models import (
    User,
    Role,
    Application,
    ApplicationPolicy,
    Scope,
    RoleScope,
)

admin.site.register(User)
admin.site.register(Role)
admin.site.register(Application)
admin.site.register(ApplicationPolicy)
admin.site.register(Scope)
admin.site.register(RoleScope)
