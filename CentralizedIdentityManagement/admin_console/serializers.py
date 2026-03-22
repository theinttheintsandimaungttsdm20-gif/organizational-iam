from rest_framework import serializers
from identity.models import User, Role,Scope, Application, ApplicationPolicy, RoleScope

class AdminLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

# class UserCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ["email", "password", "role"]
#         extra_kwargs = {
#             "password": {"write_only": True}
#         }

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserRoleUpdateSerializer(serializers.Serializer):
    role_id = serializers.IntegerField()

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:        
        model = Application
        fields = "__all__"

class SessionPolicySerializer(serializers.ModelSerializer):
    class Meta:        
        model = ApplicationPolicy
        fields = "__all__"

class RoleSerializer(serializers.ModelSerializer):
    class Meta:        
        model = Role
        fields = "__all__"

class ScopeSerializer(serializers.ModelSerializer):
    class Meta:        
        model = Scope
        fields = "__all__"


class RoleScopeUpdateSerializer(serializers.Serializer):
    application = serializers.CharField()
    role = serializers.CharField()
    scopes = serializers.ListField(
        child=serializers.CharField()
    )

    def validate_application(self, value):
        return Application.objects.get(client_id=value)

    def validate_role(self, value):
        return Role.objects.get(name=value)

# class SessionPolicyUpdateSerializer(serializers.Serializer):
#     application_id = serializers.IntegerField()
#     role_id = serializers.IntegerField()
#     session_timeout_seconds = serializers.IntegerField(min_value=60)

class SessionPolicyUpdateSerializer(serializers.Serializer):
    application = serializers.CharField()
    session_timeout_seconds = serializers.IntegerField(min_value=60)

    def validate_application(self, value):
        return Application.objects.get(client_id=value)